<!-- src/views/Diagnostics.vue -->
<!-- 系统诊断页面 - 健康状态监控 -->
<template>
  <div class="diagnostics">
    <h2 class="page-title">系统诊断</h2>
    <p class="page-desc">监控系统健康状态，快速定位故障</p>

    <!-- 整体状态 -->
    <div class="system-status">
      <div class="status-card" :class="systemHealth">
        <div class="status-icon">{{ healthIcon }}</div>
        <div class="status-info">
          <div class="status-label">系统状态</div>
          <div class="status-value">{{ healthText }}</div>
        </div>
      </div>
      <div class="uptime-card">
        <div class="uptime-label">持续运行时间</div>
        <div class="uptime-value">12天 7小时 23分钟</div>
      </div>
    </div>

    <!-- 通信状态 -->
    <div class="section">
      <h3>通信状态</h3>
      <div class="status-grid">
        <div v-for="item in communicationStatus" :key="item.name" class="status-item">
          <div class="item-header">
            <span class="item-name">{{ item.name }}</span>
            <span class="status-badge" :class="item.status">{{ item.status === 'online' ? '在线' : '离线' }}</span>
          </div>
          <div class="item-detail">
            <span class="detail-label">延迟</span>
            <span class="detail-value" :class="{ warning: item.latency > 100 }">{{ item.latency }}ms</span>
          </div>
          <div class="item-detail">
            <span class="detail-label">最后通信</span>
            <span class="detail-value">{{ item.lastSeen }}</span>
          </div>
          <div class="progress-bar">
            <div class="progress" :style="{ width: item.quality + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 硬件自检 -->
    <div class="section">
      <h3>硬件自检</h3>
      <div class="hardware-grid">
        <!-- 摄像头 -->
        <div class="hardware-card">
          <div class="card-header">
            <h4>摄像头</h4>
            <span class="test-result pass">通过</span>
          </div>
          <div class="hardware-tests">
            <div class="test-item">
              <span>图像采集</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>自动对焦</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>白平衡</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>帧率稳定</span>
              <span class="test-pass">✓</span>
            </div>
          </div>
          <button class="btn secondary small" @click="runTest('camera')">重新测试</button>
        </div>

        <!-- 光源 -->
        <div class="hardware-card">
          <div class="card-header">
            <h4>光源</h4>
            <span class="test-result warn">需校准</span>
          </div>
          <div class="hardware-tests">
            <div class="test-item">
              <span>亮度</span>
              <span class="test-warn">85%</span>
            </div>
            <div class="test-item">
              <span>均匀性</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>色温</span>
              <span class="test-pass">5500K</span>
            </div>
            <div class="test-item">
              <span>使用寿命</span>
              <span class="test-warn">2300h</span>
            </div>
          </div>
          <button class="btn secondary small" @click="runTest('light')">重新测试</button>
        </div>

        <!-- PLC -->
        <div class="hardware-card">
          <div class="card-header">
            <h4>PLC</h4>
            <span class="test-result pass">在线</span>
          </div>
          <div class="hardware-tests">
            <div class="test-item">
              <span>通信</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>IO状态</span>
              <span class="test-pass">正常</span>
            </div>
            <div class="test-item">
              <span>扫描周期</span>
              <span class="test-pass">12ms</span>
            </div>
            <div class="test-item">
              <span>错误计数</span>
              <span class="test-pass">0</span>
            </div>
          </div>
          <button class="btn secondary small" @click="runTest('plc')">重新测试</button>
        </div>

        <!-- 编码器 -->
        <div class="hardware-card">
          <div class="card-header">
            <h4>编码器</h4>
            <span class="test-result pass">正常</span>
          </div>
          <div class="hardware-tests">
            <div class="test-item">
              <span>脉冲计数</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>速度匹配</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>零位信号</span>
              <span class="test-pass">✓</span>
            </div>
            <div class="test-item">
              <span>AB相</span>
              <span class="test-pass">正常</span>
            </div>
          </div>
          <button class="btn secondary small" @click="runTest('encoder')">重新测试</button>
        </div>
      </div>
    </div>

    <!-- 性能监控 -->
    <div class="section">
      <h3>性能监控</h3>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-header">
            <span class="metric-label">GPU 使用率</span>
          </div>
          <div class="metric-value">76%</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress" style="width: 76%"></div>
            </div>
          </div>
          <div class="metric-details">
            <span>温度: 65°C</span>
            <span>显存: 3.2/8GB</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <span class="metric-label">CPU 使用率</span>
          </div>
          <div class="metric-value">32%</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress" style="width: 32%"></div>
            </div>
          </div>
          <div class="metric-details">
            <span>温度: 52°C</span>
            <span>负载: 2.4</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <span class="metric-label">内存使用</span>
          </div>
          <div class="metric-value">4.2/16GB</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress" style="width: 26%"></div>
            </div>
          </div>
          <div class="metric-details">
            <span>缓存: 1.2GB</span>
            <span>交换: 0.3GB</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <span class="metric-label">检测耗时</span>
          </div>
          <div class="metric-value">0.23秒</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress" style="width: 23%"></div>
            </div>
          </div>
          <div class="metric-details">
            <span>最大: 0.31秒</span>
            <span>最小: 0.18秒</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <span class="metric-label">丢帧率</span>
          </div>
          <div class="metric-value">0.3%</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress" style="width: 3%"></div>
            </div>
          </div>
          <div class="metric-details">
            <span>总帧数: 1.2M</span>
            <span>丢帧: 3.6K</span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-header">
            <span class="metric-label">系统温度</span>
          </div>
          <div class="metric-value">48°C</div>
          <div class="metric-progress">
            <div class="progress-bar">
              <div class="progress" style="width: 48%"></div>
            </div>
          </div>
          <div class="metric-details">
            <span>主板: 42°C</span>
            <span>硬盘: 38°C</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 日志诊断 -->
    <div class="section">
      <h3>最近错误日志</h3>
      <div class="error-log">
        <div class="error-item" v-for="i in 5" :key="i">
          <span class="error-time">14:{{ 20 + i }}:{{ 30 + i }}</span>
          <span class="error-level error">ERROR</span>
          <span class="error-message">检测超时，帧率下降至 15fps</span>
          <button class="error-action">详情</button>
        </div>
        <div class="error-item warning">
          <span class="error-time">13:45:12</span>
          <span class="error-level warn">WARN</span>
          <span class="error-message">光源亮度低于阈值，建议检查</span>
          <button class="error-action">详情</button>
        </div>
        <div class="error-item">
          <span class="error-time">13:22:30</span>
          <span class="error-level info">INFO</span>
          <span class="error-message">系统自检完成，所有硬件正常</span>
          <button class="error-action">详情</button>
        </div>
      </div>
    </div>

    <!-- 诊断工具 -->
    <div class="section">
      <h3>诊断工具</h3>
      <div class="tools-grid">
        <div class="tool-card">
          <div class="tool-info">
            <h4>网络诊断</h4>
            <p>测试各设备网络连通性</p>
          </div>
          <button class="btn secondary small" @click="runDiagnostic('network')">运行</button>
        </div>

        <div class="tool-card">
          <div class="tool-info">
            <h4>图像质量测试</h4>
            <p>检测摄像头清晰度、噪点</p>
          </div>
          <button class="btn secondary small" @click="runDiagnostic('image')">运行</button>
        </div>

        <div class="tool-card">
          <div class="tool-info">
            <h4>性能基准测试</h4>
            <p>测试系统处理能力</p>
          </div>
          <button class="btn secondary small" @click="runDiagnostic('performance')">运行</button>
        </div>

        <div class="tool-card">
          <div class="tool-info">
            <h4>生成诊断报告</h4>
            <p>导出完整系统诊断信息</p>
          </div>
          <button class="btn primary small" @click="generateReport">生成报告</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 系统健康状态
const systemHealth = ref('good')
const healthIcon = computed(() => {
  return {
    good: '✓',
    warning: '⚠️',
    error: '✗'
  }[systemHealth.value]
})
const healthText = computed(() => {
  return {
    good: '健康',
    warning: '注意',
    error: '故障'
  }[systemHealth.value]
})

// 通信状态
const communicationStatus = ref([
  { name: '主摄像头', status: 'online', latency: 23, lastSeen: '刚刚', quality: 98 },
  { name: '副摄像头', status: 'online', latency: 45, lastSeen: '2秒前', quality: 95 },
  { name: 'PLC', status: 'online', latency: 12, lastSeen: '刚刚', quality: 100 },
  { name: '光源控制器', status: 'online', latency: 56, lastSeen: '1秒前', quality: 92 },
  { name: '编码器', status: 'online', latency: 8, lastSeen: '刚刚', quality: 100 },
  { name: 'AI服务', status: 'online', latency: 0, lastSeen: '刚刚', quality: 100 }
])

// 运行测试
const runTest = (device) => {
  console.log('运行测试:', device)
  alert(`正在测试 ${device}...`)
}

// 运行诊断工具
const runDiagnostic = (tool) => {
  console.log('运行诊断工具:', tool)
  alert(`正在运行 ${tool} 诊断...`)
}

// 生成报告
const generateReport = () => {
  console.log('生成诊断报告')
  alert('诊断报告生成中...')
}
</script>

<style scoped>
.diagnostics {
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

/* 系统状态 */
.system-status {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.status-card {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-card.good {
  border-left: 4px solid #4caf50;
}

.status-card.warning {
  border-left: 4px solid #ff9800;
}

.status-card.error {
  border-left: 4px solid #f44336;
}

.status-icon {
  width: 48px;
  height: 48px;
  border-radius: 24px;
  background: #1e1e1e;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.status-info {
  flex: 1;
}

.status-label {
  font-size: 12px;
  color: #888;
  margin-bottom: 4px;
}

.status-value {
  font-size: 24px;
  font-weight: 600;
  color: #e0e0e0;
}

.uptime-card {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.uptime-label {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
}

.uptime-value {
  font-size: 20px;
  font-weight: 600;
  color: #00bcd4;
}

/* 通用区块样式 */
.section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.section h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0 0 16px 0;
}

/* 通信状态网格 */
.status-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.status-item {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 16px;
  border: 1px solid #3a3a3a;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
}

.status-badge {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
}

.status-badge.online {
  background: #4caf50;
  color: #fff;
}

.status-badge.offline {
  background: #f44336;
  color: #fff;
}

.item-detail {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
}

.detail-label {
  color: #888;
}

.detail-value {
  color: #e0e0e0;
}

.detail-value.warning {
  color: #ff9800;
}

.progress-bar {
  height: 4px;
  background: #2a2a2a;
  border-radius: 2px;
  overflow: hidden;
  margin-top: 8px;
}

.progress {
  height: 100%;
  background: #00bcd4;
  border-radius: 2px;
}

/* 硬件自检 */
.hardware-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.hardware-card {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 16px;
  border: 1px solid #3a3a3a;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.card-header h4 {
  flex: 1;
  font-size: 14px;
  color: #e0e0e0;
  margin: 0;
}

.test-result {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
}

.test-result.pass {
  background: #4caf50;
  color: #fff;
}

.test-result.warn {
  background: #ff9800;
  color: #fff;
}

.test-result.fail {
  background: #f44336;
  color: #fff;
}

.hardware-tests {
  margin-bottom: 16px;
}

.test-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 12px;
  border-bottom: 1px solid #2a2a2a;
}

.test-item span:first-child {
  color: #888;
}

.test-pass {
  color: #4caf50;
}

.test-warn {
  color: #ff9800;
}

/* 性能监控 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.metric-card {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 16px;
  border: 1px solid #3a3a3a;
}

.metric-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.metric-label {
  font-size: 13px;
  color: #888;
}

.metric-value {
  font-size: 24px;
  font-weight: 600;
  color: #00bcd4;
  margin-bottom: 12px;
}

.metric-progress {
  margin-bottom: 12px;
}

.metric-progress .progress-bar {
  margin-top: 0;
}

.metric-details {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #888;
}

/* 错误日志 */
.error-log {
  background: #1e1e1e;
  border-radius: 6px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
}

.error-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #2a2a2a;
  gap: 16px;
}

.error-item:last-child {
  border-bottom: none;
}

.error-item.warning {
  background: rgba(255, 152, 0, 0.05);
}

.error-item.error {
  background: rgba(244, 67, 54, 0.05);
}

.error-time {
  width: 100px;
  font-size: 12px;
  color: #888;
}

.error-level {
  width: 60px;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 3px;
  text-align: center;
}

.error-level.error {
  background: #f44336;
  color: #fff;
}

.error-level.warn {
  background: #ff9800;
  color: #fff;
}

.error-level.info {
  background: #2196f3;
  color: #fff;
}

.error-message {
  flex: 1;
  font-size: 13px;
  color: #e0e0e0;
}

.error-action {
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #888;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
}

.error-action:hover {
  background: #3a3a3a;
  color: #fff;
}

/* 诊断工具 */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.tool-card {
  background: #1e1e1e;
  border-radius: 6px;
  padding: 16px;
  border: 1px solid #3a3a3a;
  display: flex;
  align-items: center;
  gap: 16px;
}

.tool-info {
  flex: 1;
}

.tool-info h4 {
  font-size: 14px;
  color: #e0e0e0;
  margin: 0 0 4px 0;
}

.tool-info p {
  font-size: 11px;
  color: #888;
  margin: 0;
}

.btn.small {
  padding: 6px 12px;
  font-size: 12px;
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
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .hardware-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .system-status {
    grid-template-columns: 1fr;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .status-grid,
  .hardware-grid,
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .error-item {
    flex-wrap: wrap;
  }
  
  .error-time {
    width: auto;
  }
  
  .error-message {
    width: 100%;
    order: 1;
  }
}
</style>