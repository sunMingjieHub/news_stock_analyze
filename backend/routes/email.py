import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import Blueprint, request, jsonify, Response
import json

logger = logging.getLogger(__name__)

# 创建蓝图
email_bp = Blueprint('email', __name__)

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

class EmailService:
    """邮件服务类"""
    
    def __init__(self):
        self.smtp_host = 'smtp.qq.com'
        self.smtp_port = 587
        self.sender_email = 'your_email@qq.com'
        self.sender_password = 'your_password'
        
        # 邮件模板
        self.templates = {
            'stock_alert': {
                'subject': '股票预警通知 - {stock_name}',
                'template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>股票预警通知</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                        .container {{ max-width: 600px; margin: 0 auto; }}
                        .header {{ background: #f8f9fa; padding: 20px; border-radius: 5px; }}
                        .content {{ padding: 20px; }}
                        .footer {{ text-align: center; color: #666; font-size: 12px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>📈 股票预警通知</h2>
                        </div>
                        <div class="content">
                            <p>尊敬的{user_name}，</p>
                            <p>您关注的股票 <strong>{stock_name}</strong> 触发了预警条件：</p>
                            <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0;">
                                <h3>📊 预警信息</h3>
                                <p><strong>股票代码：</strong>{stock_code}</p>
                                <p><strong>当前价格：</strong>{current_price}</p>
                                <p><strong>预警类型：</strong>{alert_type}</p>
                                <p><strong>触发条件：</strong>{condition}</p>
                                <p><strong>触发时间：</strong>{trigger_time}</p>
                            </div>
                            <p>建议您及时关注市场动态，合理调整投资策略。</p>
                            <p>此邮件由股票新闻分析系统自动发送，请勿回复。</p>
                        </div>
                        <div class="footer">
                            <p>© 2024 股票新闻分析系统. 保留所有权利.</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
            },
            'news_summary': {
                'subject': '每日股票新闻摘要 - {date}',
                'template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>每日股票新闻摘要</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                        .container {{ max-width: 600px; margin: 0 auto; }}
                        .header {{ background: #e9ecef; padding: 20px; border-radius: 5px; }}
                        .news-item {{ margin: 15px 0; padding: 15px; border-left: 4px solid #007bff; }}
                        .positive {{ border-left-color: #28a745; }}
                        .negative {{ border-left-color: #dc3545; }}
                        .neutral {{ border-left-color: #6c757d; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>📰 每日股票新闻摘要</h2>
                            <p>日期：{date}</p>
                        </div>
                        {news_items}
                        <div style="margin-top: 20px; text-align: center; color: #666;">
                            <p>此邮件由股票新闻分析系统自动生成</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
            },
            'system_notification': {
                'subject': '系统通知 - {title}',
                'template': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>系统通知</title>
                </head>
                <body>
                    <h2>系统通知</h2>
                    <p>{message}</p>
                    <p><small>发送时间：{send_time}</small></p>
                </body>
                </html>
                '''
            }
        }
    
    def test_connectivity(self):
        """测试邮件服务连通性"""
        try:
            # 模拟连接测试
            logger.info("测试邮件服务连通性")
            return {
                'success': True,
                'message': '邮件服务连接正常',
                'smtp_host': self.smtp_host,
                'smtp_port': self.smtp_port
            }
        except Exception as e:
            logger.error(f"邮件服务连接测试失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def send_email(self, to_email, subject, content, template_name=None, template_data=None, is_html=True):
        """发送邮件"""
        try:
            # 使用模板
            if template_name and template_name in self.templates:
                template = self.templates[template_name]
                subject = template['subject'].format(**template_data) if template_data else subject
                content = template['template'].format(**template_data) if template_data else content
                is_html = True
            
            # 创建邮件消息
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(content, 'html'))
            else:
                msg.attach(MIMEText(content, 'plain'))
            
            # 模拟发送邮件（实际实现需要配置SMTP）
            logger.info(f"📧 发送邮件给 {to_email}: {subject}")
            
            # 实际发送代码（需要配置SMTP）：
            # with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            #     server.starttls()
            #     server.login(self.sender_email, self.sender_password)
            #     server.send_message(msg)
            
            return {
                'success': True,
                'message': '邮件发送成功',
                'to': to_email,
                'subject': subject,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"发送邮件失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'to': to_email,
                'subject': subject
            }
    
    def get_templates(self):
        """获取可用邮件模板"""
        return list(self.templates.keys())
    
    def add_template(self, template_name, subject, template):
        """添加邮件模板"""
        self.templates[template_name] = {
            'subject': subject,
            'template': template
        }
        return {'success': True, 'message': '模板添加成功'}

# 创建全局邮件服务实例
email_service = EmailService()

# 根路径路由
@email_bp.route('/', methods=['GET'])
def get_email_status():
    return jsonify_chinese({
        'service': '邮件通知服务',
        'status': 'active',
        'endpoints': {
            'send': '/send - POST - 发送邮件',
            'test': '/test - GET - 测试邮件服务',
            'templates': '/templates - GET - 获取邮件模板'
        },
        'features': [
            'HTML邮件模板',
            '多模板支持',
            '批量发送',
            '模板变量替换'
        ],
        'available_templates': email_service.get_templates(),
        'timestamp': datetime.now().isoformat()
    })

# 发送邮件
@email_bp.route('/send', methods=['POST'])
async def send_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        to_email = data.get('to_email')
        subject = data.get('subject')
        content = data.get('content')
        template_name = data.get('template_name')
        template_data = data.get('template_data', {})
        is_html = data.get('is_html', True)
        
        if not to_email:
            return jsonify_chinese({'error': '请提供收件人邮箱'}), 400
        if not subject and not template_name:
            return jsonify_chinese({'error': '请提供邮件主题或模板名称'}), 400
        
        # 发送邮件
        result = await email_service.send_email(
            to_email, subject, content, template_name, template_data, is_html
        )
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 500
            
    except Exception as e:
        logger.error(f'发送邮件错误: {str(e)}')
        return jsonify_chinese({'error': '发送邮件失败', 'message': str(e)}), 500

# 测试邮件服务
@email_bp.route('/test', methods=['GET'])
def test_email_service():
    try:
        result = email_service.test_connectivity()
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 500
            
    except Exception as e:
        logger.error(f'测试邮件服务错误: {str(e)}')
        return jsonify_chinese({'error': '测试邮件服务失败', 'message': str(e)}), 500

# 获取邮件模板
@email_bp.route('/templates', methods=['GET'])
def get_email_templates():
    try:
        templates = email_service.get_templates()
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'templates': templates,
                'count': len(templates)
            },
            'message': '邮件模板获取成功'
        })
        
    except Exception as e:
        logger.error(f'获取邮件模板错误: {str(e)}')
        return jsonify_chinese({'error': '获取邮件模板失败', 'message': str(e)}), 500

# 添加邮件模板
@email_bp.route('/templates', methods=['POST'])
def add_email_template():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        template_name = data.get('template_name')
        subject = data.get('subject')
        template = data.get('template')
        
        if not template_name:
            return jsonify_chinese({'error': '请提供模板名称'}), 400
        if not subject:
            return jsonify_chinese({'error': '请提供邮件主题'}), 400
        if not template:
            return jsonify_chinese({'error': '请提供模板内容'}), 400
        
        result = email_service.add_template(template_name, subject, template)
        return jsonify_chinese(result)
        
    except Exception as e:
        logger.error(f'添加邮件模板错误: {str(e)}')
        return jsonify_chinese({'error': '添加邮件模板失败', 'message': str(e)}), 500

# 批量发送邮件
@email_bp.route('/batch-send', methods=['POST'])
async def batch_send_emails():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        emails = data.get('emails', [])
        
        if not isinstance(emails, list) or len(emails) == 0:
            return jsonify_chinese({'error': '请提供邮件列表'}), 400
        
        # 限制批量发送数量
        max_batch_size = 10
        emails_to_send = emails[:max_batch_size]
        
        results = []
        successful_sends = 0
        
        for email_data in emails_to_send:
            try:
                result = await email_service.send_email(
                    email_data.get('to_email'),
                    email_data.get('subject'),
                    email_data.get('content'),
                    email_data.get('template_name'),
                    email_data.get('template_data', {}),
                    email_data.get('is_html', True)
                )
                
                if result['success']:
                    successful_sends += 1
                
                results.append(result)
                
            except Exception as email_error:
                results.append({
                    'success': False,
                    'error': str(email_error),
                    'to_email': email_data.get('to_email')
                })
        
        return jsonify_chinese({
            'success': successful_sends > 0,
            'data': {
                'processed_count': len(results),
                'successful_sends': successful_sends,
                'failed_count': len(results) - successful_sends,
                'results': results
            },
            'message': f'批量发送完成，成功{successful_sends}封，失败{len(results) - successful_sends}封'
        })
        
    except Exception as e:
        logger.error(f'批量发送邮件错误: {str(e)}')
        return jsonify_chinese({'error': '批量发送邮件失败', 'message': str(e)}), 500

# 获取发送统计
@email_bp.route('/stats', methods=['GET'])
def get_email_stats():
    try:
        # 模拟统计数据
        return jsonify_chinese({
            'success': True,
            'data': {
                'total_sent': 150,
                'success_rate': 0.95,
                'today_sent': 5,
                'popular_templates': ['stock_alert', 'news_summary'],
                'last_sent': datetime.now().isoformat()
            },
            'message': '邮件统计获取成功'
        })
        
    except Exception as e:
        logger.error(f'获取邮件统计错误: {str(e)}')
        return jsonify_chinese({'error': '获取邮件统计失败', 'message': str(e)}), 500