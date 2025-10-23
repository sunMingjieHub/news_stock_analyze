import os
import logging
import json
from datetime import datetime
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['JSON_AS_ASCII'] = False  # 确保中文正确显示
app.config['JSON_SORT_KEYS'] = False  # 保持JSON键的顺序
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # 美化JSON输出
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'  # 明确指定字符集

# 启用CORS
CORS(app)

# Vercel环境检测
IS_VERCEL = os.getenv('VERCEL') == '1'
PORT = int(os.getenv('PORT', 3001))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 自定义JSON响应函数，确保中文正确编码
def jsonify_chinese(*args, **kwargs):
    """返回中文编码正确的JSON响应"""
    if args and kwargs:
        raise TypeError('jsonify() takes either args or kwargs, not both')
    elif len(args) == 1:
        data = args[0]
    else:
        data = args or kwargs
    
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )

# 自定义JSON响应装饰器，确保中文正确编码
def ensure_chinese_response(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if hasattr(response, 'headers'):
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    wrapper.__name__ = func.__name__
    return wrapper

# Vercel环境特殊处理：添加请求日志
@app.before_request
def log_request_info():
    if IS_VERCEL:
        logger.info(f"📥 Vercel请求: {request.method} {request.path}")

# 导入路由蓝图
from routes.news import news_bp
from routes.analysis import analysis_bp
from routes.wechat_work import wechat_work_bp
from routes.email import email_bp
from routes.notifications import notifications_bp

# 注册蓝图
app.register_blueprint(news_bp, url_prefix='/api/news')
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(wechat_work_bp, url_prefix='/api/wechat-work')
app.register_blueprint(email_bp, url_prefix='/api/email')
app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

# 健康检查端点
@app.route('/health', methods=['GET'])
@ensure_chinese_response
def health_check():
    return jsonify_chinese({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'notification_channels': ['wechat_work', 'email']
    })

# 根路径 - 返回健康检查信息
@app.route('/', methods=['GET'])
@ensure_chinese_response
def root():
    return jsonify_chinese({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'notification_channels': ['wechat_work', 'email'],
        'message': '股票新闻分析系统后端服务 - 健康状态',
        'endpoints': {
            'news': '/api/news',
            'analysis': '/api/analysis',
            'wechat_work': '/api/wechat-work',
            'email': '/api/email',
            'notifications': '/api/notifications',
            'health': '/health'
        }
    })

# 错误处理中间件
@app.errorhandler(Exception)
@ensure_chinese_response
def handle_error(error):
    logger.error(f'Error: {error}')
    return jsonify_chinese({
        'error': '内部服务器错误',
        'message': '请联系系统管理员' if os.getenv('NODE_ENV') != 'development' else str(error)
    }), 500

# 404处理
@app.errorhandler(404)
@ensure_chinese_response
def not_found(error):
    logger.error(f'❌ 404错误: 请求路径 {request.path} 不存在')
    return jsonify_chinese({
        'error': '接口不存在',
        'available_endpoints': [
            '/api/news',
            '/api/analysis',
            '/api/wechat-work',
            '/api/email',
            '/api/notifications',
            '/health'
        ],
        'request_path': request.path,
        'environment': 'vercel' if IS_VERCEL else 'local'
    }), 404

# 只在非Vercel环境启动服务器（本地开发）
if __name__ == '__main__' and not IS_VERCEL:
    logger.info(f"🚀 服务器运行在端口 {PORT}")
    logger.info(f"🌐 环境: {'Vercel生产环境' if IS_VERCEL else '本地开发环境'}")
    logger.info("📊 股票新闻分析系统后端服务已启动")
    logger.info("🔔 通知系统支持: Telegram, 企业微信, 邮箱")
    logger.info(f"🔗 访问 http://localhost:{PORT} 查看API文档")
    
    app.run(host='0.0.0.0', port=PORT, debug=os.getenv('NODE_ENV') == 'development')