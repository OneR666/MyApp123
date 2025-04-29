#!/usr/bin/env bash
# 构建脚本：在项目根目录运行，将自动使用 Docker 构建 APK
# 使用方式：
#   mkdir -p output
#   ./build.sh

set -e
docker build -t kivy-builder .
# 确保本地有 output 目录
mkdir -p output
docker run --rm \
    -v "$(pwd)":/app \
    -v "$(pwd)/output":/output \
    kivy-builder
echo "APK 已输出到 output/ 目录"
