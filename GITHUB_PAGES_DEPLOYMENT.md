# GitHub Pages 部署指南

## 问题修复说明

### 缓存错误解决方案
GitHub Actions 报错 "Some specified paths were not resolved, unable to cache dependencies" 的原因是：

1. **问题根源**：frontend目录下没有 `package-lock.json` 文件
2. **解决方案**：移除了 GitHub Actions 工作流中的缓存配置
3. **影响**：对于小型项目，缓存带来的性能提升有限，移除缓存不会影响部署功能

## 部署流程

### 1. 准备工作
- 确保项目已推送到 GitHub 仓库
- 在 GitHub 仓库设置中启用 Pages 功能
- 选择 "GitHub Actions" 作为部署源

### 2. 自动部署
当代码推送到 `main` 分支时，GitHub Actions 会自动执行以下步骤：

1. **Checkout** - 检出代码
2. **Setup Node.js** - 设置 Node.js 环境（v18）
3. **Install dependencies** - 安装前端依赖
4. **Build frontend** - 构建生产版本
5. **Setup Pages** - 配置 Pages 环境
6. **Upload artifact** - 上传构建产物
7. **Deploy to GitHub Pages** - 部署到 GitHub Pages

### 3. 手动触发
也可以在 GitHub Actions 页面手动触发部署：
- 进入仓库的 Actions 页面
- 选择 "Deploy to GitHub Pages" 工作流
- 点击 "Run workflow"

## 环境配置

### 前端环境变量
生产环境配置在 `frontend/.env.production`：
```
VITE_API_BASE_URL=https://stock-analysis-system-f478i1336-smjs-projects-bfe2d356.vercel.app
```

### Vite 配置
`vite.config.js` 已配置 base 路径为 `/stock/`，确保在 GitHub Pages 子路径下正常工作。

## 访问地址
部署成功后，网站将通过以下地址访问：
```
https://[username].github.io/stock/
```

## 故障排除

### 常见问题
1. **缓存错误**：已通过移除缓存配置解决
2. **路径问题**：确保 vite.config.js 中的 base 路径正确
3. **依赖安装失败**：检查 package.json 依赖版本兼容性

### 验证步骤
1. 检查 GitHub Actions 运行日志
2. 确认构建产物包含 dist 目录
3. 访问部署地址验证功能正常

## 相关文件
- 工作流配置：`.github/workflows/deploy-to-gh-pages.yml`
- 生产环境配置：`frontend/.env.production`
- Vite配置：`frontend/vite.config.js`

## 技术支持
如遇问题，请查看GitHub Actions的详细日志，或参考GitHub官方文档。