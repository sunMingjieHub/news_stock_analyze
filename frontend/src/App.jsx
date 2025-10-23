import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout, Menu } from 'antd'
import {
  DashboardOutlined,
  FileTextOutlined,
  BarChartOutlined,
  SettingOutlined
} from '@ant-design/icons'
import Dashboard from './pages/Dashboard'
import NewsAnalysis from './pages/NewsAnalysis'
import SentimentTrend from './pages/SentimentTrend'
import Settings from './pages/Settings'
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
      path: '/trend'
    },
    {
      key: '4',
      icon: <SettingOutlined />,
      label: '设置',
      path: '/settings'
    }
  ]

  return (
    <Layout className="app-layout">
      <Sider
        theme="light"
        breakpoint="lg"
        collapsedWidth="0"
        width={200}
      >
        <div className="logo">
          <h2>📈 股票分析</h2>
        </div>
        <Menu
          mode="inline"
          defaultSelectedKeys={['1']}
          items={menuItems.map(item => ({
            ...item,
            onClick: () => window.location.href = item.path
          }))}
        />
      </Sider>
      
      <Layout>
        <Header className="app-header">
          <h1>股票新闻智能分析系统</h1>
        </Header>
        
        <Content className="app-content">
          <div className="container">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/news" element={<NewsAnalysis />} />
              <Route path="/trend" element={<SentimentTrend />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </div>
        </Content>
      </Layout>
    </Layout>
  )
}

export default App