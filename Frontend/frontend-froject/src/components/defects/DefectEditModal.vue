<!-- src/components/defects/DefectEditModal.vue -->
<!-- 右侧栏编辑缺陷检测结果的模态框组件 -->
<template>
    <Teleport to="body">
        <div v-if="visible" class="modal-overlay" @click.self="closeModal">
            <div class="modal-container" :style="modalStyle">
                <div class="modal-header">
                    <h2>编辑缺陷 #{{ defect?.id }}</h2>
                    <button class="close-btn" @click="closeModal">×</button>
                </div>

                <div class="modal-body">
                    <!-- 左右分栏布局 -->
                    <div class="edit-layout">
                        <!-- 左侧：图像预览区域 -->
                        <div class="preview-area">
                            <div class="image-container" ref="imageContainer">
                                <!-- 模拟缺陷图像 -->
                                <div class="defect-image" :style="{ background: getDefectColor(defect?.type) }">
                                    <div class="image-grid"></div>
                                    <!-- 可调节的检测框 -->
                                    <div class="bbox" :style="bboxStyle" @mousedown="startDrag" @touchstart="startDrag">
                                        <!-- 四个角的手柄 -->
                                        <div class="handle tl" @mousedown.stop="startResize('tl', $event)"></div>
                                        <div class="handle tr" @mousedown.stop="startResize('tr', $event)"></div>
                                        <div class="handle bl" @mousedown.stop="startResize('bl', $event)"></div>
                                        <div class="handle br" @mousedown.stop="startResize('br', $event)"></div>

                                        <!-- 边框上的调节点 -->
                                        <div class="handle top" @mousedown.stop="startResize('top', $event)"></div>
                                        <div class="handle bottom" @mousedown.stop="startResize('bottom', $event)">
                                        </div>
                                        <div class="handle left" @mousedown.stop="startResize('left', $event)"></div>
                                        <div class="handle right" @mousedown.stop="startResize('right', $event)"></div>
                                    </div>
                                </div>

                                <!-- 缩放控制 -->
                                <div class="image-controls">
                                    <button class="zoom-btn" @click="zoomOut">−</button>
                                    <span class="zoom-level">{{ Math.round(zoom * 100) }}%</span>
                                    <button class="zoom-btn" @click="zoomIn">+</button>
                                    <button class="fit-btn" @click="fitImage">适合</button>
                                </div>
                            </div>

                            <!-- 缺陷信息标签 -->
                            <div class="image-info">
                                <div class="info-tag" :style="{ background: getDefectColor(defect?.type) }">
                                    {{ defect?.type }} {{ defect?.confidence }}%
                                </div>
                            </div>
                        </div>

                        <!-- 右侧：编辑表单 -->
                        <div class="edit-area">
                            <div class="form-section">
                                <h3>缺陷信息</h3>

                                <div class="form-group">
                                    <label>缺陷类型</label>
                                    <select v-model="editedDefect.type" class="form-control">
                                        <option v-for="type in defectTypes" :key="type" :value="type">
                                            {{ type }}
                                        </option>
                                    </select>
                                </div>

                                <div class="form-group">
                                    <label>置信度 <span class="value">{{ editedDefect.confidence }}%</span></label>
                                    <input type="range" v-model="editedDefect.confidence" min="0" max="100"
                                        class="slider">
                                </div>

                                <div class="form-group">
                                    <label>状态</label>
                                    <div class="status-options">
                                        <label class="radio-label">
                                            <input type="radio" v-model="editedDefect.status" value="pending">
                                            <span class="radio-custom pending"></span>
                                            待处理
                                        </label>
                                        <label class="radio-label">
                                            <input type="radio" v-model="editedDefect.status" value="confirmed">
                                            <span class="radio-custom confirmed"></span>
                                            已确认
                                        </label>
                                        <label class="radio-label">
                                            <input type="radio" v-model="editedDefect.status" value="false-positive">
                                            <span class="radio-custom false-positive"></span>
                                            误判
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div class="form-section">
                                <h3>检测框调整</h3>

                                <div class="coord-grid">
                                    <div class="coord-item">
                                        <label>X</label>
                                        <input type="number" v-model.number="editedDefect.x" step="0.01" min="0" max="1"
                                            class="coord-input">
                                    </div>
                                    <div class="coord-item">
                                        <label>Y</label>
                                        <input type="number" v-model.number="editedDefect.y" step="0.01" min="0" max="1"
                                            class="coord-input">
                                    </div>
                                    <div class="coord-item">
                                        <label>宽度</label>
                                        <input type="number" v-model.number="editedDefect.width" step="0.01" min="0"
                                            max="1" class="coord-input">
                                    </div>
                                    <div class="coord-item">
                                        <label>高度</label>
                                        <input type="number" v-model.number="editedDefect.height" step="0.01" min="0"
                                            max="1" class="coord-input">
                                    </div>
                                </div>

                                <div class="button-group">
                                    <button class="btn secondary" @click="resetBBox">重置</button>
                                    <button class="btn secondary" @click="fitToDefect">贴合缺陷</button>
                                </div>
                            </div>

                            <div class="form-section">
                                <h3>备注</h3>
                                <textarea v-model="editedDefect.remarks" class="remarks-input" rows="4"
                                    placeholder="添加备注信息..."></textarea>
                            </div>

                            <div class="form-section">
                                <h3>操作历史</h3>
                                <div class="history-list">
                                    <div class="history-item">
                                        <span class="history-time">14:23:05</span>
                                        <span class="history-action">AI 初次检测</span>
                                        <span class="history-value">破洞 96%</span>
                                    </div>
                                    <div class="history-item" v-if="editedDefect.status !== originalDefect?.status">
                                        <span class="history-time">现在</span>
                                        <span class="history-action">状态修改</span>
                                        <span class="history-value">{{ originalDefect?.status }} → {{
                                            editedDefect.status }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modal-footer">
                    <div class="footer-left">
                        <button class="btn danger" @click="deleteDefect">删除缺陷</button>
                    </div>
                    <div class="footer-right">
                        <button class="btn secondary" @click="closeModal">取消</button>
                        <button class="btn primary" @click="saveDefect">保存修改</button>
                        <button class="btn success" @click="saveAndNext">保存并下一个</button>
                    </div>
                </div>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
    visible: Boolean,
    defect: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['update:visible', 'save', 'delete', 'next'])

const defectTypes = ['破洞', '脏污', '划痕', '色差', '毛丝']

// 编辑中的数据
const editedDefect = ref({})
const originalDefect = ref(null)

// 缩放和拖拽相关
const zoom = ref(1)
const imageContainer = ref(null)
const isDragging = ref(false)
const isResizing = ref(false)
const resizeDirection = ref(null)
const dragStart = ref({ x: 0, y: 0 })
const bboxStart = ref({ x: 0, y: 0, width: 0, height: 0 })

// 模态框样式
const modalStyle = computed(() => ({
    width: '90%',
    maxWidth: '1400px',
    height: '90%',
    maxHeight: '900px'
}))

// 计算检测框样式
const bboxStyle = computed(() => {
    if (!editedDefect.value) return {}

    return {
        left: `${editedDefect.value.x * 100}%`,
        top: `${editedDefect.value.y * 100}%`,
        width: `${editedDefect.value.width * 100}%`,
        height: `${editedDefect.value.height * 100}%`,
        position: 'absolute',
        border: '2px solid #00bcd4',
        cursor: 'move',
        transform: `scale(${1 / zoom.value})`, // 抵消父容器的缩放
        transformOrigin: 'top left'
    }
})

// 获取缺陷颜色
const getDefectColor = (type) => {
    const colors = {
        '破洞': '#f44336',
        '脏污': '#ff9800',
        '划痕': '#2196f3',
        '色差': '#9c27b0',
        '毛丝': '#4caf50'
    }
    return colors[type] || '#9e9e9e'
}

// 监听缺陷变化
watch(() => props.defect, (newVal) => {
    if (newVal) {
        editedDefect.value = JSON.parse(JSON.stringify(newVal))
        originalDefect.value = JSON.parse(JSON.stringify(newVal))
    }
}, { immediate: true, deep: true })

// 关闭模态框
const closeModal = () => {
    emit('update:visible', false)
}

// 保存缺陷
const saveDefect = () => {
    emit('save', editedDefect.value)
    closeModal()
}

// 保存并下一个
const saveAndNext = () => {
    emit('save', editedDefect.value)
    emit('next')
}

// 删除缺陷
const deleteDefect = () => {
    if (confirm('确定要删除这个缺陷吗？')) {
        emit('delete', editedDefect.value.id)
        closeModal()
    }
}

// 重置检测框
const resetBBox = () => {
    if (originalDefect.value) {
        editedDefect.value.x = originalDefect.value.x
        editedDefect.value.y = originalDefect.value.y
        editedDefect.value.width = originalDefect.value.width
        editedDefect.value.height = originalDefect.value.height
    }
}

// 贴合缺陷（模拟）
const fitToDefect = () => {
    // 这里后面可以调用AI算法重新贴合
    alert('AI正在重新计算检测框...')
}

// 缩放控制
const zoomIn = () => {
    zoom.value = Math.min(3, zoom.value + 0.25)
}

const zoomOut = () => {
    zoom.value = Math.max(0.5, zoom.value - 0.25)
}

const fitImage = () => {
    zoom.value = 1
}

// 拖拽检测框
const startDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()

    isDragging.value = true
    dragStart.value = {
        x: e.clientX,
        y: e.clientY
    }
    bboxStart.value = {
        x: editedDefect.value.x,
        y: editedDefect.value.y,
        width: editedDefect.value.width,
        height: editedDefect.value.height
    }

    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e) => {
    if (!isDragging.value) return

    const container = imageContainer.value
    if (!container) return

    const rect = container.getBoundingClientRect()
    const deltaX = (e.clientX - dragStart.value.x) / rect.width / zoom.value
    const deltaY = (e.clientY - dragStart.value.y) / rect.height / zoom.value

    let newX = bboxStart.value.x + deltaX
    let newY = bboxStart.value.y + deltaY

    // 限制边界
    newX = Math.max(0, Math.min(1 - editedDefect.value.width, newX))
    newY = Math.max(0, Math.min(1 - editedDefect.value.height, newY))

    editedDefect.value.x = newX
    editedDefect.value.y = newY
}

const stopDrag = () => {
    isDragging.value = false
    document.removeEventListener('mousemove', onDrag)
    document.removeEventListener('mouseup', stopDrag)
}

// 调整检测框大小
const startResize = (direction, e) => {
    e.preventDefault()
    e.stopPropagation()

    isResizing.value = true
    resizeDirection.value = direction
    dragStart.value = {
        x: e.clientX,
        y: e.clientY
    }
    bboxStart.value = {
        x: editedDefect.value.x,
        y: editedDefect.value.y,
        width: editedDefect.value.width,
        height: editedDefect.value.height
    }

    document.addEventListener('mousemove', onResize)
    document.addEventListener('mouseup', stopResize)
}

// 缩放时触发的事件
const onResize = (e) => {
    if (!isResizing.value || !resizeDirection.value) return

    const container = imageContainer.value
    if (!container) return

    const rect = container.getBoundingClientRect()
    const deltaX = (e.clientX - dragStart.value.x) / rect.width / zoom.value
    const deltaY = (e.clientY - dragStart.value.y) / rect.height / zoom.value

    let newX = bboxStart.value.x
    let newY = bboxStart.value.y
    let newWidth = bboxStart.value.width
    let newHeight = bboxStart.value.height

    switch (resizeDirection.value) {
        case 'tl':
            newX = Math.max(0, Math.min(bboxStart.value.x + bboxStart.value.width - 0.05, bboxStart.value.x + deltaX))
            newY = Math.max(0, Math.min(bboxStart.value.y + bboxStart.value.height - 0.05, bboxStart.value.y + deltaY))
            newWidth = bboxStart.value.width + (bboxStart.value.x - newX)
            newHeight = bboxStart.value.height + (bboxStart.value.y - newY)
            break
        case 'tr':
            newY = Math.max(0, Math.min(bboxStart.value.y + bboxStart.value.height - 0.05, bboxStart.value.y + deltaY))
            newWidth = Math.max(0.05, Math.min(1 - newX, bboxStart.value.width + deltaX))
            newHeight = bboxStart.value.height + (bboxStart.value.y - newY)
            break
        case 'bl':
            newX = Math.max(0, Math.min(bboxStart.value.x + bboxStart.value.width - 0.05, bboxStart.value.x + deltaX))
            newWidth = bboxStart.value.width + (bboxStart.value.x - newX)
            newHeight = Math.max(0.05, Math.min(1 - newY, bboxStart.value.height + deltaY))
            break
        case 'br':
            newWidth = Math.max(0.05, Math.min(1 - newX, bboxStart.value.width + deltaX))
            newHeight = Math.max(0.05, Math.min(1 - newY, bboxStart.value.height + deltaY))
            break
        case 'top':
            newY = Math.max(0, Math.min(bboxStart.value.y + bboxStart.value.height - 0.05, bboxStart.value.y + deltaY))
            newHeight = bboxStart.value.height + (bboxStart.value.y - newY)
            break
        case 'bottom':
            newHeight = Math.max(0.05, Math.min(1 - newY, bboxStart.value.height + deltaY))
            break
        case 'left':
            newX = Math.max(0, Math.min(bboxStart.value.x + bboxStart.value.width - 0.05, bboxStart.value.x + deltaX))
            newWidth = bboxStart.value.width + (bboxStart.value.x - newX)
            break
        case 'right':
            newWidth = Math.max(0.05, Math.min(1 - newX, bboxStart.value.width + deltaX))
            break
    }

    editedDefect.value.x = newX
    editedDefect.value.y = newY
    editedDefect.value.width = newWidth
    editedDefect.value.height = newHeight
}

const stopResize = () => {
    isResizing.value = false
    resizeDirection.value = null
    document.removeEventListener('mousemove', onResize)
    document.removeEventListener('mouseup', stopResize)
}

// 清理事件监听
onUnmounted(() => {
    document.removeEventListener('mousemove', onDrag)
    document.removeEventListener('mouseup', stopDrag)
    document.removeEventListener('mousemove', onResize)
    document.removeEventListener('mouseup', stopResize)
})
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.85);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
}

.modal-container {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #3a3a3a;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.modal-header {
    padding: 16px 24px;
    background: #2a2a2a;
    border-bottom: 1px solid #3a3a3a;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h2 {
    font-size: 18px;
    color: #e0e0e0;
    margin: 0;
}

.close-btn {
    background: none;
    border: none;
    color: #888;
    font-size: 24px;
    cursor: pointer;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
}

.close-btn:hover {
    background: #3a3a3a;
    color: #fff;
}

.modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
}

.edit-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    height: 100%;
}

/* 左侧预览区域 */
.preview-area {
    display: flex;
    flex-direction: column;
    gap: 16px;
    background: #2a2a2a;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #3a3a3a;
}

.image-container {
    position: relative;
    aspect-ratio: 1;
    background: #1a1a1a;
    border-radius: 4px;
    overflow: hidden;
    cursor: crosshair;
}

.defect-image {
    width: 100%;
    height: 100%;
    position: relative;
    transform: scale(v-bind('zoom'));
    transform-origin: top left;
    transition: transform 0.2s;
}

.image-grid {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
    background-size: 20px 20px;
}

.bbox {
    position: absolute;
    border: 2px solid #00bcd4;
    cursor: move;
    z-index: 10;
}

.bbox::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 188, 212, 0.1);
    pointer-events: none;
}

.handle {
    position: absolute;
    width: 12px;
    height: 12px;
    background: #00bcd4;
    border: 2px solid #fff;
    border-radius: 6px;
    z-index: 20;
}

.handle.tl {
    top: -6px;
    left: -6px;
    cursor: nw-resize;
}

.handle.tr {
    top: -6px;
    right: -6px;
    cursor: ne-resize;
}

.handle.bl {
    bottom: -6px;
    left: -6px;
    cursor: sw-resize;
}

.handle.br {
    bottom: -6px;
    right: -6px;
    cursor: se-resize;
}

.handle.top {
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    cursor: n-resize;
}

.handle.bottom {
    bottom: -6px;
    left: 50%;
    transform: translateX(-50%);
    cursor: s-resize;
}

.handle.left {
    left: -6px;
    top: 50%;
    transform: translateY(-50%);
    cursor: w-resize;
}

.handle.right {
    right: -6px;
    top: 50%;
    transform: translateY(-50%);
    cursor: e-resize;
}

.image-controls {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    background: #1a1a1a;
    border-radius: 4px;
}

.zoom-btn,
.fit-btn {
    background: #3a3a3a;
    border: none;
    color: #e0e0e0;
    width: 32px;
    height: 32px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.zoom-btn:hover,
.fit-btn:hover {
    background: #4a4a4a;
}

.zoom-level {
    flex: 1;
    text-align: center;
    font-size: 12px;
    color: #888;
}

.fit-btn {
    width: auto;
    padding: 0 12px;
    font-size: 12px;
}

.image-info {
    display: flex;
    justify-content: center;
}

.info-tag {
    padding: 6px 16px;
    border-radius: 20px;
    color: #fff;
    font-size: 14px;
    font-weight: 600;
}

/* 右侧编辑区域 */
.edit-area {
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: auto;
    padding-right: 8px;
}

.form-section {
    background: #2a2a2a;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #3a3a3a;
}

.form-section h3 {
    font-size: 14px;
    color: #e0e0e0;
    margin: 0 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #3a3a3a;
}

.form-group {
    margin-bottom: 16px;
}

.form-group label {
    display: block;
    font-size: 12px;
    color: #888;
    margin-bottom: 6px;
}

.form-control {
    width: 100%;
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 14px;
}

.form-control:focus {
    outline: none;
    border-color: #00bcd4;
}

.value {
    float: right;
    color: #00bcd4;
}

.slider {
    width: 100%;
    height: 4px;
    background: #3a3a3a;
    border-radius: 2px;
    appearance: none;
    -webkit-appearance: none;
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

.status-options {
    display: flex;
    gap: 20px;
}

.radio-label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 13px;
    color: #e0e0e0;
}

.radio-label input {
    display: none;
}

.radio-custom {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #3a3a3a;
    position: relative;
}

.radio-custom.pending {
    background: #ff9800;
}

.radio-custom.confirmed {
    background: #4caf50;
}

.radio-custom.false-positive {
    background: #f44336;
}

.radio-label input:checked+.radio-custom::after {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 8px;
    height: 8px;
    background: #fff;
    border-radius: 4px;
}

.coord-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 12px;
}

.coord-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.coord-item label {
    font-size: 11px;
    color: #888;
}

.coord-input {
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 12px;
}

.button-group {
    display: flex;
    gap: 8px;
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

.btn.danger {
    background: #f44336;
    color: #fff;
}

.btn.danger:hover {
    background: #d32f2f;
}

.remarks-input {
    width: 100%;
    background: #1e1e1e;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 12px;
    border-radius: 4px;
    font-size: 13px;
    resize: vertical;
    font-family: inherit;
}

.remarks-input:focus {
    outline: none;
    border-color: #00bcd4;
}

.history-list {
    max-height: 120px;
    overflow-y: auto;
}

.history-item {
    display: flex;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid #3a3a3a;
    font-size: 12px;
}

.history-time {
    color: #888;
    width: 70px;
}

.history-action {
    color: #b0b0b0;
    width: 100px;
}

.history-value {
    color: #e0e0e0;
    flex: 1;
}

.modal-footer {
    padding: 16px 24px;
    background: #2a2a2a;
    border-top: 1px solid #3a3a3a;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-left,
.footer-right {
    display: flex;
    gap: 12px;
}

/* 自定义滚动条 */
.edit-area::-webkit-scrollbar {
    width: 6px;
}

.edit-area::-webkit-scrollbar-track {
    background: #2a2a2a;
}

.edit-area::-webkit-scrollbar-thumb {
    background: #4a4a4a;
    border-radius: 3px;
}

.edit-area::-webkit-scrollbar-thumb:hover {
    background: #5a5a5a;
}
</style>