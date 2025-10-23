import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, List, Tag, Button, message } from 'antd'
import { 
  ArrowUpOutlined, 
  ArrowDownOutlined, 
  EyeOutlined,
  BarChartOutlined 
} from '@ant-design/icons'
import axios from 'axios'
import './Dashboard.css'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalArticles: 0,
    analyzedToday: 0,
    positiveSentiment: 0,
    negativeSentiment: 0
  })
  const [recentNews, setRecentNews] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      // 获取统计数据
      const statsResponse = await axios.get('/api/analysis/sentiment-trend?days=1')
      const newsResponse = await axios.get('/api/news/list?limit=5')
      
      // 模拟数据处理（实际应该从API获取）
      setStats({
        totalArticles: 156,
        analyzedToday: 23,
        positiveSentiment: 65,
        negativeSentiment: 12
      })
      
      setRecentNews(newsResponse.data.data || [])
    } catch (error) {
      console.error('获取仪表板数据失败:', error)
      message.error('获取数据失败')
    } finally {
      setLoading(false)
    }
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case '积极': return 'green'
      case '消极': return 'red'
      default: return 'orange'
    }
  }

  const handleAnalyzeNews = async () => {
    try {
      message.loading('正在分析最新新闻...', 0)
      // 这里可以调用分析API
      setTimeout(() => {
        message.destroy()
        message.success('分析完成！')
        fetchDashboardData() // 刷新数据
      }, 2000)
    } catch (error) {
      message.destroy()
      message.error('分析失败')
    }
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1 className="page-title">系统概览</h1>
        <p className="page-description">
          实时监控股票新闻情绪分析，为投资决策提供数据支持
        </p>
      </div>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} className="stats-row">
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总分析文章"
              value={stats.totalArticles}
              prefix={<EyeOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="今日分析"
              value={stats.analyzedToday}
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="积极情绪"
              value={stats.positiveSentiment}
              prefix={<ArrowUpOutlined />}
              valueStyle={{ color: '#52c41a' }}
              suffix="%"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="消极情绪"
              value={stats.negativeSentiment}
              prefix={<ArrowDownOutlined />}
              valueStyle={{ color: '#ff4d4f' }}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>

      {/* 操作区域 */}
      <Row gutter={[16, 16]} className="action-row">
        <Col span={24}>
          <Card 
            title="快速操作" 
            extra={
              <Button type="primary" onClick={handleAnalyzeNews}>
                立即分析最新新闻
              </Button>
            }
          >
            <div className="quick-actions">
              <Button icon={<BarChartOutlined />}>查看情绪趋势</Button>
              <Button icon={<EyeOutlined />}>浏览新闻列表</Button>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 最新新闻列表 */}
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card title="最新新闻分析" loading={loading}>
            <List
              itemLayout="horizontal"
              dataSource={recentNews}
              renderItem={(item, index) => (
                <List.Item
                  actions={[
                    <Tag color={getSentimentColor(item.sentiment)}>
                      {item.sentiment || '待分析'}
                    </Tag>
                  ]}
                >
                  <List.Item.Meta
                    title={<a href={item.url} target="_blank" rel="noopener noreferrer">{item.title}</a>}
                    description={
                      <div>
                        <span>来源: {item.source}</span>
                        <span style={{ marginLeft: 16 }}>时间: {new Date(item.timestamp).toLocaleString()}</span>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Dashboard