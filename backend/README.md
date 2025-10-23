# 股票新闻分析系统 - Python后端

这是一个使用Python Flask框架重写的股票新闻分析系统后端服务，支持AI分析、多渠道通知和新闻管理功能。

## 🚀 功能特性

- **AI新闻分析**: 支持多AI服务提供商的文章情绪分析和投资建议
- **多渠道通知**: 集成Telegram、企业微信、邮件等多种通知方式
- **新闻管理**: 新闻获取、搜索、分类和过滤功能
- **统一接口**: RESTful API设计，前后端分离架构
- **Vercel部署**: 支持无服务器部署到Vercel平台

## 📁 项目结构

```
backend/
├── app.py                 # Flask主应用
├── run.py                # 本地启动脚本
├── test_app.py           # 功能测试脚本
├── requirements.txt      # Python依赖包
├── .env.example         # 环境变量示例
├── __init__.py          # Python包初始化
├── routes/              # 路由模块
│   ├── analysis.py      # 分析路由
│   ├── news.py          # 新闻路由
│   ├── notifications.py # 通知路由
│   ├── email.py         # 邮件路由
│   ├── telegram.py      # Telegram路由
│   └── wechat_work.py   # 企业微信路由
└── services/            # 服务模块
    └── ai_service.py    # AI服务管理
```

## 🛠️ 安装和运行

### 1. 环境要求

- Python 3.8+
- pip (Python包管理器)

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量示例文件并配置实际值：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下关键参数：

```env
# AI服务配置
HUNYUAN_API_KEY=your_hunyuan_api_key
HUNYUAN_SECRET_ID=your_hunyuan_secret_id

# 邮件服务配置
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
SMTP_USERNAME=your_email@qq.com
SMTP_PASSWORD=your_email_password

# 其他服务配置...
```

### 4. 本地运行

```bash
# 方式1: 使用启动脚本
python run.py

# 方式2: 直接运行Flask应用
python app.py

# 方式3: 使用Flask命令行
export FLASK_APP=app.py
flask run --port=3001
```

### 5. 测试功能

```bash
# 运行功能测试
python test_app.py
```

## 🌐 API接口文档

### 基础端点

- `GET /` - 服务状态和API文档
- `GET /health` - 健康检查
- `GET /api/analysis/ai-status` - AI服务状态

### 分析服务

- `POST /api/analysis/analyze` - 分析单篇文章
- `POST /api/analysis/batch-analyze` - 批量分析文章
- `GET /api/analysis/sentiment-trend` - 获取情绪趋势

### 新闻服务

- `GET /api/news/latest` - 获取最新新闻
- `GET /api/news/search` - 搜索新闻
- `GET /api/news/categories` - 获取新闻分类

### 通知服务

- `POST /api/notifications/send` - 发送通知
- `GET /api/notifications/preferences/{user_id}` - 获取用户偏好
- `PUT /api/notifications/preferences/{user_id}` - 更新用户偏好

## 🚀 Vercel部署

### 1. 准备部署

确保项目根目录有正确的 `vercel.json` 配置：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/backend/app.py"
    }
  ]
}
```

### 2. 环境变量配置

在Vercel项目中设置以下环境变量：

- `HUNYUAN_API_KEY` - 腾讯混元API密钥
- `HUNYUAN_SECRET_ID` - 腾讯混元Secret ID
- `VERCEL=1` - 标识Vercel环境

### 3. 部署命令

```bash
# 安装Vercel CLI
npm i -g vercel

# 登录并部署
vercel login
vercel --prod
```

## 🔧 配置说明

### AI服务配置

系统支持多种AI服务提供商，当前主要配置腾讯混元：

```python
# 在ai_service.py中配置
providers = {
    'hunyuan': {
        'name': '腾讯混元',
        'base_url': 'https://hunyuan.cloud.tencent.com/hunyuan',
        'api_key': os.getenv('HUNYUAN_API_KEY'),
        'secret_id': os.getenv('HUNYUAN_SECRET_ID')
    }
}
```

### 通知渠道配置

系统支持三种通知渠道：

1. **Telegram**: 需要配置Bot Token
2. **企业微信**: 需要配置Corp ID、Secret和Agent ID
3. **邮件**: 需要配置SMTP服务器信息

## 🐛 故障排除

### 常见问题

1. **AI服务不可用**
   - 检查 `HUNYUAN_API_KEY` 和 `HUNYUAN_SECRET_ID` 配置
   - 验证网络连接和API配额

2. **邮件发送失败**
   - 检查SMTP服务器配置
   - 验证邮箱密码和授权码

3. **Vercel部署失败**
   - 检查 `vercel.json` 配置
   - 验证环境变量设置

### 日志查看

```bash
# 本地运行查看日志
tail -f nohup.out

# Vercel查看日志
vercel logs
```

## 📞 技术支持

如有问题请联系系统管理员或查看项目文档。

## 📄 许可证

本项目仅供学习和研究使用。

---

**版本**: 1.0.0  
**最后更新**: 2024-01-23