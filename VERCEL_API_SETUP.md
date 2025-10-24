# Vercel API URL 配置指南

## 问题描述

GitHub Actions定时任务失败，错误信息显示API调用使用了相对路径 `/api/news/crawl`，这是因为 `VERCEL_API_URL` secret 未正确设置。

## 解决方案

### 步骤1：获取你的Vercel部署地址

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 找到你的股票分析项目
3. 复制部署地址（格式如：`https://your-app-name.vercel.app`）

### 步骤2：在GitHub仓库中设置Secret

1. 进入你的GitHub仓库页面
2. 点击 **Settings** 标签页
3. 在左侧菜单选择 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** 按钮
5. 填写以下信息：
   - **Name**: `VERCEL_API_URL`
   - **Value**: 你的Vercel部署地址（例如：`https://your-app.vercel.app`）

### 步骤3：验证配置

1. 在GitHub仓库的 **Actions** 标签页
2. 找到 **股票新闻自动爬取与分析** 工作流
3. 点击 **Run workflow** 手动触发测试
4. 观察执行日志，确认API调用成功

## 配置示例

正确的secret配置示例：
```
Name: VERCEL_API_URL
Value: https://stock-analysis-app.vercel.app
```

## 常见问题排查

### 1. API返回404错误
- 检查Vercel应用是否正常部署
- 确认后端服务在Vercel上正常运行
- 验证API路由配置是否正确

### 2. API返回5xx错误
- 检查后端代码是否有运行时错误
- 查看Vercel部署日志排查问题
- 确认环境变量配置正确

### 3. Secret设置后仍然失败
- 确认secret名称完全匹配 `VERCEL_API_URL`
- 检查secret值是否包含协议头（http://或https://）
- 重启工作流重新加载secret

## 测试API连通性

部署完成后，可以通过以下命令测试API连通性：

```bash
# 测试健康检查端点
curl https://your-app.vercel.app/health

# 测试新闻爬取API
curl -X POST https://your-app.vercel.app/api/news/crawl \
  -H "Content-Type: application/json" \
  -d '{"sources": [["新浪财经","东方财富","雪球"]]}'
```

## 注意事项

- Vercel免费版有使用限制，请确保不超过配额
- GitHub Actions secret对大小写敏感
- 修改secret后需要重新运行工作流才能生效