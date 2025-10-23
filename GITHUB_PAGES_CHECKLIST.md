# GitHub Pages 部署检查清单

## 部署前检查

### ✅ 项目结构验证
- [x] 确认 frontend 目录存在且包含必要文件
- [x] 确认 package.json 文件存在且依赖配置正确
- [x] 确认 vite.config.js 配置了正确的 base 路径 `/stock/`
- [x] 确认 .env.production 文件配置了正确的 API 地址

### ✅ GitHub Actions 工作流验证
- [x] 确认 .github/workflows/deploy-to-gh-pages.yml 文件存在
- [x] 确认工作流配置正确（已移除缓存配置）
- [x] 确认触发条件设置为 push 到 main 分支
- [x] 确认权限配置正确

### ✅ 缓存配置验证
- [x] 确认 GitHub Actions 中已移除缓存配置（解决路径解析错误）
- [x] 确认没有 package-lock.json 文件不会影响部署
- [x] 确认依赖安装步骤配置正确

## 部署过程检查

### ✅ 代码推送
- [ ] 确保所有修改已提交到本地仓库
- [ ] 推送代码到 GitHub 的 main 分支
- [ ] 确认推送成功

### ✅ GitHub Actions 运行监控
- [ ] 进入 GitHub 仓库的 Actions 页面
- [ ] 确认 "Deploy to GitHub Pages" 工作流已触发
- [ ] 监控工作流执行状态，确保所有步骤通过

### ✅ 工作流步骤验证
- [ ] **Checkout**: 代码检出成功
- [ ] **Setup Node.js**: Node.js 环境设置成功（无缓存错误）
- [ ] **Install dependencies**: 依赖安装成功
- [ ] **Build frontend**: 前端构建成功
- [ ] **Setup Pages**: Pages 环境配置成功
- [ ] **Upload artifact**: 构建产物上传成功
- [ ] **Deploy to GitHub Pages**: 部署成功

## 部署后验证

### ✅ GitHub Pages 设置
- [ ] 进入仓库 Settings → Pages
- [ ] 确认部署源为 "GitHub Actions"
- [ ] 确认部署状态为 "Success"

### ✅ 网站功能验证
- [ ] 访问部署地址：https://[username].github.io/stock/
- [ ] 确认页面正常加载
- [ ] 测试主要功能（股票查询、图表显示等）
- [ ] 确认 API 调用正常

## 故障排除指南

### 🔧 缓存错误解决方案
**问题**: "Some specified paths were not resolved, unable to cache dependencies"
**原因**: frontend 目录下没有 package-lock.json 文件
**解决方案**: 已移除 GitHub Actions 中的缓存配置

### 🔧 构建失败
- 检查依赖版本兼容性
- 确认 Node.js 版本兼容性
- 查看构建日志中的具体错误信息

### 🔧 部署失败
- 确认 GitHub Pages 功能已启用
- 检查仓库权限设置
- 验证环境变量配置

### 🔧 页面无法访问
- 确认 base 路径配置正确
- 检查网络连接
- 验证域名解析

## 重要提醒
1. **缓存配置**: 已移除缓存配置以避免路径解析错误
2. **路径配置**: 确保所有路径引用都基于 `/stock/` 前缀
3. **环境变量**: 生产环境使用 .env.production 中的配置
4. **手动部署**: 可通过 GitHub Actions 页面手动触发部署