#!/usr/bin/env python3
"""
股票新闻分析系统 - Python后端启动脚本
用于本地开发和测试Flask应用
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def main():
    """主函数"""
    print("🚀 启动股票新闻分析系统 - Python后端")
    print("=" * 50)
    
    # 检查环境变量
    required_env_vars = ['HUNYUAN_API_KEY', 'HUNYUAN_SECRET_ID']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("⚠️  警告: 以下环境变量未设置:")
        for var in missing_vars:
            print(f"   - {var}")
        print("   应用将以基础模式运行（AI服务不可用）")
        print("   请参考 .env.example 文件配置环境变量")
    else:
        print("✅ 环境变量配置正常")
    
    print(f"🌐 环境: {'Vercel生产环境' if os.getenv('VERCEL') == '1' else '本地开发环境'}")
    print(f"🔧 调试模式: {'开启' if os.getenv('FLASK_DEBUG') == 'True' else '关闭'}")
    print(f"📊 服务端口: {os.getenv('PORT', 3001)}")
    print("=" * 50)
    
    # 启动Flask应用
    port = int(os.getenv('PORT', 3001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()