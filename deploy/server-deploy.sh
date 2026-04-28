#!/bin/bash
# 服务器部署脚本 - 用于手动拉取 GitHub 镜像并运行
# 用法: bash server-deploy.sh [GITHUB_USERNAME] [GITHUB_TOKEN]

set -e

GITHUB_USER="${1:-}"
GITHUB_TOKEN="${2:-${GITHUB_TOKEN:-}}"

# 镜像名称转小写（Docker 要求）
GITHUB_USER_LC=$(echo "$GITHUB_USER" | tr '[:upper:]' '[:lower:]')
IMAGE="ghcr.io/${GITHUB_USER_LC}/tcm-meridian-inference:latest"
CONTAINER_NAME="tcm-api"
PORT="18790"

if [ -z "$GITHUB_USER" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "用法: bash server-deploy.sh <GITHUB_USERNAME> <GITHUB_TOKEN>"
    echo "或者设置环境变量: export GITHUB_TOKEN=your_token"
    exit 1
fi

echo "=== TCM API 部署脚本 ==="
echo "用户: $GITHUB_USER_LC"
echo "镜像: $IMAGE"
echo "端口: $PORT"

# 登录 GitHub Container Registry
echo ""
echo "[1/5] 登录 GitHub Container Registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USER" --password-stdin

# 拉取镜像
echo ""
echo "[2/5] 拉取镜像..."
docker pull "$IMAGE"

# 停止旧容器
echo ""
echo "[3/5] 停止旧容器..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# 读取环境变量
if [ -f .env ]; then
    echo ""
    echo "[4/5] 读取环境变量..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# 启动新容器
echo ""
echo "[5/5] 启动容器..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p "$PORT:$PORT" \
    -e TCM_API_PORT="$PORT" \
    -e TCM_INFER_MODE="${TCM_INFER_MODE:-auto}" \
    -e TCM_LOG_LEVEL="${TCM_LOG_LEVEL:-INFO}" \
    -e DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-}" \
    -e DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek-chat}" \
    "$IMAGE"

# 等待启动
sleep 5

# 健康检查
echo ""
echo "=== 健康检查 ==="
if curl -s "http://localhost:$PORT/health" | grep -q '"status": "ok"'; then
    echo "✅ 部署成功!"
    echo "API 地址: http://$(curl -s ip.sb 2>/dev/null || echo 'localhost'):$PORT"
    curl -s "http://localhost:$PORT/health"
else
    echo "⚠️ 健康检查失败，查看日志:"
    docker logs "$CONTAINER_NAME" --tail 20
    exit 1
fi

echo ""
echo "管理命令:"
echo "  查看日志: docker logs -f $CONTAINER_NAME"
echo "  停止服务: docker stop $CONTAINER_NAME"
echo "  重启服务: docker restart $CONTAINER_NAME"
