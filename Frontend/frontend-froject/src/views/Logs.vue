<!-- src/views/Logs.vue -->
<!-- 日志与报表页面 - 历史数据追溯 -->
<template>
  <div class="logs">
    <h2 class="page-title">日志与报表</h2>
    <p class="page-desc">查看历史检测记录、生成报表、追溯问题</p>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-label">今日检测</div>
          <div class="stat-value">1,234 <small>次</small></div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-label">今日缺陷</div>
          <div class="stat-value">28 <small>个</small></div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-label">良品率</div>
          <div class="stat-value">97.6%</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-content">
          <div class="stat-label">平均耗时</div>
          <div class="stat-value">0.23 <small>秒</small></div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-tabs">
        <button class="tab-btn" :class="{ active: activeChart === 'defect' }" @click="activeChart = 'defect'">缺陷趋势</button>
        <button class="tab-btn" :class="{ active: activeChart === 'yield' }" @click="activeChart = 'yield'">良品率</button>
        <button class="tab-btn" :class="{ active: activeChart === 'speed' }" @click="activeChart = 'speed'">检测速度</button>
      </div>

      <div class="chart-container">
        <!-- 缺陷趋势图 -->
        <div v-if="activeChart === 'defect'" class="chart">
          <div class="chart-header">
            <h3>过去7天缺陷数量</h3>
            <select v-model="defectChartType">
              <option value="bar">柱状图</option>
              <option value="line">折线图</option>
            </select>
          </div>
          <div class="chart-bars">
            <div v-for="(day, index) in defectData" :key="index" class="chart-bar-item">
              <div class="bar-label">{{ day.date }}</div>
              <div class="bar-container">
                <div class="bar" :style="{ height: day.count * 3 + 'px', background: getBarColor(day.count) }"></div>
              </div>
              <div class="bar-value">{{ day.count }}</div>
            </div>
          </div>
        </div>

        <!-- 良品率图 -->
        <div v-if="activeChart === 'yield'" class="chart">
          <div class="chart-header">
            <h3>过去7天良品率</h3>
          </div>
          <div class="yield-chart">
            <div class="yield-circle">
              <svg viewBox="0 0 100 100" class="circular-chart">
                <circle class="circle-bg" cx="50" cy="50" r="40" fill="none" stroke="#3a3a3a" stroke-width="8"/>
                <circle class="circle-progress" cx="50" cy="50" r="40" fill="none" stroke="#4caf50" 
                        stroke-width="8" :stroke-dasharray="circumference" 
                        :stroke-dashoffset="circumference - (circumference * yieldRate / 100)"/>
              </svg>
              <div class="yield-text">{{ yieldRate }}%</div>
            </div>
            <div class="yield-stats">
              <div class="yield-stat-item">
                <span class="stat-dot good"></span>
                <span>良品: 1,206</span>
              </div>
              <div class="yield-stat-item">
                <span class="stat-dot bad"></span>
                <span>缺陷: 28</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 检测速度图 -->
        <div v-if="activeChart === 'speed'" class="chart">
          <div class="chart-header">
            <h3>过去7天检测速度 (米/分钟)</h3>
          </div>
          <div class="speed-chart">
            <div v-for="(speed, index) in speedData" :key="index" class="speed-line">
              <div class="speed-point" :style="{ bottom: speed * 0.5 + 'px' }">
                <span class="speed-tooltip">{{ speed }} m/min</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 日志列表 -->
    <div class="logs-section">
      <div class="section-header">
        <h3>实时日志</h3>
        <div class="log-controls">
          <select v-model="logFilter" class="filter-select">
            <option value="all">全部日志</option>
            <option value="info">信息</option>
            <option value="warning">警告</option>
            <option value="error">错误</option>
          </select>
          <button class="btn secondary small" @click="exportLogs">导出</button>
          <button class="btn secondary small" @click="clearLogs">清除</button>
        </div>
      </div>

      <div class="log-table">
        <div class="log-table-header">
          <div class="col-time">时间</div>
          <div class="col-level">级别</div>
          <div class="col-message">消息</div>
          <div class="col-user">操作人</div>
        </div>
        <div class="log-table-body">
          <div v-for="(log, index) in filteredLogs" :key="index" 
               class="log-row" 
               :class="log.level">
            <div class="col-time">{{ log.time }}</div>
            <div class="col-level">
              <span class="level-badge" :class="log.level">{{ log.level }}</span>
            </div>
            <div class="col-message">{{ log.message }}</div>
            <div class="col-user">{{ log.user }}</div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <button class="page-btn" :disabled="logPage === 1" @click="logPage--">←</button>
        <span class="page-info">{{ logPage }} / {{ logTotalPages }}</span>
        <button class="page-btn" :disabled="logPage === logTotalPages" @click="logPage++">→</button>
      </div>
    </div>

    <!-- 报表导出 -->
    <div class="reports-section">
      <h3>报表导出</h3>
      
      <div class="report-grid">
        <div class="report-card">
          <div class="report-info">
            <h4>日报表</h4>
            <p>每日检测统计、缺陷分布</p>
          </div>
          <button class="btn secondary small" @click="exportReport('daily')">导出</button>
        </div>

        <div class="report-card">
          <div class="report-info">
            <h4>周报表</h4>
            <p>趋势分析、良品率变化</p>
          </div>
          <button class="btn secondary small" @click="exportReport('weekly')">导出</button>
        </div>

        <div class="report-card">
          <div class="report-info">
            <h4>月报表</h4>
            <p>月度总结、缺陷TOP N</p>
          </div>
          <button class="btn secondary small" @click="exportReport('monthly')">导出</button>
        </div>

        <div class="report-card">
          <div class="report-info">
            <h4>缺陷图库</h4>
            <p>所有NG图片打包下载</p>
          </div>
          <button class="btn secondary small" @click="exportReport('images')">导出</button>
        </div>
      </div>

      <div class="custom-report">
        <h4>自定义报表</h4>
        <div class="date-range">
          <input type="date" v-model="startDate" class="date-input">
          <span>至</span>
          <input type="date" v-model="endDate" class="date-input">
          <button class="btn primary small" @click="generateCustomReport">生成报表</button>
        </div>
      </div>
    </div>

    <!-- NG图片留存 -->
    <div class="images-section">
      <h3>NG图片留存</h3>
      
      <div class="image-grid">
        <div v-for="i in 8" :key="i" class="image-card">
          <div class="image-preview" :style="{ background: getImageColor(i) }">
            <span class="image-time">14:{{ 20 + i }}:{{ 30 + i }}</span>
            <span class="image-type" :style="{ background: getDefectColor(i) }">破洞</span>
          </div>
          <div class="image-info">
            <span>缺陷 #{{ 100 + i }}</span>
            <button class="btn-icon small">编辑</button>
          </div>
        </div>
      </div>
      
      <div class="image-footer">
        <button class="btn secondary small">加载更多</button>
        <span class="image-total">共 24 张图片</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 图表切换
const activeChart = ref('defect')
const defectChartType = ref('bar')

// 图表数据
const defectData = ref([
  { date: '03/10', count: 12 },
  { date: '03/11', count: 8 },
  { date: '03/12', count: 15 },
  { date: '03/13', count: 10 },
  { date: '03/14', count: 22 },
  { date: '03/15', count: 18 },
  { date: '03/16', count: 14 }
])

const speedData = ref([85, 82, 88, 86, 84, 87, 85])

const yieldRate = ref(97.6)
const circumference = 2 * Math.PI * 40

// 日志数据
const logs = ref([
  { time: '14:23:05', level: 'info', message: '检测完成，批次 #12345', user: '系统' },
  { time: '14:22:30', level: 'warning', message: 'GPU温度达到65°C', user: '系统' },
  { time: '14:21:15', level: 'info', message: '检测到缺陷 #12，类型: 破洞', user: '系统' },
  { time: '14:20:45', level: 'error', message: '摄像头通信超时，已重连', user: '系统' },
  { time: '14:18:22', level: 'info', message: '参数调整: 置信度阈值改为70%', user: '工程师A' },
  { time: '14:15:10', level: 'info', message: '启动检测，产品型号: 纯棉布A型', user: '操作员B' },
  { time: '14:10:05', level: 'warning', message: '光源亮度下降，建议检查', user: '系统' },
  { time: '13:58:30', level: 'info', message: '检测完成，批次 #12344', user: '系统' }
])

const logFilter = ref('all')
const logPage = ref(1)
const pageSize = 5

// 过滤后的日志
const filteredLogs = computed(() => {
  let filtered = logs.value
  if (logFilter.value !== 'all') {
    filtered = filtered.filter(log => log.level === logFilter.value)
  }
  const start = (logPage.value - 1) * pageSize
  return filtered.slice(start, start + pageSize)
})

const logTotalPages = computed(() => {
  let filtered = logs.value
  if (logFilter.value !== 'all') {
    filtered = filtered.filter(log => log.level === logFilter.value)
  }
  return Math.ceil(filtered.length / pageSize)
})

// 报表日期
const startDate = ref('2024-03-01')
const endDate = ref('2024-03-16')

// 工具函数
const getBarColor = (count) => {
  if (count > 20) return '#f44336'
  if (count > 10) return '#ff9800'
  return '#4caf50'
}

const getImageColor = (i) => {
  const colors = ['#f44336', '#ff9800', '#2196f3', '#4caf50', '#9c27b0']
  return colors[i % colors.length]
}

const getDefectColor = (i) => {
  const colors = ['#f44336', '#ff9800', '#2196f3', '#4caf50', '#9c27b0']
  return colors[i % colors.length]
}

// 操作函数
const exportLogs = () => {
  console.log('导出日志')
  alert('日志导出中...')
}

const clearLogs = () => {
  console.log('清除日志')
  alert('日志已清除')
}

const exportReport = (type) => {
  console.log('导出报表:', type)
  alert(`${type}报表导出中...`)
}

const generateCustomReport = () => {
  console.log('生成自定义报表', startDate.value, endDate.value)
  alert(`生成 ${startDate.value} 至 ${endDate.value} 报表`)
}
</script>

<style scoped>
.logs {
  height: 100%;
  overflow-y: auto;
  padding-right: 8px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #e0e0e0;
  margin-bottom: 4px;
}

.page-desc {
  color: #888;
  font-size: 14px;
  margin-bottom: 24px;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #3a3a3a;
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 12px;
  color: #888;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #e0e0e0;
}

.stat-value small {
  font-size: 12px;
  color: #888;
  font-weight: normal;
  margin-left: 4px;
}

/* 图表区域 */
.charts-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.chart-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  border-bottom: 1px solid #3a3a3a;
  padding-bottom: 12px;
}

.tab-btn {
  background: none;
  border: none;
  color: #888;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 13px;
  border-radius: 4px;
}

.tab-btn:hover {
  background: #3a3a3a;
  color: #e0e0e0;
}

.tab-btn.active {
  background: #00bcd4;
  color: #fff;
}

.chart-container {
  min-height: 300px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 16px;
  color: #e0e0e0;
  margin: 0;
}

.chart-header select {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 4px 8px;
  border-radius: 4px;
}

/* 柱状图 */
.chart-bars {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 200px;
}

.chart-bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 40px;
}

.bar-label {
  font-size: 11px;
  color: #888;
  margin-bottom: 8px;
}

.bar-container {
  width: 30px;
  height: 150px;
  background: #1e1e1e;
  border-radius: 4px;
  position: relative;
  margin-bottom: 4px;
}

.bar {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: #00bcd4;
  border-radius: 4px;
  transition: height 0.3s;
}

.bar-value {
  font-size: 11px;
  color: #e0e0e0;
}

/* 环形图 */
.yield-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  padding: 20px;
}

.yield-circle {
  position: relative;
  width: 150px;
  height: 150px;
}

.circular-chart {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.circle-bg {
  stroke: #3a3a3a;
}

.circle-progress {
  stroke: #4caf50;
  transition: stroke-dashoffset 0.3s;
}

.yield-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 28px;
  font-weight: 600;
  color: #4caf50;
}

.yield-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.yield-stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #e0e0e0;
}

.stat-dot {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.stat-dot.good {
  background: #4caf50;
}

.stat-dot.bad {
  background: #f44336;
}

/* 速度图 */
.speed-chart {
  height: 200px;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  padding: 20px 0;
}

.speed-line {
  position: relative;
  width: 2px;
  height: 150px;
  background: #3a3a3a;
}

.speed-point {
  position: absolute;
  left: -4px;
  width: 10px;
  height: 10px;
  background: #00bcd4;
  border-radius: 5px;
  cursor: pointer;
}

.speed-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #1e1e1e;
  color: #e0e0e0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  white-space: nowrap;
  display: none;
  border: 1px solid #3a3a3a;
}

.speed-point:hover .speed-tooltip {
  display: block;
}

/* 日志区域 */
.logs-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0;
}

.log-controls {
  display: flex;
  gap: 8px;
}

.filter-select {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.btn.small {
  padding: 6px 12px;
  font-size: 12px;
}

.log-table {
  border: 1px solid #3a3a3a;
  border-radius: 4px;
  overflow: hidden;
}

.log-table-header {
  display: grid;
  grid-template-columns: 100px 80px 1fr 100px;
  background: #1e1e1e;
  padding: 10px 16px;
  font-size: 12px;
  color: #888;
  border-bottom: 1px solid #3a3a3a;
}

.log-table-body {
  max-height: 300px;
  overflow-y: auto;
}

.log-row {
  display: grid;
  grid-template-columns: 100px 80px 1fr 100px;
  padding: 8px 16px;
  font-size: 12px;
  color: #e0e0e0;
  border-bottom: 1px solid #2a2a2a;
}

.log-row:hover {
  background: #2a2a2a;
}

.log-row.warning {
  background: rgba(255, 152, 0, 0.1);
}

.log-row.error {
  background: rgba(244, 67, 54, 0.1);
}

.level-badge {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
}

.level-badge.info {
  background: #2196f3;
  color: #fff;
}

.level-badge.warning {
  background: #ff9800;
  color: #fff;
}

.level-badge.error {
  background: #f44336;
  color: #fff;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}

.page-btn {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  cursor: pointer;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  color: #888;
}

/* 报表区域 */
.reports-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.reports-section h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0 0 16px 0;
}

.report-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.report-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #1e1e1e;
  border-radius: 6px;
  border: 1px solid #3a3a3a;
}


.report-info {
  flex: 1;
}

.report-info h4 {
  font-size: 14px;
  color: #e0e0e0;
  margin: 0 0 4px 0;
}

.report-info p {
  font-size: 11px;
  color: #888;
  margin: 0;
}

.custom-report {
  padding: 16px;
  background: #1e1e1e;
  border-radius: 6px;
  border: 1px solid #3a3a3a;
}

.custom-report h4 {
  font-size: 14px;
  color: #e0e0e0;
  margin: 0 0 12px 0;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-input {
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 12px;
}

/* NG图片区域 */
.images-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.images-section h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0 0 16px 0;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.image-card {
  background: #1e1e1e;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #3a3a3a;
}

.image-preview {
  aspect-ratio: 1;
  position: relative;
}

.image-time {
  position: absolute;
  bottom: 4px;
  left: 4px;
  background: rgba(0,0,0,0.7);
  color: #fff;
  padding: 2px 4px;
  font-size: 10px;
  border-radius: 2px;
}

.image-type {
  position: absolute;
  top: 4px;
  right: 4px;
  color: #fff;
  padding: 2px 4px;
  font-size: 10px;
  border-radius: 2px;
}

.image-info {
  padding: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: #888;
}

.image-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-total {
  font-size: 12px;
  color: #888;
}

.btn-icon.small {
  font-size: 14px;
  padding: 2px 4px;
}

.btn.primary {
  background: #00bcd4;
  color: #fff;
}

.btn.primary:hover {
  background: #00acc1;
}

.btn.secondary {
  background: #3a3a3a;
  color: #e0e0e0;
}

.btn.secondary:hover {
  background: #4a4a4a;
}

/* 响应式 */
@media (max-width: 1400px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .image-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1200px) {
  .report-grid {
    grid-template-columns: 1fr;
  }
  
  .date-range {
    flex-wrap: wrap;
  }
  
  .image-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 900px) {
  .log-table-header,
  .log-row {
    grid-template-columns: 80px 70px 1fr 80px;
    font-size: 11px;
  }
  
  .yield-chart {
    flex-direction: column;
  }
}
</style>