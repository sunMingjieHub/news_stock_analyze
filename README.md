# 📈 智能股票投资理财系统

一个基于AI分析的智能股票投资系统，集成新闻爬取、情绪分析、多渠道通知等功能。

## ✨ 核心功能

### 1. 智能新闻爬取与分析
- 实时爬取多家财经媒体最新新闻
- **国内AI服务**自动分析文章内容和市场情绪
- 技术指标关联和投资建议生成

### 2. 多渠道通知系统（**新增重点**）
- **企业微信机器人**：实时推送、团队协作
- **邮箱通知**：详细报告、归档记录
- **智能路由**：根据优先级自动选择最优渠道

### 3. 多AI服务支持（**新增**）
- **DeepSeek**：性价比高，响应速度快
- **智谱AI**：中文理解能力强，财经分析专业
- **腾讯混元**：企业级稳定性，安全可靠
- **元宝AI**：新兴服务，功能丰富
- **百川AI**：技术实力强，多模态支持
- **智能降级**：自动切换最优可用服务

### 4. 自动化工作流
- GitHub Actions定时执行分析任务
- Vercel免费后端托管
- GitHub Pages前端展示

## 🚀 快速开始

### 环境要求
- **Python 3.8+**
- **至少一个国内AI服务API密钥**（推荐DeepSeek或智谱AI）
- 企业微信账号或邮箱账号

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd stock
```

2. **安装依赖**
```bash
# 后端依赖（Python）
cd backend && pip install -r requirements.txt

# 前端依赖（如果使用前端）
cd ../frontend && npm install
```

3. **配置环境变量**
```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，填写实际配置
```

4. **启动服务**
```bash
# 启动后端（端口3001）
cd backend && python run.py

# 或使用Flask命令行
cd backend && flask run --port=3001

# 启动前端（端口3000，如果使用前端）
cd frontend && npm run dev
```

## 🤖 AI服务配置（重点）

### 推荐AI服务商

**优先级推荐：**
1. **DeepSeek** - 免费额度充足，响应速度快
2. **智谱AI** - 中文理解强，财经分析专业  
3. **腾讯混元** - 企业级稳定性
4. **元宝AI** - 新兴服务，功能丰富
5. **百川AI** - 技术实力强

### 配置方法

1. **选择至少一个AI服务商**并申请API密钥
2. **配置环境变量**：
```env
# DeepSeek (推荐)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 智谱AI (推荐)
ZHIPU_API_KEY=your_zhipu_api_key_here

# 腾讯混元
HUNYUAN_API_KEY=your_hunyuan_api_key_here
HUNYUAN_SECRET_ID=your_hunyuan_secret_id_here

# 元宝AI
YUANBAO_API_KEY=your_yuanbao_api_key_here

# 百川AI
BAICHUAN_API_KEY=your_baichuan_api_key_here
```

3. **测试AI服务连接**：
```bash
curl -X GET http://localhost:3001/api/analysis/ai-status
```

### AI服务优势

- **智能选择**：自动检测并选择最优服务商
- **自动降级**：主要服务不可用时自动切换
- **性能优化**：内容截断、并发控制、超时重试
- **成本控制**：多服务商分摊，避免单点依赖

## 📧 通知系统配置（重点）

### 企业微信机器人配置

1. **创建企业微信机器人**
   - 登录企业微信管理后台
   - 创建自定义应用，获取Webhook URL

2. **环境变量配置**
```env
# 方式1：使用Webhook URL（推荐）
WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key

# 方式2：使用Bot Key
WECHAT_BOT_KEY=your_bot_key
```

### 邮箱通知配置

1. **准备邮箱账号**
   - 支持QQ邮箱、163邮箱、Gmail等
   - 获取SMTP授权码

2. **环境变量配置**
```env
# QQ邮箱示例
SMTP_HOST=smtp.qq.com
SMTP_PORT=587
SMTP_USERNAME=your_email@qq.com
SMTP_PASSWORD=your_smtp_code
```

### 测试通知功能

```bash
# 测试所有通知渠道
python backend/test_app.py

# 或使用curl测试
curl -X POST http://localhost:3001/api/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "message": "测试消息",
    "analysis_result": "测试分析",
    "channels": ["all"]
  }'
```

## 🏗️ 系统架构

```
前端 (GitHub Pages)
    ↓
API网关 (Vercel)
    ↓
后端服务 (Python Flask)
    ├── 新闻爬取模块
    ├── AI分析模块（多服务商支持）
    │   ├── DeepSeek AI
    │   ├── 智谱AI
    │   ├── 腾讯混元
    │   ├── 元宝AI
    │   └── 百川AI
    ├── 通知管理模块
    │   ├── 企业微信机器人
    │   ├── 邮箱通知
    │   └── 智能路由
    └── 数据存储 (Notion)
```

## 🔧 API接口

### AI分析接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/analysis/analyze` | POST | 分析单个文章内容 |
| `/api/analysis/batch-analyze` | POST | 批量分析多篇文章 |
| `/api/analysis/ai-status` | GET | 查询AI服务状态 |

### 通知相关接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/notifications/send` | POST | 统一发送通知（智能路由） |
| `/api/wechat-work/broadcast` | POST | 发送企业微信消息 |
| `/api/email/broadcast` | POST | 发送邮件通知 |
| `/api/wechat-work/test` | GET | 测试企业微信连接 |
| `/api/email/test` | GET | 测试邮箱连接 |

### 使用示例

```python
# Python示例
import requests

# AI分析接口
analysis_response = requests.post('http://localhost:3001/api/analysis/analyze', 
    json={
        'content': '财经新闻内容...',
        'title': '新闻标题',
        'source_credibility': 0.8
    }
)

# 统一通知接口（推荐）
notification_response = requests.post('http://localhost:3001/api/notifications/send',
    json={
        'message': '📈 重要市场分析',
        'analysis_result': '技术指标显示买入信号...',
        'channels': ['wechat_work', 'email'],
        'priority': 'high'
    }
)
```

## 📊 功能特性

### 国内AI服务优势
- ✅ **本地化服务**：国内网络访问稳定
- ✅ **中文优化**：对中文内容理解更准确
- ✅ **成本可控**：多种计费方式选择
- ✅ **合规安全**：符合国内数据安全要求

### 企业微信机器人优势
- ✅ **实时性强**：秒级消息推送
- ✅ **团队协作**：支持@提及和群聊
- ✅ **移动友好**：企业微信App即时接收
- ✅ **格式丰富**：支持Markdown和文本

### 邮箱通知优势  
- ✅ **内容详细**：支持HTML富文本
- ✅ **归档记录**：便于后续查阅
- ✅ **可靠性高**：邮件服务稳定性好
- ✅ **附件支持**：可发送图表和分析报告

### 智能路由特性
- 🧠 **自动选择**：根据渠道性能智能路由
- 🔄 **失败重试**：自动切换到备用渠道
- 📈 **性能统计**：实时监控各渠道成功率
- ⚡ **优先级处理**：重要消息优先发送

## 🛠️ 部署指南

### Vercel部署（Python Flask）
1. 连接GitHub仓库到Vercel
2. 配置环境变量（确保包含Python相关配置）
3. 自动部署完成（Vercel会自动识别Python项目）

### GitHub Actions配置
```yaml
name: Daily Stock Analysis
on:
  schedule:
    - cron: '0 9 * * *'  # 每天9点执行
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run Analysis
        run: |
          curl -X POST $VERCEL_URL/api/analysis/run-daily \
            -H "Authorization: Bearer $SECRET_TOKEN"
```

## 🔍 监控与调试

### 查看AI服务状态
```bash
curl -X GET http://localhost:3001/api/analysis/ai-status
```

### 查看渠道性能
```bash
curl -X GET http://localhost:3001/api/notifications/stats
```

### 测试脚本
```bash
# 全面测试后端功能
cd backend && python test_app.py

# 测试AI分析功能
curl -X POST http://localhost:3001/api/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{"content":"测试文章内容"}'

# 单独测试企业微信
curl -X GET http://localhost:3001/api/wechat-work/test

# 单独测试邮箱
curl -X GET http://localhost:3001/api/email/test
```

## 📖 详细文档

- [后端部署指南](backend/README.md) - Python Flask后端详细说明
- [AI服务配置指南](AI_SERVICE_GUIDE.md) - 详细的AI服务配置说明
- [架构设计](ARCHITECTURE.md) - 系统架构和技术选型
- [通知系统使用指南](NOTIFICATION_GUIDE.md) - 详细的通知配置说明
- [部署检查清单](DEPLOYMENT_CHECKLIST.md) - 部署前的检查项目

## 🐛 故障排除

### 常见问题

**Q: AI服务不可用**
A: 检查API密钥配置，使用 `/api/analysis/ai-status` 查看服务状态

**Q: 企业微信消息发送失败**
A: 检查Webhook URL格式和机器人权限设置

**Q: 邮箱认证失败**  
A: 确认SMTP授权码是否正确，检查邮箱服务商设置

**Q: 通知没有收到**
A: 使用测试脚本验证各渠道连通性

**Q: Python依赖安装失败**
A: 确保Python版本为3.8+，检查requirements.txt文件

### Python特定问题

**Q: Flask应用启动失败**
A: 检查Python环境，确保所有依赖包正确安装

**Q: 模块导入错误**
A: 确保在backend目录下运行，或设置正确的Python路径

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

MIT License

## 📞 支持

如有问题，请提交Issue或参考详细文档。

---
*最后更新: 2024-10-23*  
*版本: v4.0 - Python Flask后端重构*