# GitHub Pages 前端部署指南

## 部署流程

### 1. 启用GitHub Pages
1. 进入GitHub仓库的 **Settings** 页面
2. 左侧菜单选择 **Pages**
3. 在 **Source** 部分选择 **GitHub Actions**
4. 保存设置

### 2. 触发部署
- **自动触发**：每次推送到 `main` 分支时自动部署
- **手动触发**：在Actions页面手动运行 `Deploy to GitHub Pages` 工作流

### 3. 部署验证
部署完成后，访问：`https://[你的用户名].github.io/[仓库名]`

## 工作流配置说明

当前配置的 `deploy-to-gh-pages.yml` 工作流包含：

### Build阶段
```yaml
- name: Install dependencies
  run: npm install
  working-directory: frontend

- name: Build frontend  
  run: npm run build
  working-directory: frontend
  env:
    NODE_ENV: production
```

### Deploy阶段
```yaml
- name: Deploy to GitHub Pages
  id: deployment
  uses: actions/deploy-pages@v4
```

## 环境配置

### 前端环境变量
确保 `frontend/.env.production` 文件包含正确的后端API地址：
```env
VITE_API_BASE_URL=https://your-vercel-app.vercel.app
```

### 后端配置
后端已部署在Vercel，前端通过环境变量调用后端API。

## 故障排除

### 常见问题

**1. 构建失败**
- 检查Node.js版本兼容性
- 验证前端依赖安装
- 查看构建日志中的具体错误

**2. 部署后页面空白**
- 检查构建产物路径是否正确（应为`frontend/dist`）
- 验证环境变量配置
- 检查浏览器控制台错误信息

**3. API调用失败**
- 确认Vercel后端服务正常运行
- 检查前端环境变量中的API地址
- 验证CORS配置

### 调试方法

1. **查看工作流日志**：在GitHub Actions页面查看详细执行日志
2. **本地测试**：在本地运行 `npm run build` 验证构建过程
3. **API测试**：使用curl或Postman测试后端接口连通性

## 性能优化建议

1. **缓存优化**：考虑添加npm依赖缓存到工作流
2. **构建优化**：优化前端打包配置减少文件大小
3. **CDN加速**：考虑使用CDN加速静态资源加载

## 监控与维护

- 定期检查GitHub Pages部署状态
- 监控前端应用性能
- 更新依赖包版本
- 测试不同浏览器的兼容性

---
*最后更新: 2024-10-23*