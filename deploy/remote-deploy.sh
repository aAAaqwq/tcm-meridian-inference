#!/bin/bash
# 一键部署脚本 - 在服务器上运行
# 下载并执行: curl -fsSL http://你的文件服务器/remote-deploy.sh | bash

set -e

APP_DIR="/opt/tcm-api"
PORT="12000"

echo "========================================="
echo "  TCM Meridian Inference API 部署脚本"
echo "========================================="

# 检查root权限
if [ "$EUID" -ne 0 ]; then
    echo "请使用 root 权限运行: sudo bash remote-deploy.sh"
    exit 1
fi

# 安装Docker
echo "[1/6] 检查 Docker..."
if ! command -v docker &> /dev/null; then
    echo "安装 Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
fi
echo "Docker: $(docker --version)"

if ! command -v docker-compose &> /dev/null; then
    echo "安装 Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi
echo "Docker Compose: $(docker-compose --version)"

# 创建目录
echo "[2/6] 创建项目目录: $APP_DIR"
mkdir -p $APP_DIR
cd $APP_DIR

# 创建 Dockerfile
echo "[3/6] 创建配置文件..."
cat > Dockerfile << 'EOF'
# Stage 1: Builder
FROM python:3.12-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --user httpx

# Stage 2: Production runner
FROM python:3.12-slim AS runner
RUN groupadd -r tcm -g 1001 && useradd -r -g tcm -u 1001 tcm
WORKDIR /app
COPY --from=builder /root/.local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /root/.local/bin /usr/local/bin
COPY --chown=tcm:tcm scripts/ ./scripts/
COPY --chown=tcm:tcm rules/ ./rules/
COPY --chown=tcm:tcm prompts/ ./prompts/
COPY --chown=tcm:tcm logs/ ./logs/
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 TCM_API_PORT=8080 TCM_INFER_MODE=auto TCM_LOG_LEVEL=INFO PATH=/usr/local/bin:$PATH
USER tcm
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1
CMD ["python3", "scripts/tcm_api.py"]
EOF

# 创建 docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'
services:
  tcm-api:
    build:
      context: .
      dockerfile: Dockerfile
    image: tcm-meridian-inference:latest
    container_name: tcm-api
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
    environment:
      - TCM_API_PORT=8080
      - TCM_INFER_MODE=\${TCM_INFER_MODE:-auto}
      - TCM_LOG_LEVEL=\${TCM_LOG_LEVEL:-INFO}
      - DEEPSEEK_API_KEY=\${DEEPSEEK_API_KEY:-}
      - DEEPSEEK_MODEL=\${DEEPSEEK_MODEL:-deepseek-chat}
    ports:
      - "${PORT}:8080"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    security_opt:
      - no-new-privileges:true
    networks:
      - tcm-network
networks:
  tcm-network:
    driver: bridge
EOF

# 创建 .dockerignore
cat > .dockerignore << 'EOF'
.git
__pycache__/
*.py[cod]
.venv/
venv/
logs/*.log
docs/
fixtures/
scripts/test_*.py
scripts/test_*.sh
.env
.env.local
.github/
EOF

# 配置环境变量
echo "[4/6] 配置环境变量..."
if [ ! -f .env ]; then
    cat > .env << 'EOF'
# DeepSeek API (Hybrid模式需要)
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-chat

# 推理模式: rule | agent | auto
TCM_INFER_MODE=auto

# 日志级别
TCM_LOG_LEVEL=INFO
EOF
    echo "环境文件已创建: $APP_DIR/.env"
    echo "⚠️  请编辑 .env 文件，填入 DEEPSEEK_API_KEY"
fi

# 克隆或复制代码
echo "[5/6] 准备应用代码..."
mkdir -p scripts rules prompts logs

# 如果当前目录有代码，使用本地代码
if [ -f "scripts/tcm_api.py" ]; then
    echo "使用本地代码..."
else
    echo "⚠️  请确保 scripts/, rules/, prompts/ 目录存在"
    echo "从 Git 仓库克隆或手动上传代码文件"
fi

# 构建并启动
echo "[6/6] 构建并启动服务..."
docker-compose down 2>/dev/null || true
docker-compose up -d --build

echo ""
echo "========================================="
echo "  部署完成!"
echo "========================================="
echo ""
echo "服务地址:"
echo "  - Health:  http://$(curl -s ip.sb 2>/dev/null || echo 'localhost'):${PORT}/health"
echo "  - API:     http://$(curl -s ip.sb 2>/dev/null || echo 'localhost'):${PORT}/"
echo ""
echo "管理命令:"
echo "  查看日志:  docker-compose logs -f"
echo "  停止服务:  docker-compose down"
echo "  重启服务:  docker-compose restart"
echo "  查看状态:  docker-compose ps"
echo ""
echo "配置文件位置: $APP_DIR/.env"
echo ""

# 等待服务启动
sleep 5
if curl -s http://localhost:${PORT}/health | grep -q '"status": "ok"'; then
    echo "✅ 服务运行正常!"
    curl -s http://localhost:${PORT}/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:${PORT}/health
else
    echo "⚠️  服务可能未完全启动，请查看日志: docker-compose logs -f"
fi
