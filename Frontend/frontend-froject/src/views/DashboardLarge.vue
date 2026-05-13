<!-- src/views/DashboardLarge.vue -->
<!-- 可视化大屏 - 实时数据监控 -->
<template>
    <div class="dashboard-large">
        <!-- 顶部标题栏 -->
        <div class="header">
            <h1>AI布匹检测 · 实时数据可视化大屏</h1>
            <div class="header-right">
                <div class="time-display">{{ currentTime }}</div>
                <div class="system-status">
                    <span class="status-dot online"></span>
                    系统正常运行
                </div>
            </div>
        </div>

        <!-- 主要内容区域 -->
        <div class="main-content">
            <!-- 左侧面板 -->
            <div class="left-panel">
                <!-- 实时检测画面 -->
                <div class="widget video-widget">
                    <div class="widget-header">
                        <span class="widget-title">实时检测画面</span>
                        <span class="widget-badge">直播中</span>
                    </div>
                    <div class="video-container">
                        <div class="video-placeholder">
                            <div class="camera-overlay">
                                <div class="scan-line"></div>
                            </div>
                            <div class="video-stats">
                                <span>分辨率: 1920x1080</span>
                                <span>帧率: 30 FPS</span>
                                <span>码率: 4.5 Mbps</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 缺陷实时分布 -->
                <div class="widget chart-widget">
                    <div class="widget-header">
                        <select v-model="defectTimeRange" class="widget-select">
                            <option value="hour">最近1小时</option>
                            <option value="day">最近24小时</option>
                            <option value="week">最近7天</option>
                        </select>
                    </div>
                    <div class="chart-container" ref="pieChart"></div>
                </div>
            </div>

            <!-- 中间面板 - 核心指标 -->
            <div class="center-panel">
                <!-- KPI 卡片 -->
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-info">
                            <div class="kpi-label">今日检测</div>
                            <div class="kpi-value">12,580</div>
                            <div class="kpi-unit">米</div>
                        </div>
                        <div class="kpi-trend up">+12.5%</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-info">
                            <div class="kpi-label">良品率</div>
                            <div class="kpi-value">97.6</div>
                            <div class="kpi-unit">%</div>
                        </div>
                        <div class="kpi-trend up">+2.3%</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-info">
                            <div class="kpi-label">缺陷数</div>
                            <div class="kpi-value">286</div>
                            <div class="kpi-unit">个</div>
                        </div>
                        <div class="kpi-trend down">-5.2%</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-info">
                            <div class="kpi-label">检测速度</div>
                            <div class="kpi-value">85.3</div>
                            <div class="kpi-unit">米/分</div>
                        </div>
                        <div class="kpi-trend up">+1.8%</div>
                    </div>
                </div>

                <!-- 缺陷趋势图 -->
                <div class="widget chart-widget large">
                    <div class="widget-header">
                        <div class="widget-controls">
                            <select v-model="trendTimeRange" class="widget-select">
                                <option value="hour">小时</option>
                                <option value="day">日</option>
                                <option value="week">周</option>
                                <option value="month">月</option>
                            </select>
                            <select v-model="trendType" class="widget-select">
                                <option value="all">全部缺陷</option>
                                <option value="破洞">破洞</option>
                                <option value="脏污">脏污</option>
                                <option value="划痕">划痕</option>
                            </select>
                        </div>
                    </div>
                    <div class="chart-container large" ref="trendChart"></div>
                </div>

                <!-- 实时缺陷列表 -->
                <div class="widget">
                    <div class="widget-header">
                        <span class="widget-badge warning">最新 5 条</span>
                    </div>
                    <div class="alert-list">
                        <div v-for="(alert, index) in realtimeAlerts" :key="index" class="alert-item"
                            :class="alert.level">
                            <span class="alert-time">{{ alert.time }}</span>
                            <span class="alert-type" :style="{ background: getDefectColor(alert.type) }">{{ alert.type
                                }}</span>
                            <span class="alert-message">{{ alert.message }}</span>
                            <span class="alert-position">{{ alert.position }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 右侧面板 -->
            <div class="right-panel">
                <!-- 设备状态 -->
                <div class="widget">
                    <div class="widget-header">
                        <span class="widget-badge success">所有设备在线</span>
                    </div>
                    <div class="device-list">
                        <div class="device-item" v-for="device in devices" :key="device.name">
                            <div class="device-info">
                                <span class="device-name">{{ device.name }}</span>
                                <span class="device-status" :class="device.status">{{ device.status === 'online' ? '在线'
                                    : '离线' }}</span>
                            </div>
                            <div class="device-metrics">
                                <span class="metric">{{ device.metric }}</span>
                                <span class="value">{{ device.value }}</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress" :style="{ width: device.usage + '%', background: device.color }">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 缺陷排名 -->
                <div class="widget">
                    <div class="widget-header">
                        <span class="widget-badge">今日</span>
                    </div>
                    <div class="rank-list">
                        <div v-for="(item, index) in defectRank" :key="item.type" class="rank-item">
                            <div class="rank-index"
                                :class="{ gold: index === 0, silver: index === 1, bronze: index === 2 }">
                                {{ index + 1 }}
                            </div>
                            <div class="rank-type" :style="{ color: item.color }">{{ item.type }}</div>
                            <div class="rank-count">{{ item.count }}个</div>
                            <div class="rank-bar">
                                <div class="bar"
                                    :style="{ width: (item.count / maxDefectCount) * 100 + '%', background: item.color }">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 良品率仪表盘 -->
                <div class="widget">
                    <div class="widget-header">
                    </div>
                    <div class="gauge-container" ref="gaugeChart"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'

// 当前时间
const currentTime = ref('')
const updateTime = () => {
    const now = new Date()
    currentTime.value = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    })
}
setInterval(updateTime, 1000)
updateTime()

// 图表容器
const pieChart = ref(null)
const trendChart = ref(null)
const gaugeChart = ref(null)

// 图表实例
let pieInstance = null
let trendInstance = null
let gaugeInstance = null

// 筛选条件
const defectTimeRange = ref('hour')
const trendTimeRange = ref('day')
const trendType = ref('all')

// 实时告警数据
const realtimeAlerts = ref([
    { time: '14:23:05', type: '破洞', level: 'error', message: '检测到破洞, 置信度96%', position: 'X:320, Y:240' },
    { time: '14:22:30', type: '脏污', level: 'warning', message: '检测到脏污, 置信度82%', position: 'X:560, Y:180' },
    { time: '14:21:45', type: '划痕', level: 'info', message: '检测到划痕, 置信度91%', position: 'X:180, Y:420' },
    { time: '14:20:15', type: '色差', level: 'info', message: '检测到色差, 置信度79%', position: 'X:640, Y:380' },
    { time: '14:18:30', type: '毛丝', level: 'warning', message: '检测到毛丝, 置信度88%', position: 'X:420, Y:520' }
])

// 设备状态
const devices = ref([
    { name: '主摄像头', status: 'online', metric: '负载', value: '45%', usage: 45, color: '#4caf50' },
    { name: '光源', status: 'online', metric: '亮度', value: '85%', usage: 85, color: '#ff9800' },
    { name: 'PLC', status: 'online', metric: 'CPU', value: '23%', usage: 23, color: '#2196f3' },
    { name: 'GPU', status: 'online', metric: '显存', value: '3.2/8GB', usage: 40, color: '#9c27b0' },
    { name: '编码器', status: 'online', metric: '速度', value: '85m/min', usage: 85, color: '#00bcd4' }
])

// 缺陷排名
const defectRank = ref([
    { type: '破洞', count: 86, color: '#f44336' },
    { type: '脏污', count: 72, color: '#ff9800' },
    { type: '划痕', count: 54, color: '#2196f3' },
    { type: '色差', count: 38, color: '#9c27b0' },
    { type: '毛丝', count: 26, color: '#4caf50' }
])

const maxDefectCount = computed(() => Math.max(...defectRank.value.map(d => d.count)))

// 获取缺陷颜色
const getDefectColor = (type) => {
    const colors = {
        '破洞': '#f44336',
        '脏污': '#ff9800',
        '划痕': '#2196f3',
        '色差': '#9c27b0',
        '毛丝': '#4caf50'
    }
    return colors[type] || '#888'
}

// 初始化所有图表
const initCharts = () => {
    // 饼图 - 缺陷分布
    if (pieChart.value) {
        pieInstance = echarts.init(pieChart.value)
        pieInstance.setOption({
            tooltip: { trigger: 'item' },
            legend: {
                orient: 'vertical',
                left: 'left',
                textStyle: { color: '#e0e0e0' }
            },
            series: [
                {
                    name: '缺陷分布',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    center: ['60%', '50%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#1e1e1e',
                        borderWidth: 2
                    },
                    label: { show: false },
                    emphasis: {
                        scale: true,
                        label: { show: true }
                    },
                    data: [
                        { value: 86, name: '破洞', itemStyle: { color: '#f44336' } },
                        { value: 72, name: '脏污', itemStyle: { color: '#ff9800' } },
                        { value: 54, name: '划痕', itemStyle: { color: '#2196f3' } },
                        { value: 38, name: '色差', itemStyle: { color: '#9c27b0' } },
                        { value: 26, name: '毛丝', itemStyle: { color: '#4caf50' } }
                    ]
                }
            ],
            backgroundColor: 'transparent'
        })
    }

    // 趋势图
    if (trendChart.value) {
        trendInstance = echarts.init(trendChart.value)
        trendInstance.setOption({
            tooltip: { trigger: 'axis' },
            legend: {
                data: ['破洞', '脏污', '划痕', '色差', '毛丝'],
                textStyle: { color: '#e0e0e0' },
                bottom: 0
            },
            grid: { left: '5%', right: '5%', top: '10%', bottom: '15%', containLabel: true },
            xAxis: {
                type: 'category',
                data: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'],
                axisLabel: { color: '#888' },
                axisLine: { lineStyle: { color: '#3a3a3a' } }
            },
            yAxis: {
                type: 'value',
                axisLabel: { color: '#888' },
                splitLine: { lineStyle: { color: '#2a2a2a' } }
            },
            series: [
                { name: '破洞', type: 'line', data: [12, 8, 15, 10, 22, 18, 14, 20, 16, 13, 9, 11], smooth: true, symbol: 'circle', color: '#f44336' },
                { name: '脏污', type: 'line', data: [8, 12, 10, 14, 18, 16, 12, 15, 13, 10, 8, 9], smooth: true, symbol: 'circle', color: '#ff9800' },
                { name: '划痕', type: 'line', data: [5, 7, 9, 8, 12, 14, 10, 11, 9, 7, 6, 8], smooth: true, symbol: 'circle', color: '#2196f3' },
                { name: '色差', type: 'line', data: [3, 4, 6, 5, 8, 9, 7, 8, 6, 4, 3, 5], smooth: true, symbol: 'circle', color: '#9c27b0' },
                { name: '毛丝', type: 'line', data: [2, 3, 4, 3, 5, 6, 4, 5, 4, 3, 2, 3], smooth: true, symbol: 'circle', color: '#4caf50' }
            ],
            backgroundColor: 'transparent'
        })
    }

    // 仪表盘
    if (gaugeChart.value) {
        gaugeInstance = echarts.init(gaugeChart.value)
        gaugeInstance.setOption({
            series: [
                {
                    type: 'gauge',
                    center: ['50%', '60%'],
                    radius: '70%',
                    startAngle: 180,
                    endAngle: 0,
                    min: 90,
                    max: 100,
                    splitNumber: 10,
                    progress: {
                        show: true,
                        width: 15,
                        roundCap: true,
                        itemStyle: {
                            color: {
                                type: 'linear', x: 0, y: 0, x2: 1, y2: 0,
                                colorStops: [{ offset: 0, color: '#f44336' }, { offset: 0.5, color: '#ff9800' }, { offset: 1, color: '#4caf50' }]
                            }
                        }
                    },
                    axisLine: { lineStyle: { width: 15, color: [[0.97, '#2a2a2a']] } },
                    axisTick: { show: false },
                    splitLine: { show: false },
                    axisLabel: { show: false },
                    detail: {
                        offsetCenter: [0, 20],
                        valueAnimation: true,
                        fontSize: 30,
                        color: '#e0e0e0',
                        formatter: '{value}%'
                    },
                    data: [{ value: 97.6, name: '良品率' }]
                }
            ],
            backgroundColor: 'transparent'
        })
    }
}

// 窗口大小变化时自适应
const handleResize = () => {
    pieInstance?.resize()
    trendInstance?.resize()
    gaugeInstance?.resize()
}

onMounted(() => {
    initCharts()
    window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    pieInstance?.dispose()
    trendInstance?.dispose()
    gaugeInstance?.dispose()
})
</script>

<style scoped>
.dashboard-large {
    height: 100vh;
    background: #0a0a0a;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    color: #e0e0e0;
}

/* 头部 */
.header {
    height: 60px;
    background: linear-gradient(90deg, #0a0a0a 0%, #1a1a1a 100%);
    border-bottom: 1px solid #2a2a2a;
    padding: 0 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header h1 {
    font-size: 20px;
    font-weight: 600;
    color: #00bcd4;
    text-shadow: 0 0 10px rgba(0, 188, 212, 0.3);
    margin: 0;
    letter-spacing: 2px;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 20px;
}

.time-display {
    font-size: 16px;
    color: #888;
    font-family: monospace;
}

.system-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: #4caf50;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 4px;
    animation: pulse 2s infinite;
}

.status-dot.online {
    background: #4caf50;
    box-shadow: 0 0 10px #4caf50;
}

@keyframes pulse {
    0% {
        opacity: 1;
    }

    50% {
        opacity: 0.5;
    }

    100% {
        opacity: 1;
    }
}

/* 主要内容区域 */
.main-content {
    flex: 1;
    display: grid;
    grid-template-columns: 400px 1fr 350px;
    gap: 16px;
    padding: 16px;
    overflow: hidden;
}

/* 通用面板样式 */
.left-panel,
.center-panel,
.right-panel {
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow-y: auto;
    scrollbar-width: none;
}

.left-panel::-webkit-scrollbar,
.center-panel::-webkit-scrollbar,
.right-panel::-webkit-scrollbar {
    display: none;
}

.widget {
    background: rgba(30, 30, 30, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.widget-header {
    padding: 16px 20px;
    background: rgba(20, 20, 20, 0.9);
    border-bottom: 1px solid #2a2a2a;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.widget-title {
    font-size: 16px;
    font-weight: 600;
    color: #e0e0e0;
}

.widget-badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    background: #2a2a2a;
    color: #888;
}

.widget-badge.warning {
    background: #ff9800;
    color: #fff;
}

.widget-badge.success {
    background: #4caf50;
    color: #fff;
}

.widget-select {
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
}

/* 视频组件 */
.video-widget {
    height: 280px;
}

.video-container {
    height: calc(100% - 57px);
    background: #0a0a0a;
    position: relative;
    overflow: hidden;
}

.video-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #1a1a1a 25%, #0a0a0a 25%, #0a0a0a 50%, #1a1a1a 50%, #1a1a1a 75%, #0a0a0a 75%);
    background-size: 40px 40px;
    position: relative;
}

.camera-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, transparent 0%, rgba(0, 0, 0, 0.5) 100%);
}

.scan-line {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: rgba(0, 188, 212, 0.3);
    animation: scan 3s linear infinite;
    box-shadow: 0 0 20px #00bcd4;
}

@keyframes scan {
    0% {
        top: 0;
    }

    100% {
        top: 100%;
    }
}

.video-stats {
    position: absolute;
    bottom: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.7);
    background: rgba(0, 0, 0, 0.5);
    padding: 4px 8px;
    border-radius: 4px;
    backdrop-filter: blur(5px);
}

/* 图表组件 */
.chart-widget {
    height: 300px;
}

.chart-widget.large {
    height: 400px;
}

.chart-container {
    height: calc(100% - 57px);
    width: 100%;
}

.chart-container.large {
    height: calc(100% - 57px);
}

/* KPI卡片 */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.kpi-card {
    background: rgba(30, 30, 30, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00bcd4, transparent);
}

.kpi-info {
    flex: 1;
}

.kpi-label {
    font-size: 12px;
    color: #888;
    margin-bottom: 4px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 600;
    color: #e0e0e0;
    line-height: 1;
    display: inline-block;
    margin-right: 4px;
}

.kpi-unit {
    display: inline-block;
    font-size: 12px;
    color: #888;
}

.kpi-trend {
    position: absolute;
    top: 12px;
    right: 12px;
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 3px;
}

.kpi-trend.up {
    background: #4caf50;
    color: #fff;
}

.kpi-trend.down {
    background: #f44336;
    color: #fff;
}

/* 告警列表 */
.alert-list {
    padding: 12px;
    max-height: 300px;
    overflow-y: auto;
}

.alert-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    border-bottom: 1px solid #2a2a2a;
    font-size: 12px;
}

.alert-item:last-child {
    border-bottom: none;
}

.alert-item.error {
    background: rgba(244, 67, 54, 0.05);
}

.alert-item.warning {
    background: rgba(255, 152, 0, 0.05);
}

.alert-item.info {
    background: rgba(33, 150, 243, 0.05);
}

.alert-time {
    color: #888;
    min-width: 70px;
}

.alert-type {
    padding: 2px 6px;
    border-radius: 3px;
    color: #fff;
    font-size: 11px;
    min-width: 40px;
    text-align: center;
}

.alert-message {
    flex: 1;
    color: #e0e0e0;
}

.alert-position {
    color: #888;
    font-family: monospace;
}

/* 设备列表 */
.device-list {
    padding: 16px;
}

.device-item {
    margin-bottom: 16px;
}

.device-item:last-child {
    margin-bottom: 0;
}

.device-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 13px;
}

.device-name {
    color: #e0e0e0;
}

.device-status {
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 3px;
}

.device-status.online {
    background: #4caf50;
    color: #fff;
}

.device-status.offline {
    background: #f44336;
    color: #fff;
}

.device-metrics {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #888;
    margin-bottom: 4px;
}

.device-metrics .value {
    color: #e0e0e0;
}

/* 排名列表 */
.rank-list {
    padding: 12px;
}

.rank-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid #2a2a2a;
}

.rank-item:last-child {
    border-bottom: none;
}

.rank-index {
    width: 24px;
    height: 24px;
    border-radius: 12px;
    background: #1e1e1e;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
}

.rank-index.gold {
    background: #ffd700;
    color: #000;
}

.rank-index.silver {
    background: #c0c0c0;
    color: #000;
}

.rank-index.bronze {
    background: #cd7f32;
    color: #000;
}

.rank-type {
    width: 60px;
    font-size: 13px;
    font-weight: 500;
}

.rank-count {
    width: 50px;
    font-size: 12px;
    color: #888;
}

.rank-bar {
    flex: 1;
    height: 6px;
    background: #1e1e1e;
    border-radius: 3px;
    overflow: hidden;
}

.rank-bar .bar {
    height: 100%;
    border-radius: 3px;
}

/* 仪表盘 */
.gauge-container {
    height: 200px;
    width: 100%;
}

/* 进度条通用样式 */
.progress-bar {
    height: 4px;
    background: #1e1e1e;
    border-radius: 2px;
    overflow: hidden;
}

.progress-bar .progress {
    height: 100%;
    border-radius: 2px;
}

/* 响应式 */
@media (max-width: 1600px) {
    .main-content {
        grid-template-columns: 350px 1fr 300px;
    }
}

@media (max-width: 1400px) {
    .kpi-grid {
        grid-template-columns: 1fr;
    }
}
</style>