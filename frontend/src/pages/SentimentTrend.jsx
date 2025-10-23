import React, { useState, useEffect } from 'react'
import { Card, Select, DatePicker, Spin, Typography, Row, Col, Statistic } from 'antd'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import axios from 'axios'

const { Title } = Typography
const { Option } = Select
const { RangePicker } = DatePicker

const SentimentTrend = () => {
  const [trendData, setTrendData] = useState([])
  const [loading, setLoading] = useState(false)
  const [timeRange, setTimeRange] = useState('7d') // 7d, 30d, 90d

  const fetchTrendData = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/analysis/trend`, {
        params: { period: timeRange }
      })
      setTrendData(response.data.trend || [])
    } catch (error) {
      console.error('获取趋势数据失败:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTrendData()
  }, [timeRange])

  // 模拟统计数据
  const stats = {
    totalNews: trendData.reduce((sum, item) => sum + (item.positive + item.neutral + item.negative), 0),
    positiveRate: trendData.length > 0 ? 
      Math.round((trendData[trendData.length - 1].positive / 
        (trendData[trendData.length - 1].positive + trendData[trendData.length - 1].neutral + trendData[trendData.length - 1].negative)) * 100) : 0,
    avgSentiment: trendData.length > 0 ? 
      Math.round(((trendData.reduce((sum, item) => sum + item.sentiment_score, 0)) / trendData.length) * 100) / 100 : 0
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
          <Title level={3} style={{ margin: 0 }}>情绪趋势分析</Title>
          <Select 
            value={timeRange} 
            onChange={setTimeRange}
            style={{ width: 120 }}
          >
            <Option value="7d">最近7天</Option>
            <Option value="30d">最近30天</Option>
            <Option value="90d">最近90天</Option>
          </Select>
        </div>

        {/* 统计卡片 */}
        <Row gutter={16} style={{ marginBottom: '24px' }}>
          <Col span={8}>
            <Card>
              <Statistic
                title="总新闻数"
                value={stats.totalNews}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="积极新闻比例"
                value={stats.positiveRate}
                suffix="%"
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="平均情绪得分"
                value={stats.avgSentiment}
                valueStyle={{ color: stats.avgSentiment > 0 ? '#52c41a' : '#f5222d' }}
              />
            </Card>
          </Col>
        </Row>

        <Spin spinning={loading}>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="positive" 
                stroke="#52c41a" 
                strokeWidth={2}
                name="积极新闻"
              />
              <Line 
                type="monotone" 
                dataKey="neutral" 
                stroke="#faad14" 
                strokeWidth={2}
                name="中性新闻"
              />
              <Line 
                type="monotone" 
                dataKey="negative" 
                stroke="#f5222d" 
                strokeWidth={2}
                name="消极新闻"
              />
              <Line 
                type="monotone" 
                dataKey="sentiment_score" 
                stroke="#1890ff" 
                strokeWidth={3}
                name="情绪得分"
                dot={{ fill: '#1890ff' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Spin>
      </Card>
    </div>
  )
}

export default SentimentTrend