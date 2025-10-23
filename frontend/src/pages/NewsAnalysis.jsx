import React, { useState, useEffect } from 'react'
import { Card, Table, Tag, Button, message, Spin, Typography } from 'antd'
import { ReloadOutlined, EyeOutlined } from '@ant-design/icons'
import axios from 'axios'

const { Title } = Typography

const NewsAnalysis = () => {
  const [newsData, setNewsData] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchNewsData = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/news`)
      setNewsData(response.data.news || [])
      message.success('新闻数据加载成功')
    } catch (error) {
      console.error('获取新闻数据失败:', error)
      message.error('获取新闻数据失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchNewsData()
  }, [])

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      width: '40%',
      render: (text, record) => (
        <div>
          <div style={{ fontWeight: 'bold', marginBottom: 4 }}>{text}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            来源: {record.source} | 时间: {record.publish_time}
          </div>
        </div>
      )
    },
    {
      title: '情绪分析',
      dataIndex: 'sentiment',
      key: 'sentiment',
      width: '15%',
      render: (sentiment) => {
        let color = sentiment === 'positive' ? 'green' : sentiment === 'negative' ? 'red' : 'orange'
        let text = sentiment === 'positive' ? '积极' : sentiment === 'negative' ? '消极' : '中性'
        return <Tag color={color}>{text}</Tag>
      }
    },
    {
      title: '风险评估',
      dataIndex: 'risk_level',
      key: 'risk_level',
      width: '15%',
      render: (risk) => {
        let color = risk === 'high' ? 'red' : risk === 'medium' ? 'orange' : 'green'
        let text = risk === 'high' ? '高风险' : risk === 'medium' ? '中风险' : '低风险'
        return <Tag color={color}>{text}</Tag>
      }
    },
    {
      title: '操作',
      key: 'action',
      width: '10%',
      render: (_, record) => (
        <Button 
          type="link" 
          icon={<EyeOutlined />}
          onClick={() => window.open(record.url, '_blank')}
        >
          查看原文
        </Button>
      )
    }
  ]

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <Title level={3} style={{ margin: 0 }}>新闻分析</Title>
          <Button 
            type="primary" 
            icon={<ReloadOutlined />}
            onClick={fetchNewsData}
            loading={loading}
          >
            刷新数据
          </Button>
        </div>
        
        <Spin spinning={loading}>
          <Table
            columns={columns}
            dataSource={newsData}
            rowKey="id"
            pagination={{
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total) => `共 ${total} 条新闻`
            }}
          />
        </Spin>
      </Card>
    </div>
  )
}

export default NewsAnalysis