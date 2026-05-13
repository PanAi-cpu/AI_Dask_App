<!-- src/components/layout/MainLayout.vue -->
<!-- 主布局设置 -->
<template>
  <div class="app">
    <!-- 左侧导航栏 -->
    <nav class="sidebar">
      <div class="logo">
        <span class="logo-text">AI 布匹检测</span>
        <span class="logo-badge">v2.1.0</span>
      </div>

      <div class="nav-menu">
        <div v-for="item in navItems" :key="item.path" class="nav-item" :class="{ active: currentPath === item.path }"
          @click="navigateTo(item.path)">
          <i :class="item.icon"></i>
          <span>{{ item.name }}</span>
          <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
        </div>
      </div>
    </nav>

    <!-- 中间主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <KeepAlive>
          <component :is="Component" />
        </KeepAlive>
      </router-view>
    </main>

    <!-- 可拖拽的分割线 -->
    <div class="resizer right-resizer" @mousedown="startResize('right', $event)"></div>

    <!-- 右侧瑕疵面板 -->
    <aside class="defect-panel" ref="rightPanel" :style="{ width: rightPanelWidth + 'px' }">
      <div class="panel-header">
        <h3>瑕疵列表 <span class="defect-count">({{ defectStore.totalDefects }})</span></h3>
        <button class="panel-close" @click="toggleRightPanel" title="缩放">
          <span v-if="rightPanelWidth > 100">◀</span>
          <span v-else>▶</span>
        </button>
      </div>
      <div class="panel-content">
        <DefectList @edit-defect="handleEditDefect" />
      </div>
    </aside>

    <!-- 缺陷编辑模态框 -->
    <DefectEditModal v-model:visible="defectStore.showEditModal" :defect="defectStore.currentDefect"
      @save="handleSaveDefect" @delete="handleDeleteDefect" @next="handleNextDefect" />
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDefectStore } from '../../stores/defect'  // 注意路径
import DefectList from '../defects/DefectList.vue'
import DefectEditModal from '../defects/DefectEditModal.vue'

const router = useRouter()
const route = useRoute()
const currentPath = ref(route.path)

// 使用 store
const defectStore = useDefectStore()
console.log('DefectStore loaded:', defectStore)  // 调试用

// 监听路由变化
watch(() => route.path, (newPath) => {
  currentPath.value = newPath
})

const navItems = [
  { path: '/dashboard', name: '工作台', icon: 'icon-dashboard', badge: null },
  { path: '/dashboard-large', name: '实时可视化', icon: 'icon-chart', badge: null },
  { path: '/parameters', name: '参数调整', icon: 'icon-sliders', badge: null },
  { path: '/camera', name: '摄像头设置', icon: 'icon-camera', badge: null },
  { path: '/defect-config', name: '识别项目设置', icon: 'icon-tags', badge: null },
  { path: '/logs', name: '日志与报表', icon: 'icon-chart', badge: null },
  { path: '/templates', name: '模板管理', icon: 'icon-template', badge: null },
  { path: '/diagnostics', name: '系统诊断', icon: 'icon-diagnose', badge: null },
  { path: '/users', name: '用户管理', icon: 'icon-users', badge: null }
]

// 右侧面板宽度控制
const rightPanelWidth = ref(320)
const rightPanel = ref(null)
const resizing = ref(null)
const startX = ref(0)
const startWidth = ref(0)

const startResize = (side, e) => {
  e.preventDefault()
  resizing.value = side
  startX.value = e.clientX
  if (side === 'right') {
    startWidth.value = rightPanelWidth.value
  }
  document.addEventListener('mousemove', onResize)
  document.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'col-resize'
  document.body.classList.add('resizing')
}

const onResize = (e) => {
  if (!resizing.value) return
  const delta = e.clientX - startX.value
  if (resizing.value === 'right') {
    const newWidth = Math.min(600, Math.max(250, startWidth.value - delta))
    rightPanelWidth.value = newWidth
  }
}

const stopResize = () => {
  resizing.value = null
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
  document.body.classList.remove('resizing')
}

const toggleRightPanel = () => {
  if (rightPanelWidth.value < 100) {
    rightPanelWidth.value = 320
  } else {
    rightPanelWidth.value = 40
  }
}

const navigateTo = (path) => {
  currentPath.value = path
  router.push(path)
}

// 操作函数直接调用 store 的方法
const handleEditDefect = (defect) => {
  defectStore.openEditModal(defect)
}

const handleSaveDefect = (updatedDefect) => {
  defectStore.saveDefect(updatedDefect)
}

const handleDeleteDefect = (defectId) => {
  defectStore.deleteDefect(defectId)
}

const handleNextDefect = () => {
  defectStore.nextDefect()
}

// 清理事件监听
onUnmounted(() => {
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.classList.remove('resizing')
})
</script>

<style scoped>
/* 全局禁止文本选择在拖拽时 */
:global(body.resizing) {
  user-select: none;
  -webkit-user-select: none;
  cursor: col-resize !important;
}

.app {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: #1e1e1e;
  position: relative;
}

/* 左侧导航栏 - 固定宽度 */
.sidebar {
  width: 260px;
  background: #2a2a2a;
  border-right: 1px solid #3a3a3a;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
  flex-shrink: 0;
  overflow-y: auto;
}

/* 左侧导航栏滚动条样式 */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: #1a1a1a;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

.logo {
  padding: 0 20px 20px 20px;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #00bcd4;
  letter-spacing: 1px;
}

.logo-badge {
  font-size: 12px;
  background: #3a3a3a;
  padding: 2px 6px;
  border-radius: 4px;
  color: #aaa;
}

.nav-menu {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
}

/* 导航菜单滚动条样式 */
.nav-menu::-webkit-scrollbar {
  width: 4px;
}

.nav-menu::-webkit-scrollbar-track {
  background: transparent;
}

.nav-menu::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 2px;
}

.nav-menu::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  margin: 4px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  color: #b0b0b0;
  position: relative;
}

.nav-item:hover {
  background: #3a3a3a;
  color: #fff;
}

.nav-item.active {
  background: #108b96;
  color: #fff;
  box-shadow: 0 4px 8px rgba(0, 188, 212, 0.3);
}

.nav-item i {
  width: 24px;
  margin-right: 12px;
  font-size: 18px;
}

.nav-badge {
  position: absolute;
  right: 12px;
  background: #ff5722;
  color: #fff;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
}

/* 分割线 - 可拖拽区域 */
.resizer {
  width: 4px;
  height: 100%;
  background: transparent;
  cursor: col-resize;
  transition: background 0.2s;
  flex-shrink: 0;
  position: relative;
  z-index: 10;
}

.resizer:hover,
.resizer:active {
  background: #00bcd4;
}



.right-resizer {
  margin-right: -2px;
}

/* 中间主内容区 */
.main-content {
  flex: 1;
  min-width: 400px;
  background: #1e1e1e;
  overflow-y: auto;
  padding: 16px;
}

/* 主内容区滚动条样式 */
.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: #2a2a2a;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

/* 右侧瑕疵面板 */
.defect-panel {
  background: #2a2a2a;
  border-left: 1px solid #3a3a3a;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
  transition: width 0.1s;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.2);
}

.panel-header {
  padding: 16px 16px 12px 16px;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.panel-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #e0e0e0;
  margin: 0;
}

.defect-count {
  color: #00bcd4;
  font-size: 14px;
  margin-left: 4px;
}

.panel-close {
  width: 24px;
  height: 24px;
  border: none;
  background: #3a3a3a;
  color: #b0b0b0;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.2s;
}

.panel-close:hover {
  background: #4a4a4a;
  color: #fff;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

/* 右侧面板滚动条样式 */
.panel-content::-webkit-scrollbar {
  width: 6px;
}

.panel-content::-webkit-scrollbar-track {
  background: #1a1a1a;
  border-radius: 3px;
}

.panel-content::-webkit-scrollbar-thumb {
  background: #4a4a4a;
  border-radius: 3px;
}

.panel-content::-webkit-scrollbar-thumb:hover {
  background: #5a5a5a;
}

/* 缺陷列表项样式 */
.defect-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 6px;
  background: #323232;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.defect-item:hover {
  background: #3a3a3a;
  border-color: #00bcd4;
}

.defect-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  flex-shrink: 0;
}

.defect-info {
  flex: 1;
  min-width: 0;
}

.defect-title {
  font-size: 14px;
  font-weight: 500;
  color: #e0e0e0;
  margin-bottom: 4px;
}

.defect-time {
  font-size: 11px;
  color: #888;
}

/* 当面板很窄时的特殊样式 */
.defect-panel[style*="width: 40px"] .panel-header h3,
.defect-panel[style*="width: 40px"] .defect-info,
.defect-panel[style*="width: 40px"] .defect-count {
  display: none;
}

.defect-panel[style*="width: 40px"] .panel-header {
  padding: 16px 8px;
  justify-content: center;
}

.defect-panel[style*="width: 40px"] .defect-item {
  padding: 8px;
  justify-content: center;
}

.defect-panel[style*="width: 40px"] .defect-color {
  width: 20px;
  height: 20px;
}
</style>