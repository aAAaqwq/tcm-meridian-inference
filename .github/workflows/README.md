# GitHub Actions CI/CD 配置

## 工作流程

```
代码推送 ──┬── GitHub Actions ── Build 镜像 ── Push to GHCR
            └── SSH 到百度云 ── Pull 镜像 ── Run 容器
```

## 配置步骤

### 1. 添加 Secrets

GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret

必填 Secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `SSH_HOST` | 服务器 IP | `180.76.137.183` |
| `SSH_USER` | SSH 用户名 | `root` |
| `SSH_PASSWORD` | SSH 密码 | `your-password` |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | `sk-xxxxxxxx` |

可选 Secrets：

| Secret 名称 | 说明 | 默认值 |
|------------|------|--------|
| `TCM_INFER_MODE` | 推理模式 | `auto` |
| `TCM_LOG_LEVEL` | 日志级别 | `INFO` |
| `DEEPSEEK_MODEL` | 模型名称 | `deepseek-chat` |

### 2. 启用 GitHub Container Registry

1. GitHub 仓库 → Settings → Packages
2. 确保 "Inherit access from source repository" 已启用

### 3. 推送代码触发部署

```bash
git add .
git commit -m "ci: add GitHub Actions workflow"
git push origin main
```

GitHub Actions 会自动：
1. 构建 Docker 镜像
2. 推送到 GHCR (ghcr.io/用户名/仓库名:latest)
3. SSH 到百度云服务器
4. 拉取镜像并启动容器

### 4. 手动触发

GitHub → Actions → Build and Deploy → Run workflow

---

## 服务器手动部署（备用）

如果 GitHub Actions 失败，可以手动部署：

```bash
# 1. 登录服务器
ssh root@180.76.137.183

# 2. 创建目录
cd ~
mkdir -p tcm-api && cd tcm-api

# 3. 创建环境变量文件
cat > .env << EOL
DEEPSEEK_API_KEY=your-api-key
TCM_INFER_MODE=auto
TCM_LOG_LEVEL=INFO
EOL

# 4. 运行部署脚本
export GITHUB_TOKEN=your_github_token
bash deploy/server-deploy.sh your_github_username $GITHUB_TOKEN
```

或者直接用 Docker 命令：

```bash
# 登录 GitHub Container Registry
echo "your_github_token" | docker login ghcr.io -u your_github_username --password-stdin

# 拉取并运行
docker pull ghcr.io/your_github_username/tcm-meridian-inference-mvp:latest
docker run -d \
  --name tcm-api \
  --restart unless-stopped \
  -p 18790:18790 \
  -e DEEPSEEK_API_KEY=your-api-key \
  ghcr.io/your_github_username/tcm-meridian-inference-mvp:latest
```

---

## 故障排查

### 镜像拉取失败

```bash
# 在服务器上测试
docker pull ghcr.io/your_username/tcm-meridian-inference-mvp:latest

# 如果失败，检查网络或尝试代理
docker pull --platform linux/amd64 ghcr.io/your_username/tcm-meridian-inference-mvp:latest
```

### 权限错误

确保 GitHub Token 有 `write:packages` 和 `read:packages` 权限。

### 部署日志查看

GitHub 仓库 → Actions → 选择工作流运行 → 查看日志

---

## 安全建议

1. **使用 SSH 密钥** 代替密码（修改 workflow 中的 `password` 为 `key`）
2. **定期轮换 GitHub Token**
3. **限制 Token 权限**（仅 packages 和 contents）
