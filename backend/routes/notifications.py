import logging
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, Response

logger = logging.getLogger(__name__)

# 创建蓝图
notifications_bp = Blueprint('notifications', __name__)

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

# 模拟用户配置数据
MOCK_USER_CONFIGS = {
    'user1': {
        'preferences': {
            'telegram': {'enabled': True, 'priority': 'high'},
            'wechat_work': {'enabled': True, 'priority': 'medium'},
            'email': {'enabled': False, 'priority': 'low'}
        },
        'channels': ['telegram', 'wechat_work']
    },
    'user2': {
        'preferences': {
            'email': {'enabled': True, 'priority': 'high'},
            'telegram': {'enabled': False, 'priority': 'low'}
        },
        'channels': ['email']
    }
}

# 模拟通知历史
MOCK_NOTIFICATION_HISTORY = []

class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        self.channels = {
            'telegram': TelegramChannel(),
            'wechat_work': WechatWorkChannel(),
            'email': EmailChannel()
        }
    
    async def send_notification(self, user_id, message, priority='medium', channels=None):
        """发送通知"""
        try:
            user_config = MOCK_USER_CONFIGS.get(user_id, {})
            
            # 确定要使用的渠道
            target_channels = channels or user_config.get('channels', [])
            if not target_channels:
                target_channels = list(self.channels.keys())
            
            results = []
            successful_sends = 0
            
            for channel_name in target_channels:
                if channel_name not in self.channels:
                    results.append({
                        'channel': channel_name,
                        'success': False,
                        'error': '渠道不存在'
                    })
                    continue
                
                # 检查用户偏好
                channel_pref = user_config.get('preferences', {}).get(channel_name, {})
                if not channel_pref.get('enabled', True):
                    results.append({
                        'channel': channel_name,
                        'success': False,
                        'error': '渠道被用户禁用'
                    })
                    continue
                
                # 发送通知
                try:
                    channel_result = await self.channels[channel_name].send(
                        user_id, message, priority
                    )
                    if channel_result.get('success'):
                        successful_sends += 1
                    
                    results.append({
                        'channel': channel_name,
                        'success': channel_result.get('success', False),
                        'message': channel_result.get('message', ''),
                        'error': channel_result.get('error', '')
                    })
                    
                except Exception as channel_error:
                    results.append({
                        'channel': channel_name,
                        'success': False,
                        'error': str(channel_error)
                    })
            
            # 记录通知历史
            notification_record = {
                'id': len(MOCK_NOTIFICATION_HISTORY) + 1,
                'user_id': user_id,
                'message': message,
                'priority': priority,
                'channels_attempted': target_channels,
                'results': results,
                'successful_sends': successful_sends,
                'timestamp': datetime.now().isoformat(),
                'status': 'success' if successful_sends > 0 else 'failed'
            }
            
            MOCK_NOTIFICATION_HISTORY.append(notification_record)
            
            return {
                'success': successful_sends > 0,
                'data': notification_record,
                'message': f'成功通过{successful_sends}个渠道发送通知' if successful_sends > 0 else '通知发送失败'
            }
            
        except Exception as error:
            logger.error(f'发送通知错误: {str(error)}')
            return {
                'success': False,
                'error': str(error)
            }
    
    def get_user_preferences(self, user_id):
        """获取用户通知偏好"""
        return MOCK_USER_CONFIGS.get(user_id, {
            'preferences': {
                'telegram': {'enabled': True, 'priority': 'medium'},
                'wechat_work': {'enabled': True, 'priority': 'medium'},
                'email': {'enabled': True, 'priority': 'medium'}
            },
            'channels': ['telegram', 'wechat_work', 'email']
        })
    
    def update_user_preferences(self, user_id, preferences):
        """更新用户通知偏好"""
        if user_id not in MOCK_USER_CONFIGS:
            MOCK_USER_CONFIGS[user_id] = {'preferences': {}, 'channels': []}
        
        MOCK_USER_CONFIGS[user_id]['preferences'].update(preferences)
        
        # 更新启用的渠道列表
        enabled_channels = [
            channel for channel, pref in preferences.items() 
            if pref.get('enabled', False)
        ]
        MOCK_USER_CONFIGS[user_id]['channels'] = enabled_channels
        
        return {'success': True, 'message': '用户偏好更新成功'}
    
    def get_notification_history(self, user_id, limit=10):
        """获取用户通知历史"""
        user_history = [
            record for record in MOCK_NOTIFICATION_HISTORY 
            if record['user_id'] == user_id
        ]
        return user_history[-limit:] if limit > 0 else user_history
    
    def test_channel_connectivity(self, channel_name):
        """测试渠道连通性"""
        if channel_name not in self.channels:
            return {'success': False, 'error': '渠道不存在'}
        
        try:
            result = self.channels[channel_name].test_connectivity()
            return result
        except Exception as error:
            return {'success': False, 'error': str(error)}

class TelegramChannel:
    """Telegram渠道"""
    
    async def send(self, user_id, message, priority):
        """发送Telegram通知"""
        # 模拟Telegram API调用
        logger.info(f"📱 发送Telegram通知给用户 {user_id}: {message[:50]}...")
        
        # 模拟API调用结果
        return {
            'success': True,
            'message': 'Telegram通知发送成功',
            'channel': 'telegram'
        }
    
    def test_connectivity(self):
        """测试Telegram连通性"""
        return {
            'success': True,
            'message': 'Telegram渠道连接正常',
            'channel': 'telegram'
        }

class WechatWorkChannel:
    """企业微信渠道"""
    
    async def send(self, user_id, message, priority):
        """发送企业微信通知"""
        logger.info(f"💼 发送企业微信通知给用户 {user_id}: {message[:50]}...")
        
        # 模拟API调用结果
        return {
            'success': True,
            'message': '企业微信通知发送成功',
            'channel': 'wechat_work'
        }
    
    def test_connectivity(self):
        """测试企业微信连通性"""
        return {
            'success': True,
            'message': '企业微信渠道连接正常',
            'channel': 'wechat_work'
        }

class EmailChannel:
    """邮件渠道"""
    
    async def send(self, user_id, message, priority):
        """发送邮件通知"""
        logger.info(f"📧 发送邮件通知给用户 {user_id}: {message[:50]}...")
        
        # 模拟API调用结果
        return {
            'success': True,
            'message': '邮件通知发送成功',
            'channel': 'email'
        }
    
    def test_connectivity(self):
        """测试邮件连通性"""
        return {
            'success': True,
            'message': '邮件渠道连接正常',
            'channel': 'email'
        }

# 创建全局通知管理器实例
notification_manager = NotificationManager()

# 根路径路由
@notifications_bp.route('/', methods=['GET'])
def get_notifications_status():
    return jsonify_chinese({
        'service': '统一通知服务',
        'status': 'active',
        'endpoints': {
            'send': '/send - POST - 发送通知',
            'preferences': '/preferences - GET/PUT - 用户偏好管理',
            'history': '/history - GET - 通知历史',
            'test': '/test - POST - 测试渠道连通性'
        },
        'supported_channels': ['telegram', 'wechat_work', 'email'],
        'features': [
            '多渠道统一接口',
            '用户偏好设置',
            '优先级管理',
            '历史记录追踪',
            '连通性测试'
        ],
        'timestamp': datetime.now().isoformat()
    })

# 发送通知
@notifications_bp.route('/send', methods=['POST'])
async def send_notification():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        user_id = data.get('user_id')
        message = data.get('message')
        priority = data.get('priority', 'medium')
        channels = data.get('channels')
        
        if not user_id:
            return jsonify_chinese({'error': '请提供用户ID'}), 400
        if not message:
            return jsonify_chinese({'error': '请提供通知内容'}), 400
        
        # 验证优先级
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if priority not in valid_priorities:
            return jsonify_chinese({'error': f'优先级必须是: {", ".join(valid_priorities)}'}), 400
        
        # 发送通知
        result = await notification_manager.send_notification(user_id, message, priority, channels)
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 500
            
    except Exception as e:
        logger.error(f'发送通知错误: {str(e)}')
        return jsonify_chinese({'error': '发送通知失败', 'message': str(e)}), 500

# 获取用户偏好
@notifications_bp.route('/preferences/<user_id>', methods=['GET'])
def get_user_preferences(user_id):
    try:
        preferences = notification_manager.get_user_preferences(user_id)
        return jsonify_chinese({
            'success': True,
            'data': preferences,
            'message': '用户偏好获取成功'
        })
    except Exception as e:
        logger.error(f'获取用户偏好错误: {str(e)}')
        return jsonify_chinese({'error': '获取用户偏好失败', 'message': str(e)}), 500

# 更新用户偏好
@notifications_bp.route('/preferences/<user_id>', methods=['PUT'])
def update_user_preferences(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        result = notification_manager.update_user_preferences(user_id, data)
        return jsonify_chinese(result)
    except Exception as e:
        logger.error(f'更新用户偏好错误: {str(e)}')
        return jsonify_chinese({'error': '更新用户偏好失败', 'message': str(e)}), 500

# 获取通知历史
@notifications_bp.route('/history/<user_id>', methods=['GET'])
def get_notification_history(user_id):
    try:
        limit = int(request.args.get('limit', 10))
        history = notification_manager.get_notification_history(user_id, limit)
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'history': history,
                'total_count': len(history)
            },
            'message': '通知历史获取成功'
        })
    except ValueError as e:
        return jsonify_chinese({'error': '参数格式错误', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f'获取通知历史错误: {str(e)}')
        return jsonify_chinese({'error': '获取通知历史失败', 'message': str(e)}), 500

# 测试渠道连通性
@notifications_bp.route('/test', methods=['POST'])
def test_channel_connectivity():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请提供JSON格式的请求体'}), 400
        
        channel_name = data.get('channel')
        if not channel_name:
            return jsonify_chinese({'error': '请提供渠道名称'}), 400
        
        result = notification_manager.test_channel_connectivity(channel_name)
        
        if result['success']:
            return jsonify_chinese(result)
        else:
            return jsonify_chinese(result), 500
            
    except Exception as e:
        logger.error(f'测试渠道连通性错误: {str(e)}')
        return jsonify_chinese({'error': '测试渠道连通性失败', 'message': str(e)}), 500

# 获取所有渠道状态
@notifications_bp.route('/channels', methods=['GET'])
def get_channels_status():
    try:
        channels_status = {}
        for channel_name in ['telegram', 'wechat_work', 'email']:
            result = notification_manager.test_channel_connectivity(channel_name)
            channels_status[channel_name] = result
        
        return jsonify_chinese({
            'success': True,
            'data': channels_status,
            'message': '渠道状态获取成功'
        })
    except Exception as e:
        logger.error(f'获取渠道状态错误: {str(e)}')
        return jsonify_chinese({'error': '获取渠道状态失败', 'message': str(e)}), 500