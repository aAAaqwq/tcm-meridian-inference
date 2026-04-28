#!/bin/bash
# 在服务器上运行: bash install-docker.sh

set -e

echo "=== 安装 Docker ==="
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
    echo "Docker 安装完成"
else
    echo "Docker 已安装: $(docker --version)"
fi

if ! command -v docker-compose &> /dev/null; then
    echo "=== 安装 Docker Compose ==="
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    echo "Docker Compose 安装完成"
else
    echo "Docker Compose 已安装: $(docker-compose --version)"
fi

echo "=== 安装完成 ==="
