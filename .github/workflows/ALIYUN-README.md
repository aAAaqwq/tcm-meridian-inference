# 阿里云镜像仓库部署指南

## 为什么使用阿里云？

- ✅ 国内访问速度快
- ✅ 与百度云服务器网络互通好
- ✅ 免费额度充足（个人版）

---

## 配置步骤

### 1. 创建阿里云容器镜像服务

1. 登录 [阿里云控制台](https://cr.console.aliyun.com/)
2. 创建个人版实例（免费）
3. 创建命名空间：`aaa-tcm`
4. 创建仓库：`tcm-meridian-inference`

### 2. 获取访问凭证

1. 阿里云控制台 → 容器镜像服务 → 访问凭证
2. 设置固定密码
3. 记录：
   - 用户名：你的阿里云账号
   - 密码：刚设置的固定密码

### 3. 添加 GitHub Secrets

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `ALIYUN_USERNAME` | 阿里云账号 | `aaa_xxx` |
| `ALIYUN_PASSWORD` | 固定密码 | `your-password` |
| `SSH_HOST` | 服务器 IP | `180.76.137.183` |
| `SSH_USER` | SSH 用户名 | `root` |
| `SSH_PASSWORD` | SSH 密码 | `your-password` |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | `sk-xxxxxxxx` |

### 4. 推送代码触发部署

```bash
git add .
git commit -m "ci: add aliyun deployment"
git push origin main
```

---

## 手动部署（备用）

如果 GitHub Actions 失败，可手动部署：

```bash
# 1. 登录服务器
ssh root@180.76.137.183

# 2. 登录阿里云镜像仓库
docker login registry.cn-hangzhou.aliyuncs.com -u YOUR_ALIYUN_USERNAME

# 3. 拉取镜像
docker pull registry.cn-hangzhou.aliyuncs.com/aaa-tcm/tcm-meridian-inference:latest

# 4. 运行容器
docker run -d \
  --name tcm-api \
  --restart unless-stopped \
  -p 18790:18790 \
  -e DEEPSEEK_API_KEY=sk-your-api-key \
  registry.cn-hangzhou.aliyuncs.com/aaa-tcm/tcm-meridian-inference:latest

# 5. 验证
curl http://localhost:18790/health
```

---

## 镜像地址

```
registry.cn-hangzhou.aliyuncs.com/aaa-tcm/tcm-meridian-inference:latest
```

---

## 故障排查

### 登录失败

```bash
# 检查用户名密码
docker login registry.cn-hangzhou.aliyuncs.com

# 阿里云访问凭证页面重置密码
# https://cr.console.aliyun.com/cn-hangzhou/instances/credentials
```

### 拉取失败

```bash
# 检查镜像是否存在
# 阿里云控制台 → 镜像仓库 → 查看

# 手动测试拉取
docker pull registry.cn-hangzhou.aliyuncs.com/aaa-tcm/tcm-meridian-inference:latest
```
