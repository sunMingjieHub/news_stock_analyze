import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import App from './App.jsx'
import './index.css'

// 配置Antd主题
const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
  },
}

// 根据环境设置basename
const basename = process.env.NODE_ENV === 'production' ? '/news_stock_analyze' : '/'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ConfigProvider locale={zhCN} theme={theme}>
      <BrowserRouter basename={basename}>
        <App />
      </BrowserRouter>
    </ConfigProvider>
  </React.StrictMode>,
)