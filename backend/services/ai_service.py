import os
import logging
import asyncio
import aiohttp
import hashlib
import hmac
import time
import json
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AIServiceManager:
    """
    国内AI服务管理器
    支持：混元、元宝、DeepSeek等主流国内AI接口
    """
    
    def __init__(self):
        self.providers = {
            'hunyuan': {
                'name': '腾讯混元',
                'base_url': 'https://hunyuan.cloud.tencent.com/hunyuan',
                'api_key': os.getenv('HUNYUAN_API_KEY'),
                'secret_id': os.getenv('HUNYUAN_SECRET_ID'),
                'available': False,
                'last_error': None
            }
        }
        
        self.current_provider = None
        self.fallback_order = ['hunyuan']
        self._initialized = False
        
    async def initialize_providers(self):
        """初始化AI服务提供商可用性检测"""
        if self._initialized:
            return
            
        has_available_provider = False
        
        for key, provider in self.providers.items():
            # 检查API密钥是否存在
            if not provider['api_key'] or not provider['secret_id']:
                logger.warning(f"⚠️ {provider['name']} API密钥或SecretId未配置")
                provider['available'] = False
                continue
            
            # 测试服务可用性
            try:
                provider['available'] = await self.test_provider_availability(key)
                if provider['available']:
                    has_available_provider = True
                    logger.info(f"✅ {provider['name']} 服务可用")
                else:
                    logger.warning(f"❌ {provider['name']} 服务不可用")
            except Exception as e:
                provider['available'] = False
                provider['last_error'] = str(e)
                logger.error(f"❌ {provider['name']} 服务测试失败: {e}")
        
        # 设置当前可用的提供商
        if has_available_provider:
            for key in self.fallback_order:
                if self.providers[key]['available']:
                    self.current_provider = key
                    logger.info(f"🎯 当前使用AI服务: {self.providers[key]['name']}")
                    break
        else:
            logger.warning("⚠️ 没有可用的AI服务提供商，将使用基础分析模式")
        
        self._initialized = True
    
    async def ensure_initialized(self):
        """确保服务已初始化"""
        if not self._initialized:
            await self.initialize_providers()
    
    async def test_provider_availability(self, provider_key: str) -> bool:
        """测试服务提供商可用性"""
        try:
            provider = self.providers[provider_key]
            test_prompt = '测试连接，请回复"OK"'
            
            response = await self.make_request(provider_key, test_prompt, 50)
            
            # 清除之前的错误信息
            provider['last_error'] = None
            
            return response and 'OK' in response
        except Exception as error:
            logger.warning(f"{self.providers[provider_key]['name']} 连接测试失败: {str(error)}")
            
            # 记录具体的错误信息
            self.providers[provider_key]['last_error'] = self.extract_error_message(error)
            
            return False
    
    def select_optimal_provider(self):
        """选择最优的AI服务提供商"""
        for provider_key in self.fallback_order:
            provider = self.providers[provider_key]
            if provider['available']:
                self.current_provider = provider_key
                logger.info(f"✅ 选择 {provider['name']} 作为主要AI服务提供商")
                return
        
        logger.warning("⚠️ 没有可用的AI服务提供商，请检查API密钥配置")
        self.current_provider = None
    
    async def make_request(self, provider_key: str, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """向AI服务提供商发送请求"""
        provider = self.providers[provider_key]
        
        if provider_key == 'hunyuan':
            return await self._make_hunyuan_request(provider, prompt, max_tokens)
        
        # 可以添加其他AI服务提供商的实现
        return None
    
    def _generate_hunyuan_signature(self, secret_key: str, timestamp: int) -> str:
        """生成腾讯混元API签名"""
        sign_str = f"timestamp={timestamp}"
        signature = hmac.new(
            secret_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def _make_hunyuan_request(self, provider: Dict, prompt: str, max_tokens: int) -> Optional[str]:
        """腾讯混元API请求"""
        try:
            timestamp = int(time.time())
            signature = self._generate_hunyuan_signature(provider['api_key'], timestamp)
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'{provider["secret_id"]}',
                'X-TC-Timestamp': str(timestamp),
                'X-TC-Signature': signature
            }
            
            payload = {
                'prompt': prompt,
                'max_tokens': max_tokens,
                'temperature': 0.7,
                'top_p': 0.9
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{provider['base_url']}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get('choices', [{}])[0].get('message', {}).get('content', '')
                    else:
                        error_text = await response.text()
                        raise Exception(f"API请求失败: {response.status} - {error_text}")
                        
        except aiohttp.ClientError as error:
            logger.error(f"腾讯混元网络请求错误: {str(error)}")
            raise Exception(f"网络连接错误: {str(error)}")
        except Exception as error:
            logger.error(f"腾讯混元API调用失败: {str(error)}")
            raise error
    
    def extract_error_message(self, error: Exception) -> str:
        """从错误中提取有用的错误信息"""
        error_msg = str(error)
        
        if 'network' in error_msg.lower() or 'connection' in error_msg.lower():
            return "网络连接错误"
        elif 'timeout' in error_msg.lower():
            return "请求超时"
        elif 'auth' in error_msg.lower() or 'key' in error_msg.lower():
            return "API认证失败"
        elif 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
            return "API调用额度不足"
        else:
            return error_msg
    
    def get_service_status(self) -> Dict[str, Any]:
        """获取AI服务状态"""
        provider_status = {}
        has_configured_api_keys = False
        
        for key, provider in self.providers.items():
            provider_status[key] = {
                'name': provider['name'],
                'available': provider['available'],
                'has_api_key': bool(provider['api_key']),
                'configured': bool(provider['api_key'] and provider['secret_id']),
                'base_url': provider['base_url'],
                'last_error': provider.get('last_error')
            }
            
            if provider['api_key']:
                has_configured_api_keys = True
        
        # 构建状态消息
        status_messages = []
        for key in self.fallback_order:
            provider = self.providers[key]
            if provider['available']:
                status_messages.append(f"{provider['name']}: 服务可用")
            elif provider['api_key']:
                error_msg = provider.get('last_error', '未知错误')
                status_messages.append(f"{provider['name']}: API密钥已配置但连接失败 ({error_msg})")
            else:
                status_messages.append(f"{provider['name']}: API密钥未配置")
        
        return {
            'current_provider': self.current_provider,
            'providers': provider_status,
            'fallback_order': self.fallback_order,
            'has_configured_api_keys': has_configured_api_keys,
            'service_available': bool(self.current_provider),
            'message': '\n'.join(status_messages),
            'detailed_status': provider_status
        }
    
    def get_provider_status(self) -> Dict[str, Any]:
        """获取提供商状态（兼容性方法）"""
        return self.get_service_status()
    
    async def test_connectivity(self, provider_key: str = None) -> Dict[str, Any]:
        """测试AI服务连通性"""
        try:
            if not provider_key:
                provider_key = self.current_provider
            
            if not provider_key:
                return {
                    'success': False,
                    'message': '没有可用的AI服务提供商',
                    'details': '请检查API密钥配置'
                }
            
            provider = self.providers[provider_key]
            
            # 测试连接
            test_result = await self.test_provider_availability(provider_key)
            
            return {
                'success': test_result,
                'provider': provider['name'],
                'provider_key': provider_key,
                'configured': bool(provider['api_key'] and provider['secret_id']),
                'available': provider['available'],
                'last_error': provider.get('last_error'),
                'message': f"{provider['name']}连通性测试{'成功' if test_result else '失败'}",
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as error:
            logger.error(f"连通性测试错误: {str(error)}")
            return {
                'success': False,
                'message': f'连通性测试失败: {str(error)}',
                'timestamp': datetime.now().isoformat()
            }
    
    async def analyze_content(self, content: str, title: str = "", source_credibility: float = 0.8) -> Dict[str, Any]:
        """分析文章内容"""
        if not self.current_provider:
            # 使用基础分析模式
            return self._get_fallback_analysis(content, title, source_credibility)
        
        try:
            # 限制内容长度，优化API调用成本
            truncated_content = content[:4000]
            
            # 构建分析提示
            analysis_prompt = f"""
请分析以下股票新闻文章，提供专业的投资分析：

标题：{title}
内容：{truncated_content}

请从以下维度进行分析：
1. 情绪分析（积极/消极/中性）
2. 风险等级评估（低/中/高）
3. 投资建议（买入/持有/卖出/观望）
4. 关键信息提取
5. 对相关股票的影响分析

请以JSON格式返回分析结果。
"""
            
            response = await self.make_request(self.current_provider, analysis_prompt, 1000)
            
            if response:
                return self._parse_analysis_response(response, source_credibility)
            else:
                return self._get_fallback_analysis(content, title, source_credibility)
                
        except Exception as error:
            logger.error(f"AI分析失败: {str(error)}")
            return self._get_fallback_analysis(content, title, source_credibility)
    
    def _parse_analysis_response(self, response: str, source_credibility: float) -> Dict[str, Any]:
        """解析AI分析响应"""
        # 这里应该根据实际的AI响应格式进行解析
        # 简化处理，返回基础分析结果
        return {
            'sentiment': 'neutral',
            'sentiment_score': 0.5,
            'risk_level': 'medium',
            'investment_advice': 'hold',
            'key_points': ['基础分析模式'],
            'stock_impact': '中性影响',
            'confidence': 0.6 * source_credibility,
            'analysis_timestamp': datetime.now().isoformat(),
            'ai_provider': self.providers[self.current_provider]['name']
        }
    
    def _get_fallback_analysis(self, content: str, title: str = "", source_credibility: float = 0.8) -> Dict[str, Any]:
        """基础分析模式（降级处理）"""
        return {
            'sentiment': 'neutral',
            'sentiment_score': 0.5,
            'risk_level': 'medium',
            'investment_advice': '观望',
            'key_points': ['使用基础分析模式'],
            'stock_impact': '影响待评估',
            'confidence': 0.5 * source_credibility,
            'analysis_timestamp': datetime.now().isoformat(),
            'ai_provider': '基础分析模式',
            'fallback_mode': True
        }

# 创建全局AI服务实例
ai_service = AIServiceManager()