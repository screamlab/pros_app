#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess


def list_sh_scripts():
    """列出當前目錄中的所有 .sh 檔案"""
    return [f for f in os.listdir(".") if f.endswith(".sh")]


def extract_docker_images(script_content):
    """
    從腳本內容中提取出所有使用的 Docker 映像檔名稱
    """
    images = set()
    # 匹配 docker pull 或 docker run 使用的映像檔
    pattern = r"(docker (?:pull|run)\s+)([^\s]+)"
    for match in re.finditer(pattern, script_content):
        images.add(match.group(2))
    return images


def check_image_exists(image_name):
    """
    檢查 Docker 映像檔是否已存在於本地
    """
    result = subprocess.run(
        ["docker", "images", "-q", image_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return bool(result.stdout.strip())  # 如果有結果，表示映像檔存在


def pull_image(image_name):
    """
    執行 docker pull 下載映像檔
    """
    print(f"[訊息] 拉取映像檔: {image_name}")
    result = subprocess.run(
        ["docker", "pull", image_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        print(f"[成功] 映像檔 {image_name} 拉取完成！")
    else:
        print(f"[錯誤] 無法拉取映像檔 {image_name}：\n{result.stderr}")


def main():
    # 列出所有的 .sh 檔案
    sh_scripts = list_sh_scripts()
    if not sh_scripts:
        print("[警告] 當前目錄下沒有 .sh 檔案！")
        return

    # 檢查每個腳本中的 Docker 映像檔
    for script in sh_scripts:
        print(f"\n[檢查] 腳本: {script}")
        with open(script, "r") as f:
            script_content = f.read()

        images = extract_docker_images(script_content)
        if not images:
            print(f"[訊息] 腳本 {script} 中沒有發現需要檢查的 Docker 映像檔。")
            continue

        for image in images:
            print(f"  - 檢查映像檔: {image}")
            if check_image_exists(image):
                print(f"    [存在] 映像檔 {image} 已存在於本地。")
            else:
                print(f"    [缺失] 映像檔 {image} 不存在，開始拉取...")
                pull_image(image)

    print("\n[完成] 所有腳本中的映像檔已檢查完畢！")


if __name__ == "__main__":
    main()
