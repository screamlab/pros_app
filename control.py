#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import signal
import argparse
import subprocess

# 用來記錄正在執行的 .sh 腳本 {檔案名稱: Popen物件}
running_processes = {}

CONTAINER_NAME = "my_app_container"  # 若你有對應的 Docker Container 可以刪除


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


def remove_container(container_name):
    """
    若有特定容器名稱，就執行 `docker rm -f` 以刪除容器
    """
    if container_name:
        print(f"[訊息] 嘗試刪除容器: {container_name}")
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


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

    # (選用) 刪除容器
    remove_container(CONTAINER_NAME)


def signal_handler(sig, frame):
    """
    捕捉 Ctrl + C (SIGINT) 時，做跟 stop_all_scripts() 一樣動作，再退出程式
    """
    print("\n[訊息] 偵測到 Ctrl + C，開始終止所有腳本並退出程式...")
    stop_all_scripts()
    sys.exit(0)


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
                print(f"{i}. 執行 {script}")
        else:
            print("[警告] 目前沒有任何 .sh 檔案可以執行！")

        print("-------------------------")
        print("b. 返回選單 (不終止目前執行的腳本)")
        print("s. 顯示正在執行的腳本")
        print("d. 終止並刪除所有正在執行的腳本 (SIGINT)")
        print("q. 結束程式 (並終止所有執行中的腳本, SIGINT)")
        print("=========================")

        if last_message:
            print(f"\n{last_message}\n")
            last_message = ""

        # 這裡用 try/except 捕捉 Ctrl + D (EOF)
        try:
            choice = input("請輸入選擇：").strip().lower()
        except EOFError:
            # 如果使用者按下 Ctrl + D，就進行跟 Ctrl + C 一樣的動作
            print("\n[訊息] 偵測到 EOF (Ctrl + D)，開始終止所有腳本並退出程式...")
            stop_all_scripts()
            sys.exit(0)

        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(sh_scripts):
                script_name = sh_scripts[idx - 1]
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

        elif choice == "b":
            last_message = "[返回選單] 不終止任何腳本。"

        elif choice == "s":
            if running_processes:
                msg_list = ["[正在執行的腳本]: "]
                for script_name, proc in running_processes.items():
                    if proc.poll() is None:
                        msg_list.append(f" - {script_name} (PID={proc.pid})")
                    else:
                        msg_list.append(f" - {script_name} (已結束)")
                last_message = "\n".join(msg_list)
            else:
                last_message = "[訊息] 沒有正在執行的腳本。"

        elif choice == "d":
            stop_all_scripts()
            input("[按 Enter 鍵繼續...]")

        elif choice == "q":
            stop_all_scripts()
            print("[訊息] 程式即將退出...")
            sys.exit(0)

        else:
            last_message = "[錯誤] 無效的選項，請重新輸入。"


if __name__ == "__main__":
    main()
