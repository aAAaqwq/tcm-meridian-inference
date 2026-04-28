# TCM Meridian Inference API - Docker 部署指南

> 端口: **18790** (统一配置)

## 部署方式选择

| 方式 | 适用场景 | 复杂度 |
|------|---------|--------|
| **GitHub Actions 自动部署** | 正式环境，持续集成 | 低 |
| 服务器手动拉取镜像 | 测试环境，快速验证 | 中 |
| Docker Compose 本地构建 | 开发调试 | 高 |

---

## 方式一: GitHub Actions 自动部署 (推荐)

代码推送到 main 分支后，自动构建镜像并部署到服务器。

### 配置步骤

1. **在 GitHub 添加 Secrets**

   仓库 → Settings → Secrets → New repository secret

   | Secret | 说明 |
   |--------|------|
   | `SSH_HOST` | 服务器 IP，如 `180.76.137.183` |
   | `SSH_USER` | SSH 用户名，如 `root` |
   | `SSH_PASSWORD` | SSH 密码 |
   | `DEEPSEEK_API_KEY` | DeepSeek API Key |

2. **推送代码触发部署**

   ```bash
   git push origin main
   ```

3. **查看部署状态**

   GitHub → Actions → Build and Deploy

### 服务器准备

在服务器上执行（仅需一次）：

```bash
# 1. 确保 Docker 已安装
docker --version

# 2. 开放防火墙端口
firewall-cmd --permanent --add-port=18790/tcp
firewall-cmd --reload
```

---

## 方式二: 服务器手动部署

如果 GitHub Actions 不可用，可手动拉取镜像并运行。

### 前提条件

- 已配置 GitHub Secrets 中的环境变量
- 服务器已安装 Docker（Snap 版本也可以）

### 部署步骤

```bash
# 1. 登录服务器
ssh root@180.76.137.183

# 2. 创建工作目录
cd ~ && mkdir -p tcm-api && cd tcm-api

# 3. 登录 GitHub Container Registry
# 获取 Token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
# 需要权限: read:packages
docker login ghcr.io -u YOUR_GITHUB_USERNAME
# 输入 Token 作为密码

# 4. 拉取镜像
docker pull ghcr.io/aaaqwq/tcm-meridian-inference:latest

# 5. 运行容器
docker run -d \
  --name tcm-api \
  --restart unless-stopped \
  -p 18790:18790 \
  -e TCM_API_PORT=18790 \
  -e TCM_INFER_MODE=auto \
  -e TCM_LOG_LEVEL=INFO \
  -e DEEPSEEK_API_KEY=sk-your-api-key \
  ghcr.io/aaaqwq/tcm-meridian-inference:latest

# 6. 验证
curl http://localhost:18790/health
```

### 使用部署脚本（简化版）

```bash
# 下载部署脚本
curl -O https://raw.githubusercontent.com/AAAaqwq/tcm-meridian-inference/main/deploy/server-deploy.sh
chmod +x server-deploy.sh

# 运行（交互式输入 Token）
./server-deploy.sh YOUR_GITHUB_USERNAME
```

---

## 方式三: Docker Compose 本地构建（开发调试用）

仅在需要修改代码并本地构建时使用。

> ⚠️ **注意**: Snap 安装的 Docker 有沙盒限制，建议将项目放在用户目录（`~`）下，而非 `/opt`

### 前置要求

```bash
# 检查 Docker 版本
docker --version
docker-compose --version

# 如未安装，使用官方脚本（推荐）
curl -fsSL https://get.docker.com | sh
```

### 部署步骤

```bash
# 1. 克隆代码（或上传 tar 包）
cd ~ && git clone <repo-url> tcm-api
cd tcm-api

# 2. 配置环境变量
cp .env.example .env
nano .env  # 填入 DEEPSEEK_API_KEY

# 3. 启动服务
docker-compose up -d

# 4. 验证
curl http://localhost:18790/health
```

---

## Snap Docker 注意事项

如果你的服务器使用 `snap install docker` 安装的 Docker：

### 限制
- 默认无法访问 `/opt` 目录
- 沙盒限制可能导致文件权限问题

### 解决方案

```bash
# 方案 1: 项目放在用户目录（推荐）
cd ~ && mkdir tcm-api

# 方案 2: 卸载 Snap Docker，安装官方版
sudo snap remove docker
curl -fsSL https://get.docker.com | sh
sudo reboot
```

---

## 验证部署

```bash
# 健康检查
curl http://localhost:18790/health

# API 信息
curl http://localhost:18790/

# 测试推理
curl -X POST http://localhost:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d '{"measurements":{"before":{"liver":{"left":36,"right":36},"spleen":{"left":36,"right":36},"kidney":{"left":36,"right":36},"stomach":{"left":36,"right":36},"gallbladder":{"left":36,"right":36},"bladder":{"left":36,"right":36}},"after":{"liver":{"left":36,"right":36},"spleen":{"left":36,"right":36},"kidney":{"left":36,"right":36},"stomach":{"left":36,"right":36},"gallbladder":{"left":36,"right":36},"bladder":{"left":36,"right":36}}}}'
```

---

## 防火墙配置

```bash
# firewalld (CentOS/RHEL)
firewall-cmd --permanent --add-port=18790/tcp
firewall-cmd --reload

# ufw (Ubuntu/Debian)
ufw allow 18790/tcp

# iptables
iptables -A INPUT -p tcp --dport 18790 -j ACCEPT
```

---

## 运维命令

```bash
# 查看容器状态
docker ps

# 查看日志
docker logs -f tcm-api

# 重启服务
docker restart tcm-api

# 停止服务
docker stop tcm-api && docker rm tcm-api

# 更新到最新镜像（自动部署会处理）
docker pull ghcr.io/aaaqwq/tcm-meridian-inference:latest
docker stop tcm-api
docker rm tcm-api
docker run -d ... # 重新运行

# 查看资源使用
docker stats tcm-api
```

---

## 故障排查

### 容器无法启动

```bash
# 查看日志
docker logs tcm-api

# 检查环境变量
docker inspect tcm-api | grep -A 20 Env
```

### 镜像拉取失败

```bash
# 检查网络
curl -I https://ghcr.io

# 重新登录
docker logout ghcr.io
docker login ghcr.io -u YOUR_USERNAME
```

### 端口被占用

```bash
# 检查端口占用
netstat -tlnp | grep 18790

# 释放端口
kill $(lsof -t -i:18790)
```

---

## 文件说明

```
├── Dockerfile                 # 多阶段构建镜像
├── docker-compose.yml         # 服务编排（本地开发用）
├── .dockerignore              # 排除不需要的文件
├── .env.example               # 环境变量示例
├── .github/workflows/
│   ├── deploy.yml             # GitHub Actions 工作流
│   └── README.md              # CI/CD 配置说明
├── deploy/
│   ├── tcm-api.service        # Systemd 服务文件
│   ├── server-deploy.sh       # 服务器手动部署脚本
│   └── README.md              # 本文件
├── scripts/                   # Python 应用代码
├── rules/                     # 规则库 JSON
└── prompts/                   # LLM 提示词
```

---

## 安全建议

1. **使用 SSH 密钥** 代替密码认证
2. **定期轮换 GitHub Token**
3. **配置防火墙** 仅开放必要端口
4. **启用 SSL/TLS** 生产环境必需
5. **定期更新镜像** `docker pull` 获取安全更新

---

## 端口说明

| 端口 | 用途 | 说明 |
|------|------|------|
| **18790** | **TCM API** | **主服务端口（统一使用）** |
| 80 | Nginx HTTP | 可选，配合反向代理 |
| 443 | Nginx HTTPS | 可选，SSL 加密 |
