import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import {
  DashboardOutlined,
  FileTextOutlined,
  BarChartOutlined,
  SettingOutlined
} from '@ant-design/icons'
import Dashboard from '@/pages/Dashboard.jsx'
import NewsAnalysis from '@/pages/NewsAnalysis.jsx'
import SentimentTrend from '@/pages/SentimentTrend.jsx'
import Settings from '@/pages/Settings.jsx'
import './App.css'

const { Header, Sider, Content } = Layout

function App() {
  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: '仪表板',
      path: '/'
    },
    {
      key: '2',
      icon: <FileTextOutlined />,
      label: '新闻分析',
      path: '/news'
    },
    {
      key: '3',
      icon: <BarChartOutlined />,
      label: '情绪趋势',
      path: '/sentiment'
    },
    {
      key: '4',
      icon: <SettingOutlined />,
      label: '设置',
      path: '/settings'
    }
  ]

  const [collapsed, setCollapsed] = React.useState(false)

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ height: 32, margin: 16, background: 'rgba(255, 255, 255, 0.3)' }} />
        <Menu
          theme="dark"
          defaultSelectedKeys={['1']}
          mode="inline"
          items={menuItems.map(item => ({
            ...item,
            onClick: () => window.location.href = item.path
          }))}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: '#fff' }} />
        <Content style={{ margin: '0 16px' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/news" element={<NewsAnalysis />} />
            <Route path="/sentiment" element={<SentimentTrend />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  )
}

export default App