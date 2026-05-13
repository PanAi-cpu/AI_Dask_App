<!-- src/components/defects/DefectList.vue -->
<!-- 缺陷列表管理界面 -->
<template>
  <div class="defect-list">
    <!-- 筛选栏 -->
    <div class="filter-bar">
      <select v-model="filterType" class="filter-select" @change="resetPage">
        <option value="all">全部类型 ({{ totalCount }})</option>
        <option v-for="type in defectTypes" :key="type" :value="type">
          {{ type }} ({{ getTypeCount(type) }})
        </option>
      </select>
      <select v-model="filterStatus" class="filter-select" @change="resetPage">
        <option value="all">全部状态</option>
        <option value="pending">未处理 ({{ getStatusCount('pending') }})</option>
        <option value="confirmed">已确认 ({{ getStatusCount('confirmed') }})</option>
      </select>
    </div>

    <!-- 缩略图网格 -->
    <div class="thumbnail-grid" ref="gridContainer">
      <div v-for="defect in paginatedDefects" :key="defect.id" class="thumbnail-card"
        :class="{ pending: defect.status === 'pending' }" @click="openEditModal(defect)">

        <div class="thumbnail-image" :style="{ background: getDefectColor(defect.type) }">
          <span class="thumbnail-confidence">{{ defect.confidence }}%</span>
          <!-- 缺陷形状示意 -->
          <div class="defect-shape" :class="defect.type"></div>
        </div>

        <div class="thumbnail-info">
          <div class="thumbnail-header">
            <span class="thumbnail-type">{{ defect.type }}</span>
            <span class="thumbnail-time">{{ defect.time }}</span>
          </div>
          <div class="thumbnail-footer">
            <span class="thumbnail-id">#{{ defect.id }}</span>
            <span class="status-badge" :class="defect.status">
              {{ defect.status === 'pending' ? '待处理' : '已确认' }}
            </span>
          </div>
        </div>
      </div>

      <!-- 空状态显示 -->
      <div v-if="paginatedDefects.length === 0" class="empty-state">
        没有符合条件的缺陷
      </div>
    </div>

    <!-- 分页 - 只在需要时显示 -->
    <div class="pagination" v-if="totalPages > 1">
      <button class="page-btn" :disabled="currentPage === 1" @click="prevPage">
        <span class="page-arrow">←</span>
      </button>

      <div class="page-numbers">
        <button v-for="page in displayedPages" :key="page" class="page-number" :class="{ active: currentPage === page }"
          @click="goToPage(page)">
          {{ page }}
        </button>
      </div>

      <button class="page-btn" :disabled="currentPage === totalPages" @click="nextPage">
        <span class="page-arrow">→</span>
      </button>

      <span class="page-info">
        第 {{ currentPage }} / {{ totalPages }} 页
        (共 {{ filteredDefects.length }} 条)
      </span>
    </div>

    <!-- 简单分页信息 -->
    <div class="simple-pagination" v-else-if="filteredDefects.length > 0">
      <span class="total-info">共 {{ filteredDefects.length }} 条缺陷</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useDefectStore } from '../../stores/defect'  // 导入 store

// 不再需要 props 了
const emit = defineEmits(['edit-defect'])

// 直接从 store 拿数据
const defectStore = useDefectStore()

// 缺陷数据直接从 store 获取
const defectsData = computed(() => defectStore.defectList)

// ... 后面的代码不变，但不再需要 props.defects
// 把之前用 props.defects 的地方都改成 defectsData.value

const defectTypes = ['破洞', '脏污', '划痕', '色差', '毛丝']

// 筛选条件
const filterType = ref('all')
const filterStatus = ref('all')
const currentPage = ref(1)
const pageSize = ref(6)

const resetPage = () => {
  currentPage.value = 1
}

// 计算各类型数量 - 用 defectsData.value
const getTypeCount = (type) => {
  return defectsData.value.filter(d => d.type === type).length
}

// 计算各状态数量
const getStatusCount = (status) => {
  return defectsData.value.filter(d => d.status === status).length
}

// 总数
const totalCount = computed(() => defectsData.value.length)

// 过滤后的缺陷
const filteredDefects = computed(() => {
  return defectsData.value.filter(defect => {
    if (filterType.value !== 'all' && defect.type !== filterType.value) return false
    if (filterStatus.value !== 'all' && defect.status !== filterStatus.value) return false
    return true
  })
})

// 分页后的缺陷
const paginatedDefects = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredDefects.value.slice(start, end)
})

// 总页数
const totalPages = computed(() => {
  return Math.ceil(filteredDefects.value.length / pageSize.value)
})

watch([filterType, filterStatus], () => {
  currentPage.value = 1
})

const displayedPages = computed(() => {
  const delta = 2
  const range = []
  const rangeWithDots = []
  let l

  for (let i = 1; i <= totalPages.value; i++) {
    if (i === 1 || i === totalPages.value || (i >= currentPage.value - delta && i <= currentPage.value + delta)) {
      range.push(i)
    }
  }

  range.forEach((i) => {
    if (l) {
      if (i - l === 2) {
        rangeWithDots.push(l + 1)
      } else if (i - l !== 1) {
        rangeWithDots.push('...')
      }
    }
    rangeWithDots.push(i)
    l = i
  })

  return rangeWithDots
})

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

const goToPage = (page) => {
  if (typeof page === 'number') {
    currentPage.value = page
  }
}

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

// 打开编辑模态框 - 直接调用 store 的方法
const openEditModal = (defect) => {
  defectStore.openEditModal(defect)  // 直接用 store 的方法
}
</script>

<style scoped>
.defect-list {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-bar {
  display: flex;
  gap: 8px;
  padding: 0 4px;
}

.filter-select {
  flex: 1;
  background: #323232;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 8px 8px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  outline: none;
}

.filter-select:hover {
  border-color: #00bcd4;
}

.filter-select:focus {
  border-color: #00bcd4;
  box-shadow: 0 0 0 2px rgba(0, 188, 212, 0.2);
}

.thumbnail-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  overflow-y: auto;
  padding: 4px;
  min-height: 0;
  align-content: start;
}

.thumbnail-card {
  background: #323232;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  border: 1px solid #3a3a3a;
  display: flex;
  flex-direction: column;
}

.thumbnail-card:hover {
  transform: translateY(-2px);
  border-color: #00bcd4;
  box-shadow: 0 4px 12px rgba(0, 188, 212, 0.2);
}

.thumbnail-card.pending {
  border-left: 3px solid #ff9800;
}

.thumbnail-image {
  aspect-ratio: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2a2a2a;
  overflow: hidden;
}

.defect-shape {
  width: 60%;
  height: 60%;
  border-radius: 4px;
  opacity: 0.7;
}

.defect-shape.破洞 {
  background: radial-gradient(circle, transparent 60%, #f44336 60%);
}

.defect-shape.脏污 {
  background: repeating-linear-gradient(45deg, #ff9800 0px, #ff9800 5px, #b26a00 5px, #b26a00 10px);
}

.defect-shape.划痕 {
  height: 2px;
  width: 80%;
  background: #2196f3;
  transform: rotate(45deg);
}

.defect-shape.色差 {
  background: linear-gradient(45deg, #9c27b0 25%, #6a1b9a 25%, #6a1b9a 50%, #9c27b0 50%, #9c27b0 75%, #6a1b9a 75%);
  background-size: 8px 8px;
}

.defect-shape.毛丝 {
  background: repeating-linear-gradient(0deg, #4caf50 0px, #4caf50 2px, #1b5e20 2px, #1b5e20 4px);
}

.thumbnail-confidence {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
  z-index: 1;
}

.thumbnail-info {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 11px;
}

.thumbnail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.thumbnail-type {
  color: #e0e0e0;
  font-weight: 600;
}

.thumbnail-time {
  color: #888;
}

.thumbnail-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.thumbnail-id {
  color: #666;
}

.status-badge {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
}

.status-badge.pending {
  background: #ff9800;
  color: #fff;
}

.status-badge.confirmed {
  background: #4caf50;
  color: #fff;
}

.empty-state {
  grid-column: span 2;
  text-align: center;
  padding: 40px 20px;
  color: #666;
  font-size: 13px;
  background: #2a2a2a;
  border-radius: 8px;
  border: 1px dashed #3a3a3a;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 0;
  flex-wrap: wrap;
  border-top: 1px solid #3a3a3a;
}

.page-btn {
  background: #323232;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #3a3a3a;
  border-color: #00bcd4;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-number {
  min-width: 32px;
  height: 32px;
  background: #323232;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: all 0.2s;
}

.page-number:hover {
  background: #3a3a3a;
  border-color: #00bcd4;
}

.page-number.active {
  background: #00bcd4;
  border-color: #00bcd4;
  color: #fff;
}

.page-info {
  font-size: 11px;
  color: #888;
  margin-left: 8px;
}

.simple-pagination {
  padding: 8px 0;
  text-align: center;
  border-top: 1px solid #3a3a3a;
}

.total-info {
  font-size: 12px;
  color: #888;
}

/* 当面板很窄时的样式 */
:deep(.defect-panel[style*="width: 40px"]) .thumbnail-info,
:deep(.defect-panel[style*="width: 40px"]) .filter-bar,
:deep(.defect-panel[style*="width: 40px"]) .pagination,
:deep(.defect-panel[style*="width: 40px"]) .simple-pagination {
  display: none;
}

:deep(.defect-panel[style*="width: 40px"]) .thumbnail-grid {
  grid-template-columns: 1fr;
}

:deep(.defect-panel[style*="width: 40px"]) .thumbnail-card {
  aspect-ratio: 1;
}

:deep(.defect-panel[style*="width: 40px"]) .thumbnail-image {
  height: 100%;
}
</style>