# TCM Meridian Inference API - Docker 部署指南

> 端口: **12000** (已配置)

## 完整部署流程 (从无到有)

假设你有一台全新的服务器 (例如: 180.76.137.183)，以下是完整的部署步骤：

### 步骤 1: 本地打包代码

在开发机上执行：

```bash
cd /path/to/tcm-meridian-inference-mvp

# 创建部署包 (包含所有必需文件)
tar czf deploy.tar.gz \
  Dockerfile docker-compose.yml .dockerignore \
  scripts/ rules/ prompts/ logs/ \
  .env.example deploy/

# 查看打包内容
tar tzf deploy.tar.gz | head -20
```

### 步骤 2: 上传到服务器

```bash
# 使用 scp 上传到服务器 /opt 目录
scp deploy.tar.gz root@180.76.137.183:/opt/

# SSH 登录服务器
ssh root@180.76.137.183
```

### 步骤 3: 服务器端解压

```bash
# 登录服务器后执行
cd /opt

# 创建目录并解压
mkdir -p tcm-api
tar xzf deploy.tar.gz -C tcm-api/
cd tcm-api

# 查看目录结构
ls -la
```

### 步骤 4: 安装 Docker (如未安装)

```bash
# 一键安装 Docker
curl -fsSL https://get.docker.com | sh

# 启动 Docker 服务
systemctl enable --now docker

# 验证安装
docker --version  # 应显示 20.10+ 版本

# 安装 Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# 验证
docker-compose --version
```

### 步骤 5: 配置环境变量

```bash
cd /opt/tcm-api

# 复制示例配置
cp .env.example .env

# 编辑配置 (填入你的 DeepSeek API Key)
nano .env
```

`.env` 文件内容：
```bash
# DeepSeek API (Hybrid 模式需要)
DEEPSEEK_API_KEY=sk-your-api-key-here
DEEPSEEK_MODEL=deepseek-chat

# 推理模式: rule | agent | auto
TCM_INFER_MODE=auto

# 日志级别: DEBUG | INFO | WARNING | ERROR
TCM_LOG_LEVEL=INFO
```

### 步骤 6: 构建并启动服务

```bash
# 构建镜像并启动容器
docker-compose up -d --build

# 查看构建日志
docker-compose logs -f

# 等待服务启动 (约 10-30 秒)
sleep 10
```

### 步骤 7: 验证部署

```bash
# 健康检查
curl http://localhost:12000/health

# 预期输出:
# {"status": "ok", "service": "tcm-meridian-api", ...}

# 查看 API 信息
curl http://localhost:12000/

# 测试推理
curl -X POST http://localhost:12000/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d '{"measurements":{"before":{"liver":{"left":36,"right":36},"spleen":{"left":36,"right":36},"kidney":{"left":36,"right":36},"stomach":{"left":36,"right":36},"gallbladder":{"left":36,"right":36},"bladder":{"left":36,"right":36}},"after":{"liver":{"left":36,"right":36},"spleen":{"left":36,"right":36},"kidney":{"left":36,"right":36},"stomach":{"left":36,"right":36},"gallbladder":{"left":36,"right":36},"bladder":{"left":36,"right":36}}}}'
```

### 步骤 8: 配置防火墙

```bash
# 开放 12000 端口 (firewalld)
firewall-cmd --permanent --add-port=12000/tcp
firewall-cmd --reload

# 或使用 ufw
ufw allow 12000/tcp

# 或使用 iptables
iptables -A INPUT -p tcp --dport 12000 -j ACCEPT
```

### 步骤 9: 外网访问测试

在本地机器上测试：

```bash
# 替换为你的服务器 IP
curl http://180.76.137.183:12000/health
```

---

## 快速开始 (已有 Docker 环境)

如果服务器已安装 Docker，可直接使用以下简化步骤：

### 1. 环境准备

确保服务器已安装:
- Docker 20.10+
- Docker Compose 2.0+

```bash
# 检查安装
docker --version
docker-compose --version
```

确保服务器已安装:
- Docker 20.10+
- Docker Compose 2.0+

```bash
# 检查安装
docker --version
docker-compose --version
```

### 2. 配置环境变量

```bash
cp .env.example .env
nano .env  # 编辑配置
```

**必需配置**:
```bash
# DeepSeek API (Hybrid模式需要)
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_MODEL=deepseek-chat

# 推理模式: rule | agent | auto
TCM_INFER_MODE=auto

# 日志级别: DEBUG | INFO | WARNING | ERROR
TCM_LOG_LEVEL=INFO
```

### 3. 部署方式选择

#### 方式 A: Docker Compose (推荐)

```bash
# 克隆项目到服务器
git clone <repo-url> /opt/tcm-api
cd /opt/tcm-api

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 验证部署
curl http://localhost:12000/health
```

#### 方式 B: Systemd 服务 (生产推荐)

```bash
# 1. 复制项目到 /opt
cp -r . /opt/tcm-api
cd /opt/tcm-api

# 2. 安装 systemd 服务
sudo cp deploy/tcm-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tcm-api

# 3. 启动服务
sudo systemctl start tcm-api

# 4. 查看状态
sudo systemctl status tcm-api
sudo journalctl -u tcm-api -f
```

#### 方式 C: 部署脚本

```bash
chmod +x deploy/deploy.sh

# 本地测试部署
./deploy/deploy.sh local

# 仅构建镜像
./deploy/deploy.sh build

# 构建并测试
./deploy/deploy.sh test
```

### 4. 验证部署

```bash
# 健康检查
curl http://localhost:12000/health

# API 信息
curl http://localhost:12000/

# 测试推理
curl -X POST http://localhost:12000/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d '{
    "measurements": {
      "before": {
        "liver": {"left": 36, "right": 36},
        "spleen": {"left": 36, "right": 36},
        "kidney": {"left": 36, "right": 36},
        "stomach": {"left": 36, "right": 36},
        "gallbladder": {"left": 36, "right": 36},
        "bladder": {"left": 36, "right": 36}
      },
      "after": {
        "liver": {"left": 36, "right": 36},
        "spleen": {"left": 36, "right": 36},
        "kidney": {"left": 36, "right": 36},
        "stomach": {"left": 36, "right": 36},
        "gallbladder": {"left": 36, "right": 36},
        "bladder": {"left": 36, "right": 36}
      }
    }
  }'
```

## 生产环境配置

### Nginx 反向代理 (可选)

如需使用 Nginx:

```bash
# 启动包含 nginx 的服务
docker-compose --profile with-nginx up -d
```

或手动配置 Nginx:
```bash
sudo apt install nginx
sudo cp nginx/conf.d/default.conf /etc/nginx/sites-available/tcm-api
sudo ln -s /etc/nginx/sites-available/tcm-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL 证书 (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 防火墙配置

```bash
# UFW
sudo ufw allow 12000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 或 iptables
sudo iptables -A INPUT -p tcp --dport 12000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## 运维命令

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 更新到最新版本
docker-compose pull
docker-compose up -d

# 停止服务
docker-compose down

# 进入容器调试
docker-compose exec tcm-api sh

# 查看资源使用
docker stats tcm-api
```

## 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker-compose logs --tail=100

# 检查环境变量
docker-compose exec tcm-api env | grep TCM
```

### API 无响应

```bash
# 检查容器状态
docker ps

# 测试容器内部
docker-compose exec tcm-api wget -qO- http://localhost:8080/health
```

### 内存/CPU 过高

```bash
# 监控资源
docker stats

# 调整资源限制 (docker-compose.yml)
# deploy.resources.limits.memory: 512M
```

## 安全建议

1. **使用非 root 用户运行容器** (已在 Dockerfile 配置)
2. **定期更新基础镜像**
3. **限制端口访问** (使用防火墙)
4. **配置 SSL/TLS** (生产环境必需)
5. **启用日志轮转** (已在 docker-compose.yml 配置)
6. **设置资源限制** (CPU/内存限制已配置)

## Systemd 服务部署 (生产推荐)

如果你希望使用 Systemd 管理服务（而非 Docker Compose），可按以下步骤操作：

### 1. 安装 Docker

同上，确保 Docker 和 Docker Compose 已安装。

### 2. 复制项目文件

```bash
# 将项目复制到 /opt 目录
cp -r /opt/tcm-api /opt/tcm-api-backup  # 备份（如有）
cd /opt/tcm-api
```

### 3. 安装 Systemd 服务

```bash
# 复制服务文件
sudo cp deploy/tcm-api.service /etc/systemd/system/

# 重新加载 Systemd
sudo systemctl daemon-reload

# 设置开机自启
sudo systemctl enable tcm-api
```

### 4. 配置环境变量

```bash
# 编辑环境变量
nano /opt/tcm-api/.env
```

### 5. 启动服务

```bash
# 启动
sudo systemctl start tcm-api

# 查看状态
sudo systemctl status tcm-api

# 查看日志
sudo journalctl -u tcm-api -f

# 重启
sudo systemctl restart tcm-api

# 停止
sudo systemctl stop tcm-api
```

---

## 文件说明

```
├── Dockerfile              # 多阶段构建镜像
├── docker-compose.yml      # 服务编排
├── .dockerignore           # 排除不需要的文件
├── .env.example            # 环境变量示例
├── nginx/
│   ├── nginx.conf          # Nginx 主配置
│   └── conf.d/
│       └── default.conf    # 站点配置
├── deploy/
│   ├── tcm-api.service     # Systemd 服务文件
│   ├── deploy.sh           # 本地部署脚本
│   ├── remote-deploy.sh    # 远程一键部署脚本
│   ├── install-docker.sh   # Docker 安装脚本
│   └── README.md           # 本文件
├── scripts/                # Python 应用代码
├── rules/                  # 规则库 JSON
├── prompts/                # LLM 提示词
└── logs/                   # 日志目录
```

## 端口说明

| 端口 | 用途 | 说明 |
|------|------|------|
| 12000 | TCM API | 主服务端口 |
| 8080 | 容器内部 | 不直接暴露 |
| 80 | Nginx HTTP | 可选 |
| 443 | Nginx HTTPS | 可选 |
