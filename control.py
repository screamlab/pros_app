import os
import sys
import signal
import argparse
import subprocess
import time

# 用來記錄正在執行的 .sh 腳本 {檔案名稱: Popen物件}
running_processes = {}

CONTAINER_NAME = "my_app_container"  # 若你有對應的 Docker Container，可以修改這裡


def parse_arguments():
    parser = argparse.ArgumentParser(description="Menu for running .sh scripts.")
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Hide the output (stdout, stderr) of the running .sh scripts.",
    )
    return parser.parse_args()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def list_sh_scripts():
    return [f for f in os.listdir(".") if f.endswith(".sh")]


def stop_all_docker_containers():
    """
    停止所有相關的 Docker 容器
    """
    print("[訊息] 停止所有相關的 Docker 容器...")
    subprocess.run(
        ["docker", "ps", "-q", "--filter", f"name={CONTAINER_NAME}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stdout=subprocess.DEVNULL)


def stop_all_scripts():
    """
    傳送 SIGINT 給所有背景執行的 .sh 腳本，再清空 running_processes
    """
    if running_processes:
        print("[訊息] 正在對所有腳本發送 SIGINT 以終止...")
        for script_name, proc in running_processes.items():
            if proc.poll() is None:  # 表示該 process 還沒結束
                pid = proc.pid
                print(f" - 終止 {script_name} (PID={pid}) => SIGINT")
                try:
                    os.kill(pid, signal.SIGINT)
                except OSError as e:
                    print(f"   [警告] 無法終止 PID={pid}：{e}")
        running_processes.clear()
        print("[訊息] 所有腳本已停止。")

    # 停止所有 Docker 容器
    stop_all_docker_containers()


def signal_handler(sig, frame):
    """
    捕捉 Ctrl + C (SIGINT) 時，做跟 stop_all_scripts() 一樣動作，再退出程式
    """
    print("\n[訊息] 偵測到 Ctrl + C，開始終止所有腳本並退出程式...")
    stop_all_scripts()
    sys.exit(0)


def check_and_pull_docker_image(script_name):
    """
    檢查腳本中是否有需要的 Docker 映像，若不存在則執行 docker pull 並顯示進度。
    """
    with open(script_name, "r") as script_file:
        script_content = script_file.read()

    # 提取 docker run 或 docker pull 中的映像名稱
    images = []
    for line in script_content.splitlines():
        if "docker run" in line or "docker pull" in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if part in ["docker", "run", "pull"] and i + 1 < len(parts):
                    images.append(parts[i + 1])

    for image in images:
        print(f"[檢查] Docker 映像檔: {image}")
        result = subprocess.run(
            ["docker", "images", "-q", image],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if not result.stdout.strip():
            print(f"[缺失] 映像檔 {image} 不存在，開始拉取...")
            pull_process = subprocess.Popen(
                ["docker", "pull", image], stdout=sys.stdout, stderr=sys.stderr
            )
            try:
                pull_process.wait()  # 等待拉取完成
            except KeyboardInterrupt:
                print("\n[訊息] 拉取過程中偵測到 Ctrl + C，正在取消...")
                pull_process.terminate()
                stop_all_docker_containers()
                sys.exit(1)
            if pull_process.returncode == 0:
                print(f"[成功] 映像檔 {image} 拉取完成！")
            else:
                print(f"[錯誤] 拉取映像檔 {image} 失敗！")
        else:
            print(f"[成功] 映像檔 {image} 已存在！")


def main():
    args = parse_arguments()
    silent = args.silent

    # 掛載 Ctrl+C (SIGINT) 的訊號處理
    signal.signal(signal.SIGINT, signal_handler)

    sh_scripts = list_sh_scripts()
    last_message = ""

    while True:
        clear_screen()
        print("========== 選單 ==========")
        if sh_scripts:
            for i, script in enumerate(sh_scripts, start=1):
                print(f"{i}. 檢查並執行 {script}")
        else:
            print("[警告] 目前沒有任何 .sh 檔案可以執行！")

        print("-------------------------")
        print("q. 結束程式 (並終止所有執行中的腳本, SIGINT)")
        print("=========================")

        if last_message:
            print(f"\n{last_message}\n")
            last_message = ""

        try:
            choice = input("請輸入選擇：").strip().lower()
        except EOFError:
            print("\n[訊息] 偵測到 EOF (Ctrl + D)，開始終止所有腳本並退出程式...")
            stop_all_scripts()
            sys.exit(0)

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(sh_scripts):
                script_name = sh_scripts[idx - 1]
                check_and_pull_docker_image(script_name)
                existing_proc = running_processes.get(script_name)
                if existing_proc and existing_proc.poll() is None:
                    last_message = (
                        f"[警告] {script_name} 已在執行中 (PID={existing_proc.pid})"
                    )
                else:
                    if silent:
                        p = subprocess.Popen(
                            ["/bin/bash", script_name],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                    else:
                        p = subprocess.Popen(["/bin/bash", script_name])
                    running_processes[script_name] = p
                    last_message = f"[啟動] {script_name} (PID={p.pid})"
            else:
                last_message = "[錯誤] 沒有這個選項，請重新輸入。"

        elif choice == "q":
            stop_all_scripts()
            print("[訊息] 程式即將退出...")
            sys.exit(0)

        else:
            last_message = "[錯誤] 無效的選項，請重新輸入。"


if __name__ == "__main__":
    main()
