<!-- src/views/Dashboard.vue -->
<!-- 对于中间视频实时播放和基础参数仪表盘的设置 -->
<template>
  <div class="dashboard">
    <!-- 上部：视频播放器 - 固定高度，不可调节 -->
    <div class="section video-section" :style="{ height: videoHeight + 'px' }">
      <div class="video-player">
        <div class="player-header">
          <span class="status-badge running">检测中</span>
          <span class="current-time">{{ currentTime }}</span>
        </div>

    <div class="video-container">
      <img 
        v-if="videoStreamUrl" 
        :src="videoStreamUrl" 
        class="video-feed"
        alt="实时检测画面"
      />
      <div v-else class="video-placeholder">
        <span>视频流加载中...</span>
      </div>
    </div>

        <div class="control-bar">
          <div class="control-buttons">
            <button class="control-btn">⏯️</button>
            <button class="control-btn">⏹️</button>
            <button class="control-btn">⏪</button>
            <button class="control-btn">⏩</button>
          </div>

          <div class="timeline-container">
            <div class="progress-bar">
              <div class="progress" style="width: 45%"></div>
            </div>
            <div class="time-display">
              <span class="current">14:23:05</span>
              <span class="separator">/</span>
              <span class="total">14:53:05</span>
            </div>
          </div>

          <div class="buffer-info">
            <span class="buffer-text">缓存: 98%</span>
          </div>
        </div>

        <div class="defect-timeline">
          <div class="marker" style="left: 15%" title="破洞 14:23:05"></div>
          <div class="marker" style="left: 35%" title="脏污 14:25:30"></div>
          <div class="marker" style="left: 65%" title="划痕 14:28:15"></div>
          <div class="marker" style="left: 82%" title="破洞 14:30:45"></div>
        </div>
      </div>
    </div>


    <!-- 中部：统计卡片 - 可调节高度 -->
    <div class="section stats-section" :style="{ height: statsHeight + 'px' }">
      <div class="stats-header">
        <h3>实时统计</h3>
        <span class="stats-update">更新于 {{ currentTime }}</span>
      </div>
      <div class="stats-scroll-area">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">当前检测速度</div>
            <div class="stat-value">85.3 <small>米/分钟</small></div>
            <div class="stat-trend up">+2.5%</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">缺陷率</div>
            <div class="stat-value">2.4%</div>
            <div class="stat-trend down">-1.2%</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">良品率</div>
            <div class="stat-value">97.6%</div>
            <div class="stat-trend up">+0.8%</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">今日总产量</div>
            <div class="stat-value">12,580 <small>米</small></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">今日检测次数</div>
            <div class="stat-value">1,234 <small>次</small></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">平均检测时间</div>
            <div class="stat-value">0.23 <small>秒</small></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">GPU使用率</div>
            <div class="stat-value">76%</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">内存使用</div>
            <div class="stat-value">4.2 <small>GB</small></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">CPU温度</div>
            <div class="stat-value">52°C</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">检测线程</div>
            <div class="stat-value">4 <small>个</small></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">缓存使用</div>
            <div class="stat-value">2.1 <small>GB</small></div>
          </div>
          <div class="stat-card">
            <div class="stat-label">网络状态</div>
            <div class="stat-value">稳定</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 下部：日志/其他内容 - 自动占满剩余高度 -->
    <div class="section log-section">
      <div class="log-header">
        <h3>实时日志</h3>
        <div class="log-controls">
          <button class="log-btn">清除</button>
          <button class="log-btn">导出</button>
        </div>
      </div>
      <div class="log-content">
        <div v-for="i in 8" :key="i" class="log-item">
          <span class="log-time">14:{{ 20 + i }}:{{ 30 + i }}</span>
          <span class="log-level info">INFO</span>
          <span class="log-message">检测到缺陷 #{{ i }}，类型: 破洞，置信度: 96%</span>
        </div>
        <div class="log-item warning">
          <span class="log-time">14:28:15</span>
          <span class="log-level warn">WARN</span>
          <span class="log-message">GPU温度偏高，建议检查散热</span>
        </div>
        <div class="log-item error">
          <span class="log-time">14:25:30</span>
          <span class="log-level error">ERROR</span>
          <span class="log-message">检测超时，帧率下降</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
const videoStreamUrl = ref('http://localhost:5000/video_feed')
const currentTime = ref('')
const videoHeight = ref(900)  // 视频区域固定高度
const statsHeight = ref(400)  // 统计区域初始高度



</script>

<style scoped>
.video-feed {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  gap: 2px;
  position: relative;
  scrollbar-width: thin;
  scrollbar-color: #4a4a4a #2a2a2a;
}

/* 自定义整个dashboard的滚动条 */
.dashboard::-webkit-scrollbar {
  width: 8px;
}

.dashboard::-webkit-scrollbar-track {
  background: #2a2a2a;
  border-radius: 4px;
}

.dashboard::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 4px;
  transition: background 0.2s;
}

.dashboard::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

.dashboard::-webkit-scrollbar-button {
  display: none;
}

/* 每个区域的基础样式 */
.section {
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 视频区域 - 固定高度，无过渡效果 */
.video-section {
  flex-shrink: 0;
}

.video-player {
  height: 100%;
  background: #1a1a1a;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.player-header {
  padding: 10px 16px;
  background: #2a2a2a;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
}

.status-badge.running {
  background: #4caf50;
  color: #fff;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }

  50% {
    opacity: 0.8;
  }

  100% {
    opacity: 1;
  }
}

.video-container {
  flex: 1;
  min-height: 0;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-placeholder {
  color: #666;
  font-size: 14px;
  position: relative;
}

.video-placeholder::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  border: 2px solid #00bcd4;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: translateX(-50%) rotate(360deg);
  }
}

/* 控制栏 */
.control-bar {
  flex-shrink: 0;
  padding: 10px 16px;
  background: #2a2a2a;
  border-top: 1px solid #3a3a3a;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.control-buttons {
  display: flex;
  gap: 6px;
}

.control-btn {
  background: #3a3a3a;
  border: none;
  color: #e0e0e0;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.control-btn:hover {
  background: #4a4a4a;
  transform: scale(1.05);
}

.timeline-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 200px;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: #3a3a3a;
  border-radius: 2px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }

  100% {
    transform: translateX(100%);
  }
}

.progress {
  height: 100%;
  background: #5088bd;
  border-radius: 2px;
  position: relative;
}

.time-display {
  font-size: 12px;
  color: #888;
  white-space: nowrap;
}

.buffer-info {
  font-size: 11px;
  color: #666;
  white-space: nowrap;
}

.defect-timeline {
  height: 3px;
  background: #2a2a2a;
  position: relative;
  margin: 0 16px 6px 16px;
  border-radius: 1.5px;
}

.marker {
  position: absolute;
  top: -2px;
  width: 2px;
  height: 7px;
  background: #f44336;
  border-radius: 1px;
  transform: translateX(-50%);
  cursor: help;
  transition: height 0.2s;
}

.marker:hover {
  height: 10px;
  top: -4px;
  background: #ff5252;
}


/* 统计区域 */
.stats-section {
  flex-shrink: 0;
  background: #1e1e1e;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: height 0.05s ease;
}

.stats-header {
  padding: 10px 16px;
  background: #2a2a2a;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.stats-header h3 {
  font-size: 14px;
  color: #e0e0e0;
  margin: 0;
}

.stats-update {
  font-size: 11px;
  color: #888;
}

.stats-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* 统计区域内部的滚动条 */
.stats-scroll-area::-webkit-scrollbar {
  width: 6px;
}

.stats-scroll-area::-webkit-scrollbar-track {
  background: #2a2a2a;
  border-radius: 3px;
}

.stats-scroll-area::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 3px;
}

.stats-scroll-area::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.stat-card {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #3a3a3a;
  transition: all 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: #00bcd4;
  box-shadow: 0 4px 8px rgba(0, 188, 212, 0.1);
}

.stat-label {
  font-size: 11px;
  color: #888;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 6px;
  line-height: 1.2;
}

.stat-value small {
  font-size: 11px;
  color: #888;
  margin-left: 2px;
  font-weight: normal;
}

.stat-trend {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 3px;
  display: inline-block;
}

.stat-trend.up {
  background: #4caf50;
  color: #fff;
}

.stat-trend.down {
  background: #f44336;
  color: #fff;
}

/* 日志区域 */
.log-section {
  flex: 1;
  min-height: 200px;
  background: #1e1e1e;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 2px;
}

.log-header {
  padding: 10px 16px;
  background: #2a2a2a;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-header h3 {
  font-size: 14px;
  color: #e0e0e0;
  margin: 0;
}

.log-controls {
  display: flex;
  gap: 8px;
}

.log-btn {
  background: #3a3a3a;
  border: none;
  color: #b0b0b0;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
}

.log-btn:hover {
  background: #4a4a4a;
  color: #fff;
  transform: scale(1.02);
}

.log-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  font-family: monospace;
  font-size: 12px;
}

/* 日志区域内部的滚动条 */
.log-content::-webkit-scrollbar {
  width: 6px;
}

.log-content::-webkit-scrollbar-track {
  background: #2a2a2a;
  border-radius: 3px;
}

.log-content::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 3px;
}

.log-content::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

.log-item {
  padding: 6px 0;
  border-bottom: 1px solid #2a2a2a;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.log-item:hover {
  background: #2a2a2a;
}

.log-item.warning {
  background: rgba(255, 152, 0, 0.1);
}

.log-item.error {
  background: rgba(244, 67, 54, 0.1);
}

.log-time {
  color: #888;
  font-size: 11px;
  width: 70px;
  flex-shrink: 0;
}

.log-level {
  width: 45px;
  flex-shrink: 0;
  font-weight: 600;
}

.log-level.info {
  color: #2196f3;
}

.log-level.warn {
  color: #ff9800;
}

.log-level.error {
  color: #f44336;
}

.log-message {
  color: #b0b0b0;
  flex: 1;
}

/* 响应式调整 */
@media (max-width: 1600px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .video-section {
    min-height: 300px;
  }
}
</style>