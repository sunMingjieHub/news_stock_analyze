# GitHub Pages 部署检查清单

## ✅ 前置检查
- [x] 项目包含frontend目录（前端代码）
- [x] frontend目录包含package.json文件
- [x] package.json包含正确的构建脚本（build）
- [x] frontend目录包含vite.config.js配置文件
- [x] vite.config.js配置了正确的base路径（/stock/）

## ✅ GitHub Actions工作流配置
- [x] 创建了`.github/workflows/deploy-to-gh-pages.yml`文件
- [x] 工作流在push到main分支时自动触发
- [x] 工作流包含正确的Node.js版本设置（v18）
- [x] 工作流正确设置了frontend目录的依赖安装和构建
- [x] 移除了可能导致错误的缓存配置
- [x] 工作流正确配置了GitHub Pages部署

## ✅ 环境配置
- [x] 创建了`frontend/.env.production`文件
- [x] 配置了正确的Vercel API地址
- [x] 更新了vite.config.js支持环境变量
- [x] 在GitHub仓库Secrets中配置了`VERCEL_API_URL`

## ✅ news-crawler工作流优化
- [x] 移除了本地后端服务启动步骤
- [x] 修改为直接调用Vercel API
- [x] 更新了所有API调用使用`VERCEL_API_URL`
- [x] 移除了不必要的Node.js缓存配置
- [x] 简化了工作流步骤，避免资源冲突

## ✅ 项目结构验证
- [x] frontend目录：纯前端项目，使用npm管理依赖
- [x] backend目录：Python后端项目，已独立部署到Vercel
- [x] 两个工作流职责清晰分离：
  - deploy-to-gh-pages.yml：仅前端部署
  - news-crawler.yml：定时任务，调用Vercel API

## 🔧 部署后验证
- [ ] 推送代码到main分支，观察GitHub Actions运行状态
- [ ] 确认前端成功部署到GitHub Pages
- [ ] 访问`https://[username].github.io/stock/`验证应用可访问
- [ ] 测试news-crawler工作流手动触发功能
- [ ] 验证Vercel API调用正常（检查工作流日志）

## 📝 问题记录与解决方案

### 已解决的问题
1. **缓存路径错误**：移除了GitHub Actions中的缓存配置，避免package-lock.json不存在导致的错误
2. **后端服务冲突**：news-crawler工作流现在直接调用Vercel API，避免在GitHub Actions中启动本地后端服务
3. **构建配置优化**：使用npm install替代npm ci，适应没有package-lock.json的情况

### 当前配置说明
- **前端部署**：通过deploy-to-gh-pages.yml工作流独立处理
- **后端服务**：已部署在Vercel，GitHub Actions中不包含后端部署
- **定时任务**：news-crawler.yml通过API调用与Vercel后端交互
- **环境分离**：前端和后端完全分离，避免资源冲突

## 📋 维护指南
1. **前端更新**：修改frontend目录代码后推送到main分支
2. **后端更新**：直接推送到Vercel连接的仓库分支
3. **定时任务调整**：修改news-crawler.yml中的cron表达式
4. **API变更**：更新GitHub Secrets中的VERCEL_API_URL

## 🚨 故障排除
如果部署失败，请检查：
1. GitHub Actions运行日志中的具体错误信息
2. Vercel API端点是否可访问
3. GitHub Secrets配置是否正确
4. 前端构建产物是否生成成功