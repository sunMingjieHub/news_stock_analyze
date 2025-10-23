# GitHub Pages 前端部署指南

## 概述
本项目使用GitHub Pages部署前端应用，后端服务已独立部署在Vercel上。

## 部署流程

### 1. 自动部署
- 当代码推送到 `main` 分支时，GitHub Actions会自动触发部署流程
- 工作流文件：`.github/workflows/deploy-to-gh-pages.yml`

### 2. 手动部署
- 在GitHub仓库的Actions标签页中，选择"Deploy to GitHub Pages"工作流
- 点击"Run workflow"手动触发部署

## 工作流说明

### 前端部署工作流 (deploy-to-gh-pages.yml)
- **目的**: 仅部署前端代码到GitHub Pages
- **触发条件**: push到main分支或手动触发
- **构建步骤**:
  1. 检出代码
  2. 设置Node.js环境 (v18)
  3. 安装前端依赖 (frontend目录)
  4. 构建生产版本
  5. 上传构建产物到GitHub Pages

### 新闻爬取工作流 (news-crawler.yml) - 已优化
- **目的**: 定时自动爬取和分析股票新闻
- **触发条件**: 每小时自动运行 (北京时间9:00-18:00) 或手动触发
- **重要变更**: 现在直接调用Vercel部署的后端API，不在GitHub Actions中启动本地后端服务
- **API端点**: 使用 `VERCEL_API_URL` 环境变量指向已部署的后端服务

## 环境配置

### 前端环境变量 (frontend/.env.production)
```env
VITE_API_BASE_URL=https://stock-analysis-system-f478i1336-smjs-projects-bfe2d356.vercel.app
```

### GitHub Secrets配置
需要在GitHub仓库的Settings → Secrets and variables → Actions中配置：
- `VERCEL_API_URL`: Vercel部署的后端服务URL

## 访问地址
- GitHub Pages: `https://[username].github.io/stock/`
- Vercel后端: `https://stock-analysis-system-f478i1336-smjs-projects-bfe2d356.vercel.app`

## 故障排除

### 常见问题
1. **缓存路径错误**: 已移除缓存配置，避免package-lock.json不存在导致的错误
2. **后端服务冲突**: news-crawler工作流现在直接调用Vercel API，避免本地服务冲突
3. **构建失败**: 检查Node.js版本兼容性和依赖安装

### 调试步骤
1. 检查GitHub Actions运行日志
2. 验证环境变量配置
3. 确认API端点可访问性
4. 检查构建产物是否正确生成

## 注意事项
- 前端部署只处理frontend目录内容
- 后端服务已独立部署在Vercel，GitHub Actions中不包含后端部署
- news-crawler工作流通过API调用与Vercel后端交互
- 确保Vercel API URL在GitHub Secrets中正确配置