#!/usr/bin/env python3
"""
股票新闻分析系统 - Python后端测试脚本
用于测试所有API端点的功能
"""

import asyncio
import requests
import json
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:3001"
TEST_USER_ID = "test_user_001"

def print_section(title):
    """打印测试章节标题"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")

def test_endpoint(method, endpoint, data=None, description=""):
    """测试单个API端点"""
    print(f"\n🔍 测试: {description}")
    print(f"  端点: {method} {endpoint}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method.upper() == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        elif method.upper() == 'PUT':
            response = requests.put(f"{BASE_URL}{endpoint}", json=data)
        else:
            print("   ❌ 不支持的HTTP方法")
            return False
        
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success', False):
                print("   ✅ 测试通过")
                return True
            else:
                print(f"   ❌ API返回失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"   ❌ HTTP错误: {response.status_code}")
            if response.text:
                print(f"   错误信息: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ 连接失败 - 请确保应用正在运行")
        return False
    except Exception as e:
        print(f"   ❌ 测试异常: {str(e)}")
        return False

async def test_ai_service():
    """测试AI服务功能"""
    print_section("测试AI分析服务")
    
    # 测试AI服务状态
    test_endpoint('GET', '/api/analysis/ai-status', description="AI服务状态检查")
    
    # 测试文章分析
    test_article = {
        "content": "今日A股市场表现强劲，上证指数上涨2.5%，突破3200点大关。科技股领涨，金融板块表现稳定。市场情绪积极，投资者信心回升。",
        "title": "A股市场今日大涨，上证指数突破3200点",
        "sourceCredibility": 0.8
    }
    test_endpoint('POST', '/api/analysis/analyze', data=test_article, description="单篇文章分析")

async def test_news_service():
    """测试新闻服务功能"""
    print_section("测试新闻服务")
    
    # 测试新闻状态
    test_endpoint('GET', '/api/news/', description="新闻服务状态")
    
    # 测试获取最新新闻
    test_endpoint('GET', '/api/news/latest?limit=3', description="获取最新新闻")
    
    # 测试搜索新闻
    test_endpoint('GET', '/api/news/search?q=A股', description="搜索新闻")

async def test_notification_service():
    """测试通知服务功能"""
    print_section("测试通知服务")
    
    # 测试通知服务状态
    test_endpoint('GET', '/api/notifications/', description="通知服务状态")
    
    # 测试发送通知
    test_notification = {
        "user_id": TEST_USER_ID,
        "message": "这是一条测试通知消息",
        "priority": "medium"
    }
    test_endpoint('POST', '/api/notifications/send', data=test_notification, description="发送通知")
    
    # 测试获取用户偏好
    test_endpoint('GET', f'/api/notifications/preferences/{TEST_USER_ID}', description="获取用户偏好")

async def test_email_service():
    """测试邮件服务功能"""
    print_section("测试邮件服务")
    
    # 测试邮件服务状态
    test_endpoint('GET', '/api/email/', description="邮件服务状态")
    
    # 测试邮件服务连通性
    test_endpoint('GET', '/api/email/test', description="邮件服务测试")

async def test_telegram_service():
    """测试Telegram服务功能"""
    print_section("测试Telegram服务")
    
    # 测试Telegram服务状态
    test_endpoint('GET', '/api/telegram/', description="Telegram服务状态")
    
    # 测试服务连通性
    test_endpoint('GET', '/api/telegram/test', description="Telegram服务测试")

async def test_wechat_work_service():
    """测试企业微信服务功能"""
    print_section("测试企业微信服务")
    
    # 测试企业微信服务状态
    test_endpoint('GET', '/api/wechat-work/', description="企业微信服务状态")
    
    # 测试服务连通性
    test_endpoint('GET', '/api/wechat-work/test', description="企业微信服务测试")

async def test_health_and_root():
    """测试健康检查和根路径"""
    print_section("测试基础服务")
    
    # 测试根路径
    test_endpoint('GET', '/', description="根路径访问")
    
    # 测试健康检查
    test_endpoint('GET', '/health', description="健康检查")
    
    # 测试404处理
    test_endpoint('GET', '/api/nonexistent', description="404错误处理")

async def main():
    """主测试函数"""
    print("🚀 股票新闻分析系统 - Python后端功能测试")
    print("=" * 60)
    print(f"📡 测试服务器: {BASE_URL}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 执行所有测试
    await test_health_and_root()
    await test_ai_service()
    await test_news_service()
    await test_notification_service()
    await test_email_service()
    await test_telegram_service()
    await test_wechat_work_service()
    
    print_section("测试完成")
    print("🎉 所有测试执行完毕！")
    print("💡 注意: 部分测试可能因缺少配置而失败，这是正常现象")
    print("📋 请根据实际需求配置相应的服务密钥和环境变量")

if __name__ == '__main__':
    asyncio.run(main())