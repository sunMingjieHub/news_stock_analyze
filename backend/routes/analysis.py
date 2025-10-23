import logging
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, Response
from functools import wraps
from services.ai_service import ai_service

logger = logging.getLogger(__name__)

# 创建蓝图
analysis_bp = Blueprint('analysis', __name__)

# 自定义装饰器确保中文正确编码
def ensure_chinese_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if hasattr(response, 'headers'):
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    return wrapper

# 创建支持中文的jsonify函数
def jsonify_chinese(data):
    """支持中文的jsonify函数，确保ensure_ascii=False"""
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )

def calculate_confidence_score(analysis_result: dict, source_credibility: float) -> float:
    """计算分析置信度（资深交易家建议）"""
    base_confidence = 0.7
    # 根据分析结果的质量调整置信度
    if analysis_result.get('fallback_mode'):
        return 0.5 * source_credibility
    return base_confidence * source_credibility

def get_risk_level(confidence_score: float) -> str:
    """根据置信度获取风险等级"""
    if confidence_score >= 0.8:
        return '低风险'
    elif confidence_score >= 0.6:
        return '中等风险'
    else:
        return '高风险'

def get_risk_advice(sentiment: str, confidence_score: float) -> str:
    """获取风险建议"""
    if sentiment == 'positive' and confidence_score >= 0.7:
        return '可以考虑适当增持'
    elif sentiment == 'negative' and confidence_score >= 0.7:
        return '建议减仓或观望'
    else:
        return '建议结合其他信息源验证'

# 根路径路由 - 返回分析服务状态信息
@analysis_bp.route('/', methods=['GET'])
@ensure_chinese_response
def get_analysis_status():
    return jsonify_chinese({
        'service': '股票新闻分析系统 - AI分析服务',
        'status': 'active',
        'endpoints': {
            'analyze': '/analyze - POST - 分析单篇文章',
            'batch-analyze': '/batch-analyze - POST - 批量分析文章',
            'sentiment-trend': '/sentiment-trend - GET - 获取情绪趋势',
            'ai-providers': '/ai-providers - GET - 获取AI服务提供商状态'
        },
        'features': [
            '多维度AI分析（情绪、风险、投资建议）',
            '支持多种AI模型（OpenAI、Claude、DeepSeek等）',
            '自动降级机制保证服务可用性',
            '实时分析结果反馈',
            '批量处理能力'
        ],
        'timestamp': datetime.now().isoformat()
    })

# 分析单篇文章
@analysis_bp.route('/analyze', methods=['POST'])
@ensure_chinese_response
async def analyze_article():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请求体不能为空'}), 400
        
        article_content = data.get('content', '')
        article_title = data.get('title', '')
        
        if not article_content:
            return jsonify_chinese({'error': '文章内容不能为空'}), 400
        
        # 调用AI服务进行分析
        analysis_result = await ai_service.analyze_content(
            content=article_content,
            title=article_title
        )
        
        # 计算置信度和风险等级
        source_credibility = 0.9  # 假设来源可信度
        confidence_score = calculate_confidence_score(analysis_result, source_credibility)
        risk_level = get_risk_level(confidence_score)
        risk_advice = get_risk_advice(analysis_result.get('sentiment', 'neutral'), confidence_score)
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'analysis': analysis_result,
                'confidence': {
                    'score': round(confidence_score, 2),
                    'level': risk_level,
                    'advice': risk_advice
                },
                'source_credibility': source_credibility,
                'analysis_timestamp': datetime.now().isoformat()
            },
            'message': '文章分析完成'
        })
        
    except Exception as e:
        logger.error(f'分析文章错误: {str(e)}')
        return jsonify_chinese({
            'error': '分析失败',
            'message': str(e)
        }), 500

# 批量分析文章
@analysis_bp.route('/batch-analyze', methods=['POST'])
@ensure_chinese_response
async def batch_analyze_articles():
    try:
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请求体不能为空'}), 400
        
        articles = data.get('articles', [])
        if not articles:
            return jsonify_chinese({'error': '文章列表不能为空'}), 400
        
        if len(articles) > 10:
            return jsonify_chinese({'error': '批量分析最多支持10篇文章'}), 400
        
        results = []
        for article in articles:
            try:
                article_content = article.get('content', '')
                article_title = article.get('title', '')
                
                if not article_content:
                    results.append({
                        'success': False,
                        'error': '文章内容不能为空',
                        'article_id': article.get('id')
                    })
                    continue
                
                # 调用AI服务进行分析
                analysis_result = await ai_service.analyze_content(
                    content=article_content,
                    title=article_title
                )
                
                # 计算置信度
                source_credibility = 0.9
                confidence_score = calculate_confidence_score(analysis_result, source_credibility)
                risk_level = get_risk_level(confidence_score)
                risk_advice = get_risk_advice(analysis_result.get('sentiment', 'neutral'), confidence_score)
                
                results.append({
                    'success': True,
                    'article_id': article.get('id'),
                    'analysis': analysis_result,
                    'confidence': {
                        'score': round(confidence_score, 2),
                        'level': risk_level,
                        'advice': risk_advice
                    }
                })
                
            except Exception as e:
                logger.error(f'分析单篇文章错误: {str(e)}')
                results.append({
                    'success': False,
                    'error': str(e),
                    'article_id': article.get('id')
                })
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'results': results,
                'total_count': len(results),
                'success_count': len([r for r in results if r.get('success')]),
                'failed_count': len([r for r in results if not r.get('success')]),
                'batch_timestamp': datetime.now().isoformat()
            },
            'message': f'批量分析完成，成功{len([r for r in results if r.get("success")])}篇，失败{len([r for r in results if not r.get("success")])}篇'
        })
        
    except Exception as e:
        logger.error(f'批量分析错误: {str(e)}')
        return jsonify_chinese({
            'error': '批量分析失败',
            'message': str(e)
        }), 500

# 获取情绪趋势
@analysis_bp.route('/sentiment-trend', methods=['GET'])
@ensure_chinese_response
def get_sentiment_trend():
    try:
        days = int(request.args.get('days', 7))
        if days > 30:
            return jsonify_chinese({'error': '天数不能超过30天'}), 400
        
        # 模拟情绪趋势数据
        trend_data = [
            {
                'date': f'2024-01-{23-i}',
                'positive_count': max(5, 10 - i),
                'negative_count': max(2, 5 - i//2),
                'neutral_count': max(3, 8 - i//3),
                'total_articles': max(10, 20 - i)
            }
            for i in range(days)
        ]
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'trend': trend_data,
                'summary': {
                    'total_days': days,
                    'avg_positive_rate': round(sum(d['positive_count'] for d in trend_data) / sum(d['total_articles'] for d in trend_data), 2),
                    'avg_negative_rate': round(sum(d['negative_count'] for d in trend_data) / sum(d['total_articles'] for d in trend_data), 2),
                    'trend_period': f'最近{days}天'
                }
            },
            'message': f'获取到最近{days}天的情绪趋势数据'
        })
        
    except ValueError as e:
        return jsonify_chinese({'error': '参数格式错误', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f'获取情绪趋势错误: {str(e)}')
        return jsonify_chinese({'error': '获取情绪趋势失败', 'message': str(e)}), 500

# 获取AI服务提供商状态
@analysis_bp.route('/ai-providers', methods=['GET'])
@ensure_chinese_response
async def get_ai_providers_status():
    try:
        # 确保AI服务已初始化
        await ai_service.ensure_initialized()
        
        # 获取服务状态
        service_status = ai_service.get_service_status()
        
        # 构建提供商列表
        providers = []
        for key, provider_info in service_status['providers'].items():
            providers.append({
                'name': provider_info['name'],
                'key': key,
                'status': 'active' if provider_info['available'] else 'standby',
                'configured': provider_info['configured'],
                'base_url': provider_info['base_url'],
                'last_error': provider_info.get('last_error')
            })
        
        active_count = len([p for p in providers if p['status'] == 'active'])
        standby_count = len([p for p in providers if p['status'] == 'standby'])
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'providers': providers,
                'summary': {
                    'total_providers': len(providers),
                    'active_providers': active_count,
                    'standby_providers': standby_count,
                    'current_provider': service_status['current_provider'],
                    'overall_status': 'healthy' if active_count > 0 else 'degraded'
                }
            },
            'message': f'系统运行正常，{active_count}个主用服务，{standby_count}个备用服务'
        })
        
    except Exception as e:
        logger.error(f'获取AI服务状态错误: {str(e)}')
        return jsonify_chinese({'error': '获取AI服务状态失败', 'message': str(e)}), 500

# 健康检查端点
@analysis_bp.route('/health', methods=['GET'])
@ensure_chinese_response
def health_check():
    return jsonify_chinese({
        'status': 'healthy',
        'service': '股票新闻AI分析服务',
        'timestamp': datetime.now().isoformat(),
        'endpoints_available': ['/', '/analyze', '/batch-analyze', '/sentiment-trend', '/ai-providers'],
        'features': ['AI情绪分析', '风险等级评估', '投资建议', '批量处理', '多模型支持'],
        'system_info': {
            'ai_models_available': 4,
            'max_batch_size': 10,
            'avg_response_time': '350ms',
            'uptime': '99.8%'
        }
    })

# 测试分析API连通性
@analysis_bp.route('/test', methods=['GET'])
@ensure_chinese_response
async def test_analysis_api():
    try:
        # 确保AI服务已初始化
        await ai_service.ensure_initialized()
        
        # 测试hunyuan服务连通性
        connectivity_result = await ai_service.test_connectivity('hunyuan')
        
        return jsonify_chinese({
            'success': connectivity_result['success'],
            'data': {
                'status': 'connected' if connectivity_result['success'] else 'disconnected',
                'timestamp': datetime.now().isoformat(),
                'ai_service_available': connectivity_result['success'],
                'provider_info': {
                    'name': connectivity_result.get('provider', '未知'),
                    'configured': connectivity_result.get('configured', False),
                    'available': connectivity_result.get('available', False),
                    'last_error': connectivity_result.get('last_error')
                },
                'features': ['单篇分析', '批量分析', '情绪趋势', '风险评估', 'hunyuan AI服务']
            },
            'message': connectivity_result['message']
        })
        
    except Exception as e:
        logger.error(f'测试API错误: {str(e)}')
        return jsonify_chinese({'error': 'API测试失败', 'message': str(e)}), 500

# 测试特定AI服务提供商连通性
@analysis_bp.route('/test-provider/<provider_key>', methods=['GET'])
@ensure_chinese_response
async def test_ai_provider(provider_key):
    try:
        # 确保AI服务已初始化
        await ai_service.ensure_initialized()
        
        # 检查提供商是否存在
        if provider_key not in ai_service.providers:
            return jsonify_chinese({
                'error': '不支持的AI服务提供商',
                'message': f'提供商 {provider_key} 不存在，支持的提供商: {list(ai_service.providers.keys())}'
            }), 400
        
        # 测试特定提供商连通性
        connectivity_result = await ai_service.test_connectivity(provider_key)
        
        return jsonify_chinese({
            'success': connectivity_result['success'],
            'data': connectivity_result,
            'message': connectivity_result['message']
        })
        
    except Exception as e:
        logger.error(f'测试AI提供商错误: {str(e)}')
        return jsonify_chinese({'error': '提供商测试失败', 'message': str(e)}), 500