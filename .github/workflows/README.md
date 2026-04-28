# GitHub Actions CI/CD 配置指南

## 工作流程

```
代码推送 ──┬── GitHub Actions ── Build 镜像 ── Push to GHCR
            └── SSH 到服务器 ── Pull 镜像 ── Run 容器
```

服务器**无需构建镜像**，只需拉取运行。

---

## 配置步骤

### 1. 添加 Secrets

GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret

**必填 Secrets：**

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `SSH_HOST` | 服务器 IP | `180.76.137.183` |
| `SSH_USER` | SSH 用户名 | `root` |
| `SSH_PASSWORD` | SSH 密码 | `your-password` |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | `sk-xxxxxxxx` |

**可选 Secrets：**

| Secret 名称 | 说明 | 默认值 |
|------------|------|--------|
| `TCM_INFER_MODE` | 推理模式 | `auto` |
| `TCM_LOG_LEVEL` | 日志级别 | `INFO` |
| `DEEPSEEK_MODEL` | 模型名称 | `deepseek-chat` |

### 2. 启用 GitHub Container Registry

1. GitHub 仓库 → Settings → Packages
2. 确保 "Inherit access from source repository" 已启用

### 3. 服务器准备（仅需一次）

```bash
# 1. 登录服务器
ssh root@180.76.137.183

# 2. 检查 Docker
docker --version

# 3. 开放防火墙端口
firewall-cmd --permanent --add-port=18790/tcp
firewall-cmd --reload

# 4. 创建目录（可选，用于存放 .env 文件）
mkdir -p ~/tcm-api && cd ~/tcm-api
```

### 4. 推送代码触发部署

```bash
git add .
git commit -m "你的修改"
git push origin main
```

GitHub Actions 会自动：
1. 构建 Docker 镜像
2. 推送到 GHCR (`ghcr.io/用户名/仓库名:latest`)
3. SSH 到服务器
4. 拉取镜像并启动容器

### 5. 验证部署

```bash
# 服务器上查看容器
docker ps

# 健康检查
curl http://localhost:18790/health

# 查看日志
docker logs -f tcm-api
```

---

## 手动触发

GitHub → Actions → Build and Deploy → Run workflow

---

## 服务器手动部署（备选）

如果 GitHub Actions 失败，可手动部署：

### 方法 1: 使用脚本

```bash
# 1. 登录服务器
ssh root@180.76.137.183

# 2. 下载部署脚本
cd ~ && curl -O https://raw.githubusercontent.com/AAAaqwq/tcm-meridian-inference/main/deploy/server-deploy.sh
chmod +x server-deploy.sh

# 3. 运行部署（需要 GitHub Token）
./server-deploy.sh YOUR_GITHUB_USERNAME YOUR_GITHUB_TOKEN
```

### 方法 2: 手动执行

```bash
# 1. 登录 GitHub Container Registry
# Token: GitHub → Settings → Developer settings → Personal access tokens
docker login ghcr.io -u YOUR_GITHUB_USERNAME

# 2. 拉取镜像
docker pull ghcr.io/aaaqwq/tcm-meridian-inference:latest

# 3. 运行容器
docker run -d \
  --name tcm-api \
  --restart unless-stopped \
  -p 18790:18790 \
  -e DEEPSEEK_API_KEY=sk-your-api-key \
  ghcr.io/aaaqwq/tcm-meridian-inference:latest

# 4. 验证
curl http://localhost:18790/health
```

---

## Snap Docker 注意事项

如果服务器使用 Snap 安装的 Docker：

```bash
# 检查是否为 Snap 版本
which docker
# 输出: /snap/bin/docker

# Snap Docker 限制：
# - 默认无法访问 /opt
# - 沙盒可能导致文件权限问题

# 解决方案：
# 1. 项目放在用户目录（~）下
# 2. 或卸载 Snap Docker，安装官方版本：
sudo snap remove docker
curl -fsSL https://get.docker.com | sh
sudo reboot
```

---

## 故障排查

### 镜像拉取失败

```bash
# 在服务器上测试
docker pull ghcr.io/aaaqwq/tcm-meridian-inference:latest

# 如果超时，检查网络或 DNS
cat /etc/resolv.conf

# 使用国内镜像（可选）
# 修改 /etc/docker/daemon.json
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
```

### 权限错误

确保 GitHub Token 有 `write:packages` 和 `read:packages` 权限。

### SSH 连接失败

```bash
# 检查服务器 SSH 配置
cat /etc/ssh/sshd_config | grep PasswordAuthentication

# 确保允许密码登录（或改用 SSH 密钥）
PasswordAuthentication yes

# 重启 SSH
systemctl restart sshd
```

### 部署日志查看

GitHub 仓库 → Actions → 选择工作流运行 → 查看日志

---

## 安全建议

1. **使用 SSH 密钥** 代替密码（修改 workflow 中的 `password` 为 `key`）
2. **定期轮换 GitHub Token**
3. **限制 Token 权限**（仅 packages 和 contents）
4. **配置防火墙** 仅开放 18790 端口
5. **启用 fail2ban** 防止暴力破解

---

## 更新部署

修改代码后推送即自动部署：

```bash
git add .
git commit -m "feat: 你的新功能"
git push origin main  # 触发自动部署
```

查看部署进度：GitHub → Actions → Build and Deploy
