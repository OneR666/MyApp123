# 使用 Ubuntu 22.04 基础镜像
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3.10 python3.10-venv python3.10-distutils \
       git zip unzip openjdk-17-jdk build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境并安装 Python 包
RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install buildozer kivy

# 工作目录
WORKDIR /app

# 将项目内容复制到容器中（使用时挂载外部卷覆盖此目录）
COPY . /app

# 构建 APK
RUN buildozer -v android debug

# 将生成的 APK 复制到 /output
CMD cp /app/bin/*.apk /output/
