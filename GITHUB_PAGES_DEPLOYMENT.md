# GitHub Pages 部署指南

## 问题修复说明

### 缓存错误修复
**问题**：GitHub Actions 报错 "Some specified paths were not resolved, unable to cache dependencies."

**原因**：frontend目录下没有package-lock.json文件，但工作流中配置了缓存该文件路径

**解决方案**：
- 将缓存依赖路径从 `frontend/package-lock.json` 改为 `frontend/package.json`
- 将依赖安装命令从 `npm ci` 改为 `npm install`

## 部署前准备

### 1. 环境配置
确保您的GitHub仓库已启用GitHub Pages功能：
- 进入仓库 Settings → Pages
- Source 选择 "GitHub Actions"

### 2. 环境变量设置
在GitHub仓库中设置以下环境变量：
- `VITE_API_BASE_URL`: 您的Vercel后端API地址（如：https://stock-analysis-system-f478i1336-smjs-projects-bfe2d356.vercel.app）

## 部署流程

### 自动部署（推荐）
1. 将代码推送到 `main` 分支
2. GitHub Actions会自动触发部署流程
3. 查看 Actions 标签页监控部署状态

### 手动部署
1. 进入 GitHub Actions 页面
2. 选择 "Deploy to GitHub Pages" 工作流
3. 点击 "Run workflow" 手动触发部署

## 工作流说明

### 构建阶段 (build job)
1. **检出代码**：使用 actions/checkout@v4
2. **设置Node.js环境**：使用 actions/setup-node@v4，配置Node.js 18和npm缓存
3. **安装依赖**：在frontend目录执行 `npm install`
4. **构建前端**：执行 `npm run build` 生成生产版本
5. **配置Pages**：使用 actions/configure-pages@v4
6. **上传制品**：将dist目录上传为部署制品

### 部署阶段 (deploy job)
1. **部署到GitHub Pages**：使用 actions/deploy-pages@v4
2. **环境配置**：使用github-pages环境

## 故障排除

### 常见问题

#### 1. 构建失败
- 检查Node.js版本兼容性
- 确认package.json中的依赖版本正确
- 查看构建日志中的具体错误信息

#### 2. 缓存错误
- 确保frontend目录下有package.json文件
- 如果项目没有package-lock.json，使用package.json作为缓存依赖路径

#### 3. API连接失败
- 确认VITE_API_BASE_URL环境变量设置正确
- 检查Vercel后端服务是否正常运行

#### 4. 部署后页面空白
- 检查dist目录是否成功生成
- 确认静态资源路径配置正确

## 部署后验证

1. 访问GitHub Pages提供的URL
2. 测试前端与后端API的连接
3. 验证所有功能正常

## 相关文件
- 工作流配置：`.github/workflows/deploy-to-gh-pages.yml`
- 生产环境配置：`frontend/.env.production`
- Vite配置：`frontend/vite.config.js`

## 技术支持
如遇问题，请查看GitHub Actions的详细日志，或参考GitHub官方文档。