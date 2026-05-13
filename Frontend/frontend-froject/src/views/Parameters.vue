<!-- src/views/Parameters.vue -->
<!-- 左侧导航栏处的参数调整页面 - 决定AI检测的灵敏度 -->
<template>
    <div class="parameters">
        <h2 class="page-title">参数调整</h2>
        <p class="page-desc">调整检测算法的灵敏度，平衡漏检和误报</p>

        <div class="params-grid">
            <!-- 第一行：核心参数卡片 -->
            <div class="param-card">
                <div class="param-header">
                    <h3>置信度阈值</h3>
                    <span class="param-value">{{ confidenceThreshold }}%</span>
                </div>
                <div class="param-slider">
                    <input type="range" v-model="confidenceThreshold" min="0" max="100" step="1" class="slider">
                    <div class="slider-labels">
                        <span>宽松</span>
                        <span>严格</span>
                    </div>
                </div>
                <p class="param-desc">只有AI打分超过此值才标记为缺陷。调低则更多检出（可能误报），调高则更严格（可能漏检）</p>
                <div class="param-example">
                    <span class="example-badge" :class="{ active: confidenceThreshold <= 50 }">50% 以下: 高检出</span>
                    <span class="example-badge" :class="{ active: confidenceThreshold >= 80 }">80% 以上: 高精度</span>
                </div>
            </div>

            <div class="param-card">
                <div class="param-header">
                    <h3>IOU 阈值</h3>
                    <span class="param-value">{{ iouThreshold }}</span>
                </div>
                <div class="param-slider">
                    <input type="range" v-model="iouThreshold" min="0.1" max="0.9" step="0.05" class="slider">
                    <div class="slider-labels">
                        <span>宽松合并</span>
                        <span>严格区分</span>
                    </div>
                </div>
                <p class="param-desc">多个检测框重叠时的合并规则。值越大，越容易区分相邻缺陷</p>
                <div class="param-example">
                    <span class="example-tag">当前值: {{ iouThreshold }}</span>
                </div>
            </div>

            <div class="param-card">
                <div class="param-header">
                    <h3>NG判定次数</h3>
                    <span class="param-value">{{ ngCount }} 次</span>
                </div>
                <div class="param-slider">
                    <input type="range" v-model="ngCount" min="1" max="10" step="1" class="slider">
                    <div class="slider-labels">
                        <span>敏感</span>
                        <span>稳定</span>
                    </div>
                </div>
                <p class="param-desc">连续N次检测到缺陷才算NG，避免偶尔的噪声干扰导致频繁停机</p>
            </div>
        </div>

        <!-- 第二行：高级参数 -->
        <div class="advanced-section">
            <h3>高级参数</h3>

            <div class="advanced-grid">
                <div class="advanced-item">
                    <label>最小缺陷面积</label>
                    <div class="number-input">
                        <input type="number" v-model="minArea" min="0" max="1000" step="10">
                        <span>px²</span>
                    </div>
                </div>

                <div class="advanced-item">
                    <label>最大缺陷面积</label>
                    <div class="number-input">
                        <input type="number" v-model="maxArea" min="0" max="10000" step="10">
                        <span>px²</span>
                    </div>
                </div>

                <div class="advanced-item">
                    <label>检测灵敏度</label>
                    <select v-model="sensitivity">
                        <option value="low">低 - 减少误报</option>
                        <option value="medium">中 - 平衡</option>
                        <option value="high">高 - 减少漏检</option>
                    </select>
                </div>

                <div class="advanced-item">
                    <label>缺陷合并策略</label>
                    <select v-model="mergeStrategy">
                        <option value="none">不合并</option>
                        <option value="nearby">邻近合并</option>
                        <option value="overlap">重叠合并</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- 第三行：检测区域设置 -->
        <div class="roi-section">
            <h3>检测区域 (ROI)</h3>

            <div class="roi-container">
                <div class="roi-preview">
                    <div class="roi-image" ref="roiImage">
                        <!-- 可拖拽的ROI框 -->
                        <div class="roi-box" :style="roiStyle" @mousedown="startRoiDrag" v-show="showRoi">
                            <div class="roi-handle tl" @mousedown.stop="startRoiResize('tl', $event)"></div>
                            <div class="roi-handle tr" @mousedown.stop="startRoiResize('tr', $event)"></div>
                            <div class="roi-handle bl" @mousedown.stop="startRoiResize('bl', $event)"></div>
                            <div class="roi-handle br" @mousedown.stop="startRoiResize('br', $event)"></div>
                            <div class="roi-label">检测区域</div>
                        </div>
                    </div>
                </div>

                <div class="roi-controls">
                    <div class="roi-coords">
                        <div><label>X:</label> {{ Math.round(roi.x * 100) }}%</div>
                        <div><label>Y:</label> {{ Math.round(roi.y * 100) }}%</div>
                        <div><label>宽度:</label> {{ Math.round(roi.width * 100) }}%</div>
                        <div><label>高度:</label> {{ Math.round(roi.height * 100) }}%</div>
                    </div>
                    <div class="roi-buttons">
                        <button class="btn secondary" @click="resetRoi">重置</button>
                        <button class="btn secondary" @click="setFullRoi">全画面</button>
                        <button class="btn primary" @click="applyRoi">应用</button>
                    </div>
                    <p class="roi-desc">只检测框内区域，减少边缘对于检测的干扰</p>
                </div>
            </div>
        </div>

        <!-- 底部操作栏 -->
        <div class="action-bar">
            <div class="preset-selector">
                <label>预设配置:</label>
                <select v-model="selectedPreset" @change="onPresetChange">
                    <option value="default">默认配置</option>
                    <option value="strict">严格模式 (低误报)</option>
                    <option value="sensitive">敏感模式 (低漏检)</option>
                    <option value="custom">自定义</option>
                </select>
            </div>

            <div class="action-buttons">
                <button class="btn secondary" @click="resetToDefault">恢复默认</button>
                <button class="btn primary" @click="saveParameters">保存参数</button>
                <button class="btn success" @click="applyParameters">立即应用</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useParameterStore } from '../stores/parameter'
import { storeToRefs } from 'pinia'

const paramStore = useParameterStore()
const { 
  confidenceThreshold, 
  iouThreshold, 
  ngCount, 
  minArea, 
  maxArea, 
  sensitivity, 
  mergeStrategy, 
  roi, 
  selectedPreset 
} = storeToRefs(paramStore)

// ========== ROI 相关 ==========
const showRoi = ref(true)
const roiImage = ref(null)

// ROI样式
const roiStyle = computed(() => {
  // 确保 roi.value 存在
  if (!roi.value) return {}
  return {
    left: `${roi.value.x * 100}%`,
    top: `${roi.value.y * 100}%`,
    width: `${roi.value.width * 100}%`,
    height: `${roi.value.height * 100}%`
  }
})

// ROI拖拽相关
const isDragging = ref(false)
const isResizing = ref(false)
const resizeDir = ref(null)
const dragStart = ref({ x: 0, y: 0 })
const roiStart = ref({ x: 0, y: 0, width: 0, height: 0 })

const startRoiDrag = (e) => {
  e.preventDefault()
  isDragging.value = true
  dragStart.value = { x: e.clientX, y: e.clientY }
  roiStart.value = { ...roi.value }

  document.addEventListener('mousemove', onRoiDrag)
  document.addEventListener('mouseup', stopRoiDrag)
}

const onRoiDrag = (e) => {
  if (!isDragging.value || !roi.value) return

  const deltaX = (e.clientX - dragStart.value.x) / 400
  const deltaY = (e.clientY - dragStart.value.y) / 300

  let newX = roiStart.value.x + deltaX
  let newY = roiStart.value.y + deltaY

  newX = Math.max(0, Math.min(1 - roi.value.width, newX))
  newY = Math.max(0, Math.min(1 - roi.value.height, newY))

  roi.value.x = newX
  roi.value.y = newY
}

const stopRoiDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', onRoiDrag)
  document.removeEventListener('mouseup', stopRoiDrag)
}

const startRoiResize = (dir, e) => {
  e.preventDefault()
  isResizing.value = true
  resizeDir.value = dir
  dragStart.value = { x: e.clientX, y: e.clientY }
  roiStart.value = { ...roi.value }

  document.addEventListener('mousemove', onRoiResize)
  document.addEventListener('mouseup', stopRoiResize)
}

const onRoiResize = (e) => {
  if (!isResizing.value || !resizeDir.value || !roi.value) return

  const deltaX = (e.clientX - dragStart.value.x) / 400
  const deltaY = (e.clientY - dragStart.value.y) / 300

  let newX = roiStart.value.x
  let newY = roiStart.value.y
  let newWidth = roiStart.value.width
  let newHeight = roiStart.value.height

  const minSize = 0.05

  switch (resizeDir.value) {
    case 'tl':
      newX = Math.max(0, Math.min(roiStart.value.x + roiStart.value.width - minSize, roiStart.value.x + deltaX))
      newY = Math.max(0, Math.min(roiStart.value.y + roiStart.value.height - minSize, roiStart.value.y + deltaY))
      newWidth = roiStart.value.width + (roiStart.value.x - newX)
      newHeight = roiStart.value.height + (roiStart.value.y - newY)
      break
    case 'tr':
      newY = Math.max(0, Math.min(roiStart.value.y + roiStart.value.height - minSize, roiStart.value.y + deltaY))
      newWidth = Math.max(minSize, Math.min(1 - newX, roiStart.value.width + deltaX))
      newHeight = roiStart.value.height + (roiStart.value.y - newY)
      break
    case 'bl':
      newX = Math.max(0, Math.min(roiStart.value.x + roiStart.value.width - minSize, roiStart.value.x + deltaX))
      newWidth = roiStart.value.width + (roiStart.value.x - newX)
      newHeight = Math.max(minSize, Math.min(1 - newY, roiStart.value.height + deltaY))
      break
    case 'br':
      newWidth = Math.max(minSize, Math.min(1 - newX, roiStart.value.width + deltaX))
      newHeight = Math.max(minSize, Math.min(1 - newY, roiStart.value.height + deltaY))
      break
  }

  roi.value = { x: newX, y: newY, width: newWidth, height: newHeight }
}

const stopRoiResize = () => {
  isResizing.value = false
  resizeDir.value = null
  document.removeEventListener('mousemove', onRoiResize)
  document.removeEventListener('mouseup', stopRoiResize)
}

// ========== 操作方法 ==========

// 预设切换
const onPresetChange = () => {
  paramStore.applyPreset(selectedPreset.value)
}

// 重置 ROI
const resetRoi = () => {
  paramStore.resetRoi()
}

// 全画面 ROI
const setFullRoi = () => {
  paramStore.setFullRoi()
}

// 应用 ROI
const applyRoi = () => {
  console.log('应用ROI:', roi.value)
  alert('ROI区域已应用')
}

// 恢复默认
const resetToDefault = () => {
  paramStore.applyPreset('default')
}

// 保存参数
const saveParameters = async () => {
  await paramStore.saveParameters()
  alert('参数已保存')
}

// 应用参数
const applyParameters = () => {
  console.log('应用参数')
  alert('参数已应用')
}

// 清理事件监听
onUnmounted(() => {
  document.removeEventListener('mousemove', onRoiDrag)
  document.removeEventListener('mouseup', stopRoiDrag)
  document.removeEventListener('mousemove', onRoiResize)
  document.removeEventListener('mouseup', stopRoiResize)
})
</script>

<style scoped>
/* 深色主题滚动条 */
.parameters::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

.parameters::-webkit-scrollbar-track {
    background: #1e1e1e;
    border-radius: 4px;
}

.parameters::-webkit-scrollbar-thumb {
    background: #555;
    border-radius: 4px;
    border: 2px solid #1e1e1e;
}

.parameters::-webkit-scrollbar-thumb:hover {
    background: #777;
}

.parameters::-webkit-scrollbar-corner {
    background: #1e1e1e;
}

.parameters {
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

.params-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.param-card {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #3a3a3a;
    transition: all 0.2s;
}

.param-card:hover {
    border-color: #00bcd4;
    box-shadow: 0 4px 12px rgba(0, 188, 212, 0.1);
}

.param-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
}

.param-icon {
    font-size: 24px;
}

.param-header h3 {
    flex: 1;
    font-size: 16px;
    color: #e0e0e0;
    margin: 0;
}

.param-value {
    font-size: 20px;
    font-weight: 600;
    color: #00bcd4;
}

.param-slider {
    margin-bottom: 12px;
}

.slider {
    width: 100%;
    height: 4px;
    background: #3a3a3a;
    border-radius: 2px;
    /* 不确定 */
    appearance: none;
    -webkit-appearance: none;
    margin-bottom: 4px;
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    background: #00bcd4;
    border-radius: 9px;
    cursor: pointer;
    border: 2px solid #fff;
}

.slider-labels {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #666;
}

.param-desc {
    font-size: 12px;
    color: #888;
    line-height: 1.5;
    margin-bottom: 12px;
}

.param-example {
    display: flex;
    gap: 8px;
}

.example-badge {
    font-size: 11px;
    padding: 2px 8px;
    background: #323232;
    border-radius: 12px;
    color: #888;
    border: 1px solid #3a3a3a;
}

.example-badge.active {
    background: #00bcd4;
    color: #fff;
    border-color: #00bcd4;
}

.example-tag {
    font-size: 11px;
    padding: 2px 8px;
    background: #00bcd4;
    color: #fff;
    border-radius: 12px;
}

.advanced-section {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #3a3a3a;
    margin-bottom: 24px;
}

.advanced-section h3 {
    font-size: 16px;
    color: #e0e0e0;
    margin: 0 0 16px 0;
}

.advanced-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.advanced-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.advanced-item label {
    font-size: 12px;
    color: #888;
}

.number-input {
    display: flex;
    align-items: center;
    gap: 4px;
}

.number-input input {
    flex: 1;
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
}

.number-input span {
    color: #888;
    font-size: 12px;
    min-width: 40px;
}

.advanced-item select {
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
}

.roi-section {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #3a3a3a;
    margin-bottom: 24px;
}

.roi-section h3 {
    font-size: 16px;
    color: #e0e0e0;
    margin: 0 0 16px 0;
}

.roi-container {
    display: flex;
    gap: 24px;
}

.roi-preview {
    flex: 1;
    aspect-ratio: 4/3;
    background: #1a1a1a;
    border-radius: 4px;
    overflow: hidden;
    border: 1px solid #3a3a3a;
}

.roi-image {
    width: 100%;
    height: 100%;
    position: relative;
    background: linear-gradient(45deg, #2a2a2a 25%, #1a1a1a 25%, #1a1a1a 50%, #2a2a2a 50%, #2a2a2a 75%, #1a1a1a 75%);
    background-size: 20px 20px;
}

.roi-box {
    position: absolute;
    border: 2px solid #00bcd4;
    background: rgba(0, 188, 212, 0.1);
    cursor: move;
}

.roi-handle {
    position: absolute;
    width: 12px;
    height: 12px;
    background: #00bcd4;
    border: 2px solid #fff;
    border-radius: 6px;
}

.roi-handle.tl {
    top: -6px;
    left: -6px;
    cursor: nw-resize;
}

.roi-handle.tr {
    top: -6px;
    right: -6px;
    cursor: ne-resize;
}

.roi-handle.bl {
    bottom: -6px;
    left: -6px;
    cursor: sw-resize;
}

.roi-handle.br {
    bottom: -6px;
    right: -6px;
    cursor: se-resize;
}

.roi-label {
    position: absolute;
    top: -24px;
    left: 0;
    background: #00bcd4;
    color: #fff;
    padding: 2px 8px;
    font-size: 11px;
    border-radius: 3px;
    white-space: nowrap;
}

.roi-controls {
    width: 280px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.roi-coords {
    background: #1e1e1e;
    padding: 16px;
    border-radius: 4px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.roi-coords div {
    display: flex;
    align-items: center;
    gap: 4px;
}

.roi-coords label {
    color: #888;
    font-size: 12px;
    min-width: 40px;
}

.roi-buttons {
    display: flex;
    gap: 8px;
}

.roi-desc {
    font-size: 12px;
    color: #888;
    margin: 0;
}

.action-bar {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 16px 20px;
    border: 1px solid #3a3a3a;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    bottom: 0;
    backdrop-filter: blur(8px);
    background: rgba(42, 42, 42, 0.95);
}

.preset-selector {
    display: flex;
    align-items: center;
    gap: 12px;
}

.preset-selector label {
    color: #888;
    font-size: 13px;
}

.preset-selector select {
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 13px;
    cursor: pointer;
    min-width: 150px;
}

.action-buttons {
    display: flex;
    gap: 12px;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn.primary {
    background: #00bcd4;
    color: #fff;
}

.btn.primary:hover {
    background: #00acc1;
    transform: translateY(-1px);
}

.btn.secondary {
    background: #3a3a3a;
    color: #e0e0e0;
}

.btn.secondary:hover {
    background: #4a4a4a;
}

.btn.success {
    background: #4caf50;
    color: #fff;
}

.btn.success:hover {
    background: #45a049;
    transform: translateY(-1px);
}

/* 响应式 */
@media (max-width: 1400px) {
    .params-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .advanced-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 1200px) {
    .roi-container {
        flex-direction: column;
    }

    .roi-controls {
        width: 100%;
    }
}

@media (max-width: 900px) {
    .params-grid {
        grid-template-columns: 1fr;
    }

    .action-bar {
        flex-direction: column;
        gap: 16px;
    }
}
</style>