import logging
import json
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, Response
from functools import wraps

logger = logging.getLogger(__name__)

# 创建蓝图
news_bp = Blueprint('news', __name__)

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

# 模拟新闻数据（实际应该从数据库或API获取）
MOCK_NEWS_DATA = [
    {
        'id': 1,
        'title': 'A股市场今日大涨，上证指数突破3200点',
        'content': '今日A股市场表现强劲，上证指数上涨2.5%，突破3200点大关。科技股领涨，金融板块表现稳定。',
        'source': '新浪财经',
        'publish_time': '2024-01-23T09:30:00Z',
        'category': '市场动态',
        'sentiment': 'positive',
        'keywords': ['A股', '上证指数', '科技股']
    },
    {
        'id': 2,
        'title': '央行宣布降准0.5个百分点，释放长期资金约1万亿元',
        'content': '中国人民银行决定下调金融机构存款准备金率0.5个百分点，预计释放长期资金约1万亿元。',
        'source': '财经网',
        'publish_time': '2024-01-23T10:00:00Z',
        'category': '政策动态',
        'sentiment': 'positive',
        'keywords': ['央行', '降准', '货币政策']
    },
    {
        'id': 3,
        'title': '某科技公司发布业绩预警，股价下跌8%',
        'content': '某知名科技公司发布三季度业绩预警，预计净利润同比下降30%，股价开盘下跌8%。',
        'source': '证券时报',
        'publish_time': '2024-01-23T11:15:00Z',
        'category': '公司动态',
        'sentiment': 'negative',
        'keywords': ['科技公司', '业绩预警', '股价下跌']
    }
]

def filter_news_by_keywords(news_list, keywords):
    """根据关键词过滤新闻"""
    if not keywords:
        return news_list
    
    filtered_news = []
    for news in news_list:
        content = f"{news.get('title', '')} {news.get('content', '')}".lower()
        if any(keyword.lower() in content for keyword in keywords):
            filtered_news.append(news)
    
    return filtered_news

def filter_news_by_time(news_list, hours=24):
    """根据时间过滤新闻"""
    cutoff_time = datetime.now() - timedelta(hours=hours)
    return [news for news in news_list if 
            datetime.fromisoformat(news['publish_time'].replace('Z', '+00:00')) > cutoff_time]

def filter_news_by_sentiment(news_list, sentiment):
    """根据情绪过滤新闻"""
    if not sentiment:
        return news_list
    return [news for news in news_list if news.get('sentiment') == sentiment]

# 根路径路由
@news_bp.route('/', methods=['GET'])
@ensure_chinese_response
def get_news_status():
    return jsonify_chinese({
        'service': '股票新闻获取服务',
        'status': 'active',
        'endpoints': {
            'latest': '/latest - GET - 获取最新新闻',
            'search': '/search - GET - 搜索新闻',
            'categories': '/categories - GET - 获取新闻分类',
            'sources': '/sources - GET - 获取新闻来源',
            'crawl': '/crawl - POST - 新闻爬取（GitHub Actions集成）'
        },
        'features': [
            '实时新闻获取',
            '关键词过滤',
            '情绪分析',
            '时间范围筛选',
            '多来源整合',
            'GitHub Actions定时爬取'
        ],
        'timestamp': datetime.now().isoformat()
    })

# 获取最新新闻
@news_bp.route('/latest', methods=['GET'])
@ensure_chinese_response
def get_latest_news():
    try:
        # 获取查询参数
        limit = int(request.args.get('limit', 10))
        hours = int(request.args.get('hours', 24))
        keywords = request.args.get('keywords', '')
        sentiment = request.args.get('sentiment', '')
        
        # 参数验证
        if limit > 50:
            return jsonify_chinese({'error': 'limit参数不能超过50'}), 400
        
        # 过滤新闻
        filtered_news = MOCK_NEWS_DATA.copy()
        
        # 时间过滤
        filtered_news = filter_news_by_time(filtered_news, hours)
        
        # 关键词过滤
        if keywords:
            keyword_list = [k.strip() for k in keywords.split(',')]
            filtered_news = filter_news_by_keywords(filtered_news, keyword_list)
        
        # 情绪过滤
        if sentiment:
            filtered_news = filter_news_by_sentiment(filtered_news, sentiment)
        
        # 限制数量
        result_news = filtered_news[:limit]
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'news': result_news,
                'total_count': len(result_news),
                'filtered_count': len(filtered_news),
                'original_count': len(MOCK_NEWS_DATA),
                'filters_applied': {
                    'hours': hours,
                    'keywords': keywords,
                    'sentiment': sentiment,
                    'limit': limit
                }
            },
            'message': f'获取到{len(result_news)}条新闻'
        })
        
    except ValueError as e:
        return jsonify_chinese({'error': '参数格式错误', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f'获取新闻错误: {str(e)}')
        return jsonify_chinese({'error': '获取新闻失败', 'message': str(e)}), 500

# 搜索新闻
@news_bp.route('/search', methods=['GET'])
@ensure_chinese_response
def search_news():
    try:
        query = request.args.get('q', '')
        category = request.args.get('category', '')
        source = request.args.get('source', '')
        limit = int(request.args.get('limit', 10))
        
        if not query:
            return jsonify_chinese({'error': '请提供搜索关键词'}), 400
        
        if limit > 50:
            return jsonify_chinese({'error': 'limit参数不能超过50'}), 400
        
        # 搜索逻辑
        results = []
        for news in MOCK_NEWS_DATA:
            content = f"{news.get('title', '')} {news.get('content', '')}".lower()
            query_lower = query.lower()
            
            # 关键词匹配
            if query_lower in content:
                # 分类过滤
                if category and news.get('category') != category:
                    continue
                # 来源过滤
                if source and news.get('source') != source:
                    continue
                
                results.append(news)
        
        # 限制数量
        results = results[:limit]
        
        return jsonify_chinese({
            'success': True,
            'data': {
                'results': results,
                'total_count': len(results),
                'query': query,
                'filters': {
                    'category': category,
                    'source': source,
                    'limit': limit
                }
            },
            'message': f'搜索到{len(results)}条相关新闻'
        })
        
    except ValueError as e:
        return jsonify_chinese({'error': '参数格式错误', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f'搜索新闻错误: {str(e)}')
        return jsonify_chinese({'error': '搜索新闻失败', 'message': str(e)}), 500

# 获取新闻分类
@news_bp.route('/categories', methods=['GET'])
@ensure_chinese_response
def get_categories():
    categories = list(set(news['category'] for news in MOCK_NEWS_DATA))
    return jsonify_chinese({
        'success': True,
        'data': {
            'categories': categories,
            'total_count': len(categories)
        },
        'message': f'获取到{len(categories)}个新闻分类'
    })

# 获取新闻来源
@news_bp.route('/sources', methods=['GET'])
@ensure_chinese_response
def get_sources():
    sources = list(set(news['source'] for news in MOCK_NEWS_DATA))
    return jsonify_chinese({
        'success': True,
        'data': {
            'sources': sources,
            'total_count': len(sources)
        },
        'message': f'获取到{len(sources)}个新闻来源'
    })

# 获取新闻详情
@news_bp.route('/<int:news_id>', methods=['GET'])
@ensure_chinese_response
def get_news_detail(news_id):
    news = next((n for n in MOCK_NEWS_DATA if n['id'] == news_id), None)
    if not news:
        return jsonify_chinese({'error': '新闻不存在'}), 404
    
    return jsonify_chinese({
        'success': True,
        'data': news,
        'message': '获取新闻详情成功'
    })

# 新闻爬取接口 - 支持GitHub Actions定时任务调用
@news_bp.route('/crawl', methods=['POST'])
@ensure_chinese_response
def crawl_news():
    """
    新闻爬取接口，支持从多个新闻源爬取新闻
    请求体格式:
    {
        "sources": ["新浪财经", "东方财富", "雪球"]
    }
    """
    try:
        # 解析请求数据
        data = request.get_json()
        if not data:
            return jsonify_chinese({'error': '请求体必须为JSON格式'}), 400
        
        sources = data.get('sources', ['新浪财经', '东方财富', '雪球'])
        
        if not isinstance(sources, list):
            return jsonify_chinese({'error': 'sources参数必须为数组'}), 400
        
        logger.info(f"开始爬取新闻，来源: {sources}")
        
        # 模拟爬取过程
        crawl_results = []
        
        for source in sources:
            try:
                # 模拟不同新闻源的爬取结果
                if source == '新浪财经':
                    news_items = [
                        {
                            'title': 'A股市场今日表现平稳，科技股领涨',
                            'url': 'https://finance.sina.com.cn/stock/marketresearch/2024-01-23/doc-xxxxx.shtml',
                            'content': '今日A股市场整体表现平稳，科技板块表现强势，多只科技股涨幅超过5%。',
                            'publish_time': datetime.now().isoformat(),
                            'source': '新浪财经',
                            'credibility': 0.85
                        },
                        {
                            'title': '央行货币政策保持稳健，市场流动性充裕',
                            'url': 'https://finance.sina.com.cn/money/bank/2024-01-23/doc-yyyyy.shtml',
                            'content': '央行表示将继续实施稳健的货币政策，保持市场流动性合理充裕。',
                            'publish_time': datetime.now().isoformat(),
                            'source': '新浪财经',
                            'credibility': 0.90
                        }
                    ]
                elif source == '东方财富':
                    news_items = [
                        {
                            'title': '北向资金今日净流入超50亿元',
                            'url': 'https://finance.eastmoney.com/news/xxxxx.html',
                            'content': '今日北向资金净流入52.3亿元，主要流入科技和消费板块。',
                            'publish_time': datetime.now().isoformat(),
                            'source': '东方财富',
                            'credibility': 0.88
                        },
                        {
                            'title': '多家上市公司发布业绩预告',
                            'url': 'https://finance.eastmoney.com/news/yyyyy.html',
                            'content': '近期多家上市公司发布三季度业绩预告，整体表现符合预期。',
                            'publish_time': datetime.now().isoformat(),
                            'source': '东方财富',
                            'credibility': 0.82
                        }
                    ]
                elif source == '雪球':
                    news_items = [
                        {
                            'title': '投资者情绪指数回升，市场信心增强',
                            'url': 'https://xueqiu.com/xxxxx',
                            'content': '最新投资者情绪调查显示，市场信心较上月有明显提升。',
                            'publish_time': datetime.now().isoformat(),
                            'source': '雪球',
                            'credibility': 0.75
                        },
                        {
                            '标题': '机构调研报告：关注科技成长股投资机会',
                            'url': 'https://xueqiu.com/yyyyy',
                            '内容': '多家机构发布调研报告，建议关注科技成长股的投资机会。',
                            'publish_time': datetime.now().isoformat(),
                            'source': '雪球',
                            'credibility': 0.78
                        }
                    ]
                else:
                    # 默认新闻源
                    news_items = [
                        {
                            'title': f'{source}最新市场动态',
                            'url': f'https://example.com/news/123',
                            'content': f'来自{source}的最新市场动态和分析报告。',
                            'publish_time': datetime.now().isoformat(),
                            'source': source,
                            'credibility': 0.70
                        }
                    ]
                
                crawl_results.append({
                    'source': source,
                    'success': True,
                    'items': news_items,
                    'count': len(news_items),
                    'message': f'成功爬取{len(news_items)}条新闻'
                })
                
                logger.info(f"成功爬取 {source}: {len(news_items)} 条新闻")
                
            except Exception as e:
                logger.error(f"爬取 {source} 失败: {str(e)}")
                crawl_results.append({
                    'source': source,
                    'success': False,
                    'items': [],
                    'count': 0,
                    'message': f'爬取失败: {str(e)}',
                    'error': str(e)
                })
        
        # 统计总体结果
        total_items = sum(result['count'] for result in crawl_results)
        successful_sources = [result['source'] for result in crawl_results if result['success']]
        
        return jsonify_chinese({
            'success': True,
            'results': crawl_results,
            'summary': {
                'total_sources': len(sources),
                'successful_sources': len(successful_sources),
                'failed_sources': len(sources) - len(successful_sources),
                'total_items': total_items,
                'average_credibility': round(sum(item['credibility'] for result in crawl_results for item in result['items']) / total_items if total_items > 0 else 0, 2),
                'timestamp': datetime.now().isoformat()
            },
            'message': f'爬取完成: {len(successful_sources)}/{len(sources)} 个源成功，共获取 {total_items} 条新闻'
        })
        
    except Exception as e:
        logger.error(f"新闻爬取接口错误: {str(e)}")
        return jsonify_chinese({
            'success': False,
            'error': '新闻爬取失败',
            'message': str(e)
        }), 500

# 健康检查端点
@news_bp.route('/health', methods=['GET'])
@ensure_chinese_response
def health_check():
    return jsonify_chinese({
        'status': 'healthy',
        'service': '股票新闻服务',
        'timestamp': datetime.now().isoformat(),
        'endpoints_available': ['/', '/latest', '/search', '/categories', '/sources', '/<id>'],
        'features': ['实时新闻', '关键词搜索', '分类过滤', '情绪分析']
    })

# 测试新闻API连通性
@news_bp.route('/test', methods=['GET'])
@ensure_chinese_response
def test_news_api():
    try:
        return jsonify({
            'success': True,
            'data': {
                'status': 'connected',
                'timestamp': datetime.now().isoformat(),
                'available_sources': len(set(n.get('source') for n in MOCK_NEWS_DATA)),
                'total_articles': len(MOCK_NEWS_DATA)
            },
            'message': '新闻API连接正常'
        })
        
    except Exception as e:
        logger.error(f'测试API错误: {str(e)}')
        return jsonify({'error': 'API测试失败', 'message': str(e)}), 500