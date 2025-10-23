import React, { useState, useEffect } from 'react'
import { Card, Form, Input, Button, Switch, Select, message, Typography, Divider, Space } from 'antd'
import { SaveOutlined, ReloadOutlined } from '@ant-design/icons'
import axios from 'axios'

const { Title } = Typography
const { Option } = Select
const { TextArea } = Input

const Settings = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)

  // 初始化表单数据
  useEffect(() => {
    const loadSettings = async () => {
      setLoading(true)
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/settings`)
        form.setFieldsValue(response.data.settings || {})
      } catch (error) {
        console.error('加载设置失败:', error)
        // 设置默认值
        form.setFieldsValue({
          apiUrl: process.env.REACT_APP_API_URL || '',
          newsSources: ['sina', 'eastmoney', 'xueqiu'],
          crawlInterval: 30,
          enableNotifications: true,
          riskThreshold: 0.7
        })
      } finally {
        setLoading(false)
      }
    }

    loadSettings()
  }, [form])

  const handleSave = async (values) => {
    setSaving(true)
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/api/settings`, values)
      message.success('设置保存成功')
    } catch (error) {
      console.error('保存设置失败:', error)
      message.error('保存设置失败')
    } finally {
      setSaving(false)
    }
  }

  const handleReset = () => {
    form.resetFields()
    message.info('设置已重置')
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={3}>应用设置</Title>
        
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          style={{ maxWidth: 600 }}
        >
          {/* API 配置 */}
          <Divider orientation="left">API 配置</Divider>
          <Form.Item
            label="后端API地址"
            name="apiUrl"
            rules={[{ required: true, message: '请输入API地址' }]}
          >
            <Input placeholder="例如: https://your-api.vercel.app" />
          </Form.Item>

          {/* 新闻源配置 */}
          <Divider orientation="left">新闻源配置</Divider>
          <Form.Item
            label="新闻源"
            name="newsSources"
            rules={[{ required: true, message: '请选择至少一个新闻源' }]}
          >
            <Select mode="multiple" placeholder="选择新闻源">
              <Option value="sina">新浪财经</Option>
              <Option value="eastmoney">东方财富</Option>
              <Option value="xueqiu">雪球</Option>
              <Option value="jin10">金十数据</Option>
              <Option value="wallstreetcn">华尔街见闻</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="爬取间隔（分钟）"
            name="crawlInterval"
            rules={[{ required: true, message: '请输入爬取间隔' }]}
          >
            <Input type="number" min={5} max={1440} />
          </Form.Item>

          {/* 通知配置 */}
          <Divider orientation="left">通知配置</Divider>
          <Form.Item
            label="启用通知"
            name="enableNotifications"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            label="风险阈值"
            name="riskThreshold"
            tooltip="当新闻风险评估超过此阈值时发送通知"
          >
            <Input type="number" min={0} max={1} step={0.1} />
          </Form.Item>

          {/* 高级配置 */}
          <Divider orientation="left">高级配置</Divider>
          <Form.Item
            label="自定义爬取规则"
            name="customRules"
          >
            <TextArea 
              rows={4} 
              placeholder="输入自定义的新闻爬取规则（JSON格式）"
            />
          </Form.Item>

          {/* 操作按钮 */}
          <Form.Item>
            <Space>
              <Button 
                type="primary" 
                htmlType="submit" 
                icon={<SaveOutlined />}
                loading={saving}
              >
                保存设置
              </Button>
              <Button 
                icon={<ReloadOutlined />}
                onClick={handleReset}
              >
                重置
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>

      {/* 系统信息 */}
      <Card style={{ marginTop: 24 }}>
        <Title level={4}>系统信息</Title>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div>
            <strong>前端版本:</strong> 1.0.0
          </div>
          <div>
            <strong>构建时间:</strong> {new Date().toLocaleString()}
          </div>
          <div>
            <strong>当前环境:</strong> {process.env.NODE_ENV}
          </div>
          <div>
            <strong>API地址:</strong> {process.env.REACT_APP_API_URL || '未设置'}
          </div>
        </div>
      </Card>
    </div>
  )
}

export default Settings