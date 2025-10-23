# GitHub Pages 部署指南

## 概述
本指南将帮助您将股票新闻智能分析系统的前端部署到GitHub Pages。

## 前提条件
- 项目已推送到GitHub仓库
- 您有仓库的管理员权限
- 后端服务已成功部署到Vercel

## 部署步骤

### 1. 启用GitHub Pages
1. 进入您的GitHub仓库
2. 点击 **Settings** 选项卡
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** 部分选择 **GitHub Actions**
5. 保存设置

### 2. 配置仓库设置
确保仓库设置允许GitHub Actions工作流运行：
- 进入 **Settings** → **Actions** → **General**
- 确保 **Workflow permissions** 设置为 **Read and write permissions**

### 3. 推送代码触发部署
将代码推送到main分支，GitHub Actions将自动触发部署：
```bash
git add .
git commit -m "准备GitHub Pages部署"
git push origin main
```

### 4. 监控部署状态
1. 进入仓库的 **Actions** 选项卡
2. 查看 **Deploy to GitHub Pages** 工作流的运行状态
3. 等待部署完成（通常需要2-5分钟）

### 5. 访问部署的网站
部署完成后，您的网站将可通过以下地址访问：
```
https://[您的GitHub用户名].github.io/stock/
```

## 配置说明

### 环境变量
- 生产环境API地址已配置在 `frontend/.env.production`
- 后端服务地址：`https://stock-analysis-system-f478i1336-smjs-projects-bfe2d356.vercel.app/api`

### GitHub Actions工作流
工作流文件：`.github/workflows/deploy-to-gh-pages.yml`
- 在push到main分支时自动触发
- 使用Node.js 18构建前端
- 将构建结果部署到GitHub Pages

## 故障排除

### 常见问题

#### 1. 构建失败
- 检查Node.js版本兼容性
- 查看构建日志中的错误信息
- 确保所有依赖项正确安装

#### 2. 部署后页面空白
- 检查浏览器控制台错误
- 确认base路径配置正确
- 验证API连接是否正常

#### 3. API请求失败
- 确认后端服务正常运行
- 检查CORS配置
- 验证环境变量配置

### 手动部署
如果需要手动触发部署，可以在GitHub仓库的Actions页面手动运行工作流。

## 更新部署
每次将代码推送到main分支时，部署将自动更新。您也可以通过GitHub界面手动触发部署。

## 联系支持
如果遇到问题，请检查：
1. GitHub Actions日志
2. 浏览器开发者工具控制台
3. 后端服务状态