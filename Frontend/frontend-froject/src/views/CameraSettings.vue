<!-- src/views/CameraSettings.vue -->
<!-- 摄像头设置页面 - 控制图像采集质量 -->
<template>
    <div class="camera-settings">
        <h2 class="page-title">摄像头设置</h2>
        <p class="page-desc">调整摄像头参数，确保AI能看清布匹细节</p>

        <!-- 摄像头列表和预览 -->
        <div class="camera-section">
            <div class="camera-list">
                <div class="section-header">
                    <h3>摄像头列表</h3>
                    <button class="btn secondary small" @click="refreshCameras">刷新</button>
                </div>
                <div class="camera-items">
                    <div v-for="cam in cameras" :key="cam.id" class="camera-item"
                        :class="{ active: selectedCamera === cam.id }" @click="selectCamera(cam.id)">
                        <div class="camera-info">
                            <div class="camera-name">{{ cam.name }}</div>
                            <div class="camera-status" :class="cam.status">{{ cam.status === 'online' ? '在线' : '离线' }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="camera-preview">
                <div class="preview-header">
                    <h3>实时预览</h3>
                    <div class="preview-controls">
                        <button class="btn secondary small" @click="startPreview"
                            :disabled="!selectedCamera">开始预览</button>
                        <button class="btn secondary small" @click="stopPreview" :disabled="!isPreviewing">停止</button>
                    </div>
                </div>
                <div class="preview-container">
                    <div v-if="!isPreviewing" class="preview-placeholder">
                        <span>选择摄像头开始预览</span>
                    </div>
                    <div v-else class="preview-active">
                        <!-- 这里放实际视频流 -->
                        <div class="preview-image">
                            <div class="preview-grid"></div>
                            <div class="preview-fps">FPS: 30</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 摄像头参数调整 -->
        <div class="params-section" v-if="selectedCamera">
            <h3>图像参数</h3>

            <div class="params-grid">
                <!-- 曝光 -->
                <div class="param-card">
                    <div class="param-header">
                        <h4>曝光时间</h4>
                        <span class="param-value">{{ exposure }} μs</span>
                    </div>
                    <div class="param-slider">
                        <input type="range" v-model="exposure" min="10" max="10000" step="10" class="slider">
                        <div class="slider-labels">
                            <span>暗</span>
                            <span>亮</span>
                        </div>
                    </div>
                    <p class="param-desc">控制进光量，曝光不足图像太暗，过度则发白</p>
                </div>

                <!-- 增益 -->
                <div class="param-card">
                    <div class="param-header">
                        <h4>增益</h4>
                        <span class="param-value">{{ gain }} dB</span>
                    </div>
                    <div class="param-slider">
                        <input type="range" v-model="gain" min="0" max="48" step="1" class="slider">
                        <div class="slider-labels">
                            <span>低噪点</span>
                            <span>高亮度</span>
                        </div>
                    </div>
                    <p class="param-desc">放大图像信号，增益越高噪点越多</p>
                </div>

                <!-- 对比度 -->
                <div class="param-card">
                    <div class="param-header">
                        <h4>对比度</h4>
                        <span class="param-value">{{ contrast }}%</span>
                    </div>
                    <div class="param-slider">
                        <input type="range" v-model="contrast" min="0" max="200" step="1" class="slider">
                        <div class="slider-labels">
                            <span>柔和</span>
                            <span>锐利</span>
                        </div>
                    </div>
                </div>

                <!-- 饱和度 -->
                <div class="param-card">
                    <div class="param-header">
                        <h4>饱和度</h4>
                        <span class="param-value">{{ saturation }}%</span>
                    </div>
                    <div class="param-slider">
                        <input type="range" v-model="saturation" min="0" max="200" step="1" class="slider">
                        <div class="slider-labels">
                            <span>黑白</span>
                            <span>鲜艳</span>
                        </div>
                    </div>
                </div>
            </div>

            <h3 class="mt-4">高级设置</h3>

            <div class="advanced-grid">
                <!-- 触发模式 -->
                <div class="advanced-item">
                    <label>触发模式</label>
                    <select v-model="triggerMode">
                        <option value="continuous">连续采集</option>
                        <option value="soft">软触发</option>
                        <option value="hard">硬触发</option>
                    </select>
                </div>

                <!-- 帧率 -->
                <div class="advanced-item">
                    <label>帧率 (FPS)</label>
                    <div class="number-input">
                        <input type="number" v-model="fps" min="1" max="120" step="1">
                        <span>帧/秒</span>
                    </div>
                </div>

                <!-- 分辨率 -->
                <div class="advanced-item">
                    <label>分辨率</label>
                    <select v-model="resolution">
                        <option value="640x480">640x480 (VGA)</option>
                        <option value="1280x720">1280x720 (HD)</option>
                        <option value="1920x1080">1920x1080 (Full HD)</option>
                        <option value="2592x1944">2592x1944 (5MP)</option>
                    </select>
                </div>

                <!-- 像素格式 -->
                <div class="advanced-item">
                    <label>像素格式</label>
                    <select v-model="pixelFormat">
                        <option value="mono8">Mono8 (黑白)</option>
                        <option value="mono12">Mono12 (12位黑白)</option>
                        <option value="bayer8">Bayer8 (彩色)</option>
                        <option value="yuv422">YUV422 (彩色)</option>
                    </select>
                </div>

                <!-- 白平衡 -->
                <div class="advanced-item">
                    <label>白平衡模式</label>
                    <select v-model="whiteBalance">
                        <option value="auto">自动</option>
                        <option value="manual">手动</option>
                        <option value="daylight">日光</option>
                        <option value="fluorescent">荧光灯</option>
                    </select>
                </div>

                <!-- 自动曝光 -->
                <div class="advanced-item">
                    <label>自动曝光</label>
                    <select v-model="autoExposure">
                        <option value="off">关闭</option>
                        <option value="once">单次</option>
                        <option value="continuous">连续</option>
                    </select>
                </div>
            </div>

            <!-- 图像调节曲线 (简化版) -->
            <div class="curve-section">
                <h4>伽马曲线</h4>
                <div class="curve-container">
                    <canvas ref="gammaCanvas" width="200" height="150" class="gamma-canvas"></canvas>
                    <div class="curve-slider">
                        <span class="slider-label">伽马值</span>
                        <input type="range" v-model="gamma" min="0.1" max="3.0" step="0.1" class="slider"
                            @input="drawGammaCurve">
                        <span class="slider-value">{{ gamma.toFixed(1) }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 底部操作栏 -->
        <div class="action-bar" v-if="selectedCamera">
            <div class="preset-selector">
                <label>预设:</label>
                <select v-model="selectedPreset">
                    <option value="default">默认</option>
                    <option value="bright">明亮场景</option>
                    <option value="dark">暗场</option>
                    <option value="fast">高速采集</option>
                </select>
            </div>

            <div class="action-buttons">
                <button class="btn secondary" @click="resetToDefault">恢复默认</button>
                <button class="btn primary" @click="saveSettings">保存设置</button>
                <button class="btn success" @click="applySettings" :disabled="!isPreviewing">应用</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

// 摄像头列表
const cameras = ref([
    { id: 1, name: '主摄像头 (正面)', status: 'online' },
    { id: 2, name: '副摄像头 (背面)', status: 'online' },
    { id: 3, name: '备用摄像头', status: 'offline' }
])

const selectedCamera = ref(null)
const isPreviewing = ref(false)

// 图像参数
const exposure = ref(500)
const gain = ref(12)
const contrast = ref(100)
const saturation = ref(100)
const gamma = ref(1.0)

// 高级设置
const triggerMode = ref('continuous')
const fps = ref(30)
const resolution = ref('1920x1080')
const pixelFormat = ref('mono8')
const whiteBalance = ref('auto')
const autoExposure = ref('continuous')

// 预设
const selectedPreset = ref('default')

// 伽马曲线画布
const gammaCanvas = ref(null)

// 选择摄像头
const selectCamera = (id) => {
    selectedCamera.value = id
    stopPreview()
}

// 刷新摄像头列表
const refreshCameras = () => {
    // 模拟刷新
    console.log('刷新摄像头列表')
}

// 预览控制
const startPreview = () => {
    if (!selectedCamera.value) return
    isPreviewing.value = true
    console.log('开始预览摄像头', selectedCamera.value)
}

const stopPreview = () => {
    isPreviewing.value = false
    console.log('停止预览')
}

// 绘制伽马曲线
const drawGammaCurve = () => {
    const canvas = gammaCanvas.value
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height

    // 清空
    ctx.clearRect(0, 0, width, height)

    // 绘制网格
    ctx.strokeStyle = '#3a3a3a'
    ctx.lineWidth = 0.5

    for (let i = 0; i <= 4; i++) {
        const x = (i / 4) * width
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, height)
        ctx.stroke()
    }

    for (let i = 0; i <= 4; i++) {
        const y = height - (i / 4) * height
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(width, y)
        ctx.stroke()
    }

    // 绘制对角线
    ctx.strokeStyle = '#666'
    ctx.beginPath()
    ctx.moveTo(0, height)
    ctx.lineTo(width, 0)
    ctx.stroke()

    // 绘制伽马曲线
    ctx.strokeStyle = '#00bcd4'
    ctx.lineWidth = 2
    ctx.beginPath()

    for (let x = 0; x < width; x++) {
        const input = x / width
        const output = Math.pow(input, gamma.value)
        const y = height - output * height

        if (x === 0) {
            ctx.moveTo(x, y)
        } else {
            ctx.lineTo(x, y)
        }
    }

    ctx.stroke()
}

// 预设切换
watch(selectedPreset, (newPreset) => {
    switch (newPreset) {
        case 'default':
            exposure.value = 500
            gain.value = 12
            contrast.value = 100
            saturation.value = 100
            gamma.value = 1.0
            fps.value = 30
            break
        case 'bright':
            exposure.value = 200
            gain.value = 6
            contrast.value = 110
            saturation.value = 110
            gamma.value = 0.8
            break
        case 'dark':
            exposure.value = 2000
            gain.value = 24
            contrast.value = 120
            saturation.value = 100
            gamma.value = 1.2
            break
        case 'fast':
            fps.value = 60
            resolution.value = '1280x720'
            exposure.value = 300
            break
    }
    drawGammaCurve()
})

// 重置为默认
const resetToDefault = () => {
    selectedPreset.value = 'default'
}

// 保存设置
const saveSettings = () => {
    console.log('保存摄像头设置', {
        cameraId: selectedCamera.value,
        exposure: exposure.value,
        gain: gain.value,
        contrast: contrast.value,
        saturation: saturation.value,
        gamma: gamma.value,
        triggerMode: triggerMode.value,
        fps: fps.value,
        resolution: resolution.value,
        pixelFormat: pixelFormat.value,
        whiteBalance: whiteBalance.value,
        autoExposure: autoExposure.value
    })
    alert('摄像头设置已保存')
}

// 应用设置
const applySettings = () => {
    if (!isPreviewing.value) {
        alert('请先开始预览')
        return
    }
    console.log('应用摄像头设置')
    alert('设置已应用到当前预览')
}

// 初始化
onMounted(() => {
    drawGammaCurve()
})

// 监听伽马值变化
watch(gamma, () => {
    drawGammaCurve()
})

// 清理
onUnmounted(() => {
    stopPreview()
})
</script>

<style scoped>
.camera-settings {
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

/* 摄像头列表和预览区 */
.camera-section {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

.camera-list {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #3a3a3a;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.section-header h3 {
    font-size: 16px;
    color: #e0e0e0;
    margin: 0;
}

.btn.small {
    padding: 4px 8px;
    font-size: 11px;
}

.camera-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.camera-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
}

.camera-item:hover {
    border-color: #666;
}

.camera-item.active {
    border-color: #00bcd4;
    background: #232323;
}

.camera-icon {
    font-size: 20px;
}

.camera-info {
    flex: 1;
    min-width: 0;
}

.camera-name {
    font-size: 13px;
    color: #e0e0e0;
    margin-bottom: 2px;
}

.camera-status {
    font-size: 11px;
}

.camera-status.online {
    color: #4caf50;
}

.camera-status.offline {
    color: #f44336;
}

.camera-preview {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #3a3a3a;
}

.preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.preview-header h3 {
    font-size: 16px;
    color: #e0e0e0;
    margin: 0;
}

.preview-controls {
    display: flex;
    gap: 8px;
}

.preview-container {
    aspect-ratio: 16/9;
    background: #1a1a1a;
    border-radius: 4px;
    overflow: hidden;
    border: 1px solid #3a3a3a;
}

.preview-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    font-size: 14px;
}

.preview-active {
    width: 100%;
    height: 100%;
    position: relative;
}

.preview-image {
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #2a2a2a 25%, #1a1a1a 25%, #1a1a1a 50%, #2a2a2a 50%, #2a2a2a 75%, #1a1a1a 75%);
    background-size: 20px 20px;
    position: relative;
}

.preview-grid {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
    background-size: 40px 40px;
}

.preview-fps {
    position: absolute;
    bottom: 8px;
    right: 8px;
    background: rgba(0, 0, 0, 0.7);
    color: #00bcd4;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 11px;
}

/* 参数区域 */
.params-section {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 20px;
    border: 1px solid #3a3a3a;
    margin-bottom: 24px;
}

.params-section h3 {
    font-size: 18px;
    color: #e0e0e0;
    margin: 0 0 16px 0;
}

.params-section h4 {
    font-size: 14px;
    color: #e0e0e0;
    margin: 0 0 12px 0;
}

.mt-4 {
    margin-top: 24px;
}

.params-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.param-card {
    background: #1e1e1e;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #3a3a3a;
}

.param-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.param-icon {
    font-size: 20px;
}

.param-header h4 {
    flex: 1;
    font-size: 14px;
    margin: 0;
}

.param-value {
    font-size: 16px;
    font-weight: 600;
    color: #00bcd4;
}

.param-slider {
    margin-bottom: 8px;
}

.slider {
    width: 100%;
    height: 4px;
    background: #3a3a3a;
    border-radius: 2px;
    appearance: none;
    -webkit-appearance: none;
    margin-bottom: 4px;
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    background: #00bcd4;
    border-radius: 8px;
    cursor: pointer;
    border: 2px solid #fff;
}

.slider-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #666;
}

.param-desc {
    font-size: 11px;
    color: #888;
    margin: 8px 0 0 0;
}

/* 高级设置网格 */
.advanced-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.advanced-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.advanced-item label {
    font-size: 12px;
    color: #888;
}

.advanced-item select,
.advanced-item input {
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 13px;
    width: 100%;
}

.number-input {
    display: flex;
    align-items: center;
    gap: 4px;
}

.number-input input {
    flex: 1;
}

.number-input span {
    color: #888;
    font-size: 11px;
    min-width: 40px;
}

/* 伽马曲线 */
.curve-section {
    background: #1e1e1e;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #3a3a3a;
}

.curve-container {
    display: flex;
    gap: 20px;
    align-items: center;
}

.gamma-canvas {
    width: 200px;
    height: 150px;
    background: #1a1a1a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
}

.curve-slider {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 12px;
}

.slider-label {
    font-size: 12px;
    color: #888;
    min-width: 50px;
}

.slider-value {
    font-size: 14px;
    color: #00bcd4;
    font-weight: 600;
    min-width: 40px;
}

/* 底部操作栏 */
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
    min-width: 130px;
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

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn.primary {
    background: #00bcd4;
    color: #fff;
}

.btn.primary:hover:not(:disabled) {
    background: #00acc1;
    transform: translateY(-1px);
}

.btn.secondary {
    background: #3a3a3a;
    color: #e0e0e0;
}

.btn.secondary:hover:not(:disabled) {
    background: #4a4a4a;
}

.btn.success {
    background: #4caf50;
    color: #fff;
}

.btn.success:hover:not(:disabled) {
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
    .camera-section {
        grid-template-columns: 1fr;
    }

    .camera-list {
        max-height: 200px;
    }

    .camera-items {
        flex-direction: row;
        overflow-x: auto;
        padding-bottom: 4px;
    }

    .camera-item {
        min-width: 180px;
    }
}

@media (max-width: 900px) {
    .params-grid {
        grid-template-columns: 1fr;
    }

    .advanced-grid {
        grid-template-columns: 1fr;
    }

    .action-bar {
        flex-direction: column;
        gap: 16px;
    }

    .curve-container {
        flex-direction: column;
    }
}
</style>