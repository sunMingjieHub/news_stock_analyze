import logging
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, Response

logger = logging.getLogger(__name__)

# 创建蓝图
wechat_work_bp = Blueprint('wechat_work', __name__)

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

class WechatWorkService:
    """企业微信服务类"""
    
    def __init__(self):
        self.corp_id = 'your_corp_id'  # 企业ID
        self.corp_secret = 'your_corp_secret'  # 应用Secret
        self.agent_id = 'your_agent_id'  # 应用AgentId
        
        # 模拟访问令牌（实际需要从API获取）
        self.access_token = None
        self.token_expire_time = None
        
        # 模拟部门数据
        self.departments = {
            '1': {'name': '技术部', 'parent_id': '0'},
            '2': {'name': '市场部', 'parent_id': '0'},
            '3': {'name': '研发组', 'parent_id': '1'}
        }
        
        # 模拟用户数据
        self.users = {
            'user1': {
                'userid': 'zhangsan',
                'name': '张三',
                'department': ['1'],
                'position': '工程师',
                'mobile': '13800138000',
                'email': 'zhangsan@company.com'
            },
            'user2': {
                'userid': 'lisi',
                'name': '李四',
                'department': ['2'],
                'position': '市场经理',
                'mobile': '13900139000',
                'email': 'lisi@company.com'
            }
        }
        
        # 消息模板
        self.templates = {
            'stock_alert': {
                'title': '股票预警通知',
                'description': '股票{stock_name}触发了预警条件',
                'url': 'https://your-domain.com/alerts/{alert_id}',
                'btntxt': '查看详情'
            },
            'market_report': {
                'title': '市场日报',
                'description': '{date}市场行情报告',
                'url': 'https://your-domain.com/reports/{date}',
                'btntxt': '查看报告'
            },
            'system_notice': {
                'title': '系统通知',
                'description': '{message}',
                'url': '',
                'btntxt': '知道了'
            }
        }
    
    async def get_access_token(self):
        """获取访问令牌"""
        try:
            # 模拟获取访问令牌（实际需要调用企业微信API）
            if self.access_token and self.token_expire_time and datetime.now() < self.token_expire_time:
                return self.access_token
            
            # 模拟API调用
            logger.info("获取企业微信访问令牌")
            self.access_token = 'mock_access_token_123456'
            self.token_expire_time = datetime.now().timestamp() + 7200  # 2小时
            
            return self.access_token
            
        except Exception as e:
            logger.error(f"获取访问令牌失败: {str(e)}")
            raise e
    
    def test_connectivity(self):
        """测试企业微信API连通性"""
        try:
            # 模拟连通性测试
            logger.info("测试企业微信API连通性")
            return {
                'success': True,
                'message': '企业微信API连接正常',
                'corp_id': self.corp_id,
                'agent_id': self.agent_id,
                'active_users': len(self.users),
                'departments': len(self.departments)
            }
        except Exception as e:
            logger.error(f"企业微信API连接测试失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def send_text_message(self, to_user, to_party, to_tag, content):
        """发送文本消息"""
        try:
            await self.get_access_token()  # 确保有有效的访问令牌
            
            # 模拟发送消息（实际需要调用企业微信API）
            logger.info(f"💼 发送企业微信消息: {content[:50]}...")
            logger.info(f"接收人: {to_user}, 部门: {to_party}, 标签: {to_tag}")
            
            # 实际发送代码：
            # import requests
            # url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
            # payload = {
            #     "touser": to_user,
            #     "toparty": to_party,
            #     "totag": to_tag,
            #     "msgtype": "text",
            #     "agentid": self.agent_id,
            #     "text": {"content": content},
            #     "safe": 0
            # }
            # response = requests.post(url, json=payload)
            # response.raise_for_status()
            
            return {
                'success': True,
                'message': '企业微信消息发送成功',
                'to_user': to_user,
                'to_party': to_party,
                'to_tag': to_tag,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"发送企业微信消息失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def send_template_message(self, template_name, template_data, to_user='', to_party='', to_tag=''):
        """使用模板发送消息"""
        try:
            if template_name not in self.templates:
                return {'success': False, 'error': '模板不存在'}
            
            template = self.templates[template_name]
            
            # 构建消息内容
            title = template['title'].format(**template_data)
            description = template['description'].format(**template_data)
            url = template['url'].format(**template_data) if template['url'] else ''
            btntxt = template['btntxt']
            
            await self.get_access_token()
            
            # 模拟发送模板消息
            logger.info(f"💼 发送企业微信模板消息: {title}")
            
            # 实际发送代码（文本卡片消息）：
            # payload = {
            #     "touser": to_user,
            #     "toparty": to_party,
            #     "totag": to_tag,
            #     "msgtype": "textcard",
            #     "agentid": self.agent_id,
            #     "textcard": {
            #         "title": title,
            #         "description": description,
            #         "url": url,
            #         "btntxt": btntxt
            #     }
            # }
            
            return {
                'success': True,
                'message': '企业微信模板消息发送成功',
                'template': template_name,
                'to_user': to_user,
                'to_party': to_party,
                'to_tag': to_tag,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"发送企业微信模板消息失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_user_info(self, user_id):
        """获取用户信息"""
        user = self.users.get(user_id)
        if not user:
            return {'success': False, 'error': '用户不存在'}
        
        return {
            'success': True,
            'data': user,
            'message': '用户信息获取成功'
        }
    
    def get_department_list(self):
        """获取部门列表"""
        return {
            'success': True,
            'data': {
                'departments': self.departments,
                'count': len(self.departments)
            },
            'message': '部门列表获取成功'
        }
    
    def get_department_users(self, department_id):
        """获取部门用户列表"""
        department_users = []
        for user_id, user_info in self.users.items():
            if department_id in user_info.get('department', []):
                department_users.append(user_info)
        
        return {
            'success': True,
            'data': {
                'users': department_users,
                'count': len(department_users)
            },
            'message': f'部门{department_id}用户列表获取成功'
        }
    
    async def broadcast_message(self, message, department_id=None):
        """广播消息给所有用户或特定部门"""
        try:
            target_users = []
            
            if department_id:
                # 发送给特定部门
                dept_users = self.get_department_users(department_id)
                if dept_users['success']:
                    target_users = dept_users['data']['users']
            else:
                # 发送给所有用户
                target_users = list(self.users.values())
            
            results = []
            successful_sends = 0
            
            for user in target_users:
                result = await self.send_text_message(
                    to_user=user['userid'],
                    to_party='',
                    to_tag='',
                    content=message
                )
                
                if result['success']:
                    successful_sends += 1
                
                results.append({
                    'userid': user['userid'],
                    'name': user['name'],
                    'success': result['success'],
                    'error': result.get('error')
                })
            
            return {
                'success': successful_sends > 0,
                'data': {
                    'total_users': len(target_users),
                    'successful_sends': successful_sends,
                    'failed_sends': len(target_users) - successful_sends,
                    'results': results
                },
                'message': f'广播完成，成功发送给{successful_sends}个用户'
            }
            
        except Exception as e:
            logger.error(f"广播消息失败: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_available_templates(self):
        """获取可用模板"""
        return list(self.templates.keys())

# 创建全局企业微信服务实例
wechat_work_service = WechatWorkService()

# 根路径路由
@wechat_work_bp.route('/', methods=['GET'])
def get_wechat_work_status():
    return jsonify_chinese({
        'service': '企业微信机器人服务',
        'status': 'active',
        'endpoints': {
            'send': '/send - POST - 发送消息',
            'broadcast': '/broadcast - POST - 广播消息',
            'users': '/users - GET - 用户管理',
            'departments': '/departments - GET - 部门管理',
            'test': '/test - GET - 测试服务'
        },
        'features': [
            '文本消息发送',
            '模板消息推送',
            '部门广播',
            '用户管理',
            '访问令牌管理'
        ],
        'available_templates': wechat_work_service.get_available_templates(),
        'active_users': len(wechat_work_service.users),
        'departments': len(wechat_work_service.departments),
        'timestamp': datetime.now().isoformat()
    })

# 发送消息
@wechat_work_bp.route('/send', methods=['POST'])
async def send_wechat_work_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        to_user = data.get('to_user', '')
        to_party = data.get('to_party', '')
        to_tag = data.get('to_tag', '')
        content = data.get('content')
        template_name = data.get('template_name')
        template_data = data.get('template_data', {})
        
        # 参数验证
        if not to_user and not to_party and not to_tag:
            return jsonify_chinese({'error': '请提供接收人(to_user)、部门(to_party)或标签(to_tag)'}), 400
        if not content and not template_name:
            return jsonify_chinese({'error': '请提供消息内容或模板名称'}), 400
        
        # 使用模板发送
        if template_name:
            result = await wechat_work_service.send_template_message(
                template_name, template_data, to_user, to_party, to_tag
            )
        else:
            # 直接发送文本消息
            result = await wechat_work_service.send_text_message(
                to_user, to_party, to_tag, content
            )
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 500
            
    except Exception as e:
        logger.error(f'发送企业微信消息错误: {str(e)}')
        return jsonify_chinese({'error': '发送企业微信消息失败', 'message': str(e)}), 500

# 广播消息
@wechat_work_bp.route('/broadcast', methods=['POST'])
async def broadcast_wechat_work_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        message = data.get('message')
        department_id = data.get('department_id')
        
        if not message:
            return jsonify_chinese({'error': '请提供广播消息内容'}), 400
        
        result = await wechat_work_service.broadcast_message(message, department_id)
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 500
            
    except Exception as e:
        logger.error(f'广播企业微信消息错误: {str(e)}')
        return jsonify_chinese({'error': '广播企业微信消息失败', 'message': str(e)}), 500

# 测试服务
@wechat_work_bp.route('/test', methods=['GET'])
def test_wechat_work_service():
    try:
        result = wechat_work_service.test_connectivity()
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 500
            
    except Exception as e:
        logger.error(f'测试企业微信服务错误: {str(e)}')
        return jsonify_chinese({'error': '测试企业微信服务失败', 'message': str(e)}), 500

# 获取用户信息
@wechat_work_bp.route('/users/<user_id>', methods=['GET'])
def get_user_info(user_id):
    try:
        result = wechat_work_service.get_user_info(user_id)
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 404
            
    except Exception as e:
        logger.error(f'获取用户信息错误: {str(e)}')
        return jsonify_chinese({'error': '获取用户信息失败', 'message': str(e)}), 500

# 获取部门列表
@wechat_work_bp.route('/departments', methods=['GET'])
def get_department_list():
    try:
        result = wechat_work_service.get_department_list()
        return jsonify_chinese(result)
        
    except Exception as e:
        logger.error(f'获取部门列表错误: {str(e)}')
        return jsonify_chinese({'error': '获取部门列表失败', 'message': str(e)}), 500

# 获取部门用户
@wechat_work_bp.route('/departments/<department_id>/users', methods=['GET'])
def get_department_users(department_id):
    try:
        result = wechat_work_service.get_department_users(department_id)
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 404
            
    except Exception as e:
        logger.error(f'获取部门用户错误: {str(e)}')
        return jsonify_chinese({'error': '获取部门用户失败', 'message': str(e)}), 500

# 获取所有用户
@wechat_work_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = []
        for user_id, user_info in wechat_work_service.users.items():
            users.append({
                'user_id': user_id,
                'userid': user_info.get('userid'),
                'name': user_info.get('name'),
                'department': user_info.get('department', []),
                'position': user_info.get('position')
            })
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'users': users,
                'total_count': len(users)
            },
            'message': '用户列表获取成功'
        })
        
    except Exception as e:
        logger.error(f'获取用户列表错误: {str(e)}')
        return jsonify_chinese({'error': '获取用户列表失败', 'message': str(e)}), 500

# 获取模板列表
@wechat_work_bp.route('/templates', methods=['GET'])
def get_templates():
    try:
        templates = wechat_work_service.get_available_templates()
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'templates': templates,
                'count': len(templates)
            },
            'message': '模板列表获取成功'
        })
        
    except Exception as e:
        logger.error(f'获取模板列表错误: {str(e)}')
        return jsonify_chinese({'error': '获取模板列表失败', 'message': str(e)}), 500