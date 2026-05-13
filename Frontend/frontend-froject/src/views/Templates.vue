<!-- src/views/Templates.vue -->
<!-- 模板管理页面 - 产品配置库 -->
<template>
  <div class="templates">
    <h2 class="page-title">模板管理</h2>
    <p class="page-desc">管理不同产品的检测配置模板，快速切换生产型号</p>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>

    <!-- 模板列表 -->
    <div class="templates-section">
      <div class="section-header">
        <h3>产品模板库</h3>
        <div class="header-controls">
          <button class="btn primary" @click="showNewTemplateModal = true" title="快捷键：Ctrl+N">
            <span class="btn-icon">+</span> 新建模板
          </button>
          <button class="btn secondary" @click="importTemplate">
            <span class="btn-icon">↓</span> 导入
          </button>
          <button class="btn secondary" @click="exportAllTemplates" title="导出所有模板">
            <span class="btn-icon">↑</span> 全部导出
          </button>
        </div>
      </div>

      <!-- 搜索和筛选 -->
      <div class="search-bar">
        <div class="search-input">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索模板名称、产品型号..."
            @input="handleSearch"
          >
          <button 
            v-if="searchQuery" 
            class="clear-search" 
            @click="searchQuery = ''"
            title="清除搜索"
          >×</button>
        </div>
        <select v-model="categoryFilter" class="filter-select" @change="handleFilterChange">
          <option value="all">全部分类</option>
          <option value="fabric">布料</option>
          <option value="packaging">包装</option>
          <option value="industrial">工业用</option>
        </select>
        <select v-model="sortBy" class="filter-select" @change="handleSortChange">
          <option value="name">按名称</option>
          <option value="date">按日期</option>
          <option value="usage">按使用次数</option>
        </select>
      </div>

      <!-- 模板统计 -->
      <div class="template-stats">
        <span>共 {{ filteredTemplates.length }} 个模板</span>
        <span>当前显示 {{ paginatedTemplates.length }} 个</span>
      </div>

      <!-- 模板卡片网格 -->
      <div class="template-grid">
        <div v-if="paginatedTemplates.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <h4>暂无匹配的模板</h4>
          <p>试试调整搜索条件或新建模板</p>
          <button class="btn primary" @click="showNewTemplateModal = true">
            新建模板
          </button>
        </div>

        <div 
          v-for="template in paginatedTemplates" 
          :key="template.id" 
          class="template-card"
          :class="{ 'active': template.id === currentTemplate }"
        >
          <div class="card-header">
            <div class="template-icon" :style="{ background: template.color }">
              {{ template.icon }}
            </div>
            <div class="template-info">
              <h4>{{ template.name }}</h4>
              <span class="template-category">{{ template.category }}</span>
            </div>
            <div class="template-actions">
              <button class="action-btn" @click="editTemplate(template)" title="编辑">✎</button>
              <button class="action-btn" @click="copyTemplate(template)" title="复制">⎘</button>
              <button class="action-btn" @click="exportTemplate(template)" title="导出">↑</button>
              <button class="action-btn" @click="deleteTemplate(template)" title="删除">✕</button>
            </div>
          </div>

          <div class="card-body">
            <div class="template-detail">
              <span class="detail-label">产品型号</span>
              <span class="detail-value">{{ template.model }}</span>
            </div>
            <div class="template-detail">
              <span class="detail-label">缺陷类型</span>
              <span class="detail-value">{{ template.defectTypes }}种</span>
            </div>
            <div class="template-detail">
              <span class="detail-label">最后使用</span>
              <span class="detail-value">{{ formatDate(template.lastUsed) }}</span>
            </div>
            <div class="template-detail">
              <span class="detail-label">使用次数</span>
              <span class="detail-value">{{ template.usageCount }}次</span>
            </div>
          </div>

          <div class="card-footer">
            <div class="tag-list">
              <span v-for="tag in template.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
            <button 
              class="btn primary small" 
              @click="applyTemplate(template)"
              :disabled="template.id === currentTemplate || isLoading"
            >
              {{ template.id === currentTemplate ? '使用中' : '应用模板' }}
            </button>
          </div>

          <!-- 当前使用标记 -->
          <div v-if="template.id === currentTemplate" class="current-badge">当前使用</div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="pagination">
        <button 
          class="page-btn" 
          :disabled="currentPage === 1" 
          @click="currentPage--"
        >←</button>
        
        <div class="page-numbers">
          <button 
            v-for="page in visiblePages" 
            :key="page"
            class="page-number"
            :class="{ active: currentPage === page }"
            @click="currentPage = page"
          >{{ page }}</button>
        </div>
        
        <button 
          class="page-btn" 
          :disabled="currentPage === totalPages" 
          @click="currentPage++"
        >→</button>
      </div>
    </div>

    <!-- 快速切换区域 -->
    <div class="quick-switch-section">
      <h3>快速切换</h3>
      <div class="quick-switch-grid">
        <div 
          v-for="template in recentTemplates" 
          :key="template.id" 
          class="quick-switch-item" 
          @click="applyTemplate(template)"
        >
          <div class="item-icon" :style="{ background: template.color }">{{ template.icon }}</div>
          <div class="item-info">
            <div class="item-name">{{ template.name }}</div>
            <div class="item-model">{{ template.model }}</div>
          </div>
          <button 
            class="apply-btn"
            :disabled="template.id === currentTemplate"
          >{{ template.id === currentTemplate ? '使用中' : '应用' }}</button>
        </div>
      </div>
    </div>

    <!-- 模板对比 -->
    <div class="compare-section">
      <h3>模板对比</h3>
      <div class="compare-selector">
        <select v-model="compareA" class="compare-select">
          <option value="">选择模板A</option>
          <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
        <span class="vs">VS</span>
        <select v-model="compareB" class="compare-select">
          <option value="">选择模板B</option>
          <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
        <button 
          class="btn secondary" 
          @click="compareTemplates" 
          :disabled="!compareA || !compareB || isLoading"
        >对比</button>
      </div>

      <!-- 对比结果 -->
      <div v-if="showComparison" class="compare-result">
        <div class="compare-table">
          <div class="compare-row header">
            <div class="compare-cell">参数</div>
            <div class="compare-cell">{{ getTemplateName(compareA) }}</div>
            <div class="compare-cell">{{ getTemplateName(compareB) }}</div>
          </div>
          <div class="compare-row">
            <div class="compare-cell">置信度阈值</div>
            <div class="compare-cell">{{ getTemplateConfig(compareA).confidence }}%</div>
            <div class="compare-cell">{{ getTemplateConfig(compareB).confidence }}%</div>
          </div>
          <div class="compare-row">
            <div class="compare-cell">IOU阈值</div>
            <div class="compare-cell">{{ getTemplateConfig(compareA).iou }}</div>
            <div class="compare-cell">{{ getTemplateConfig(compareB).iou }}</div>
          </div>
          <div class="compare-row">
            <div class="compare-cell">检测区域</div>
            <div class="compare-cell">{{ getTemplateConfig(compareA).region || '中心80%' }}</div>
            <div class="compare-cell">{{ getTemplateConfig(compareB).region || '全画面' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新建模板模态框 -->
    <div v-if="showNewTemplateModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container" @keyup.esc="closeModal">
        <div class="modal-header">
          <h3>新建模板</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group" :class="{ 'has-error': validationErrors.name }">
            <label>模板名称 <span class="required">*</span></label>
            <input 
              type="text" 
              v-model="newTemplate.name" 
              class="form-control" 
              placeholder="例如: 纯棉布标准型"
              @blur="validateField('name')"
            >
            <span v-if="validationErrors.name" class="error-message">
              {{ validationErrors.name }}
            </span>
          </div>
          
          <div class="form-group" :class="{ 'has-error': validationErrors.model }">
            <label>产品型号 <span class="required">*</span></label>
            <input 
              type="text" 
              v-model="newTemplate.model" 
              class="form-control" 
              placeholder="例如: CM-40S"
              @blur="validateField('model')"
            >
            <span v-if="validationErrors.model" class="error-message">
              {{ validationErrors.model }}
            </span>
          </div>
          
          <div class="form-group">
            <label>分类</label>
            <select v-model="newTemplate.category" class="form-control">
              <option value="fabric">布料</option>
              <option value="packaging">包装</option>
              <option value="industrial">工业用</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>基于现有模板</label>
            <select v-model="newTemplate.basedOn" class="form-control">
              <option value="">空白模板</option>
              <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>标签</label>
            <input 
              type="text" 
              v-model="newTemplate.tags" 
              class="form-control" 
              placeholder="用逗号分隔"
            >
            <small class="help-text">多个标签用英文逗号分隔</small>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn secondary" @click="closeModal">取消</button>
          <button 
            class="btn primary" 
            @click="createTemplate"
            :disabled="isLoading || !isFormValid"
          >
            {{ isLoading ? '创建中...' : '创建模板' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 导出进度提示 -->
    <div v-if="exportProgress" class="export-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: exportProgress + '%' }"></div>
      </div>
      <span>导出中... {{ exportProgress }}%</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

// 模板数据
const templates = ref([
  {
    id: 1,
    name: '纯棉布标准型',
    icon: 'T',
    color: '#4caf50',
    category: '布料',
    model: 'CM-40S',
    defectTypes: 5,
    lastUsed: '2024-03-15',
    usageCount: 128,
    tags: ['棉布', '40支', '国标'],
    config: {
      confidence: 65,
      iou: 0.5,
      region: '中心80%',
      defects: [1, 2, 3, 4, 5]
    }
  },
  {
    id: 2,
    name: '涤纶布高精度',
    icon: 'D',
    color: '#2196f3',
    category: '布料',
    model: 'DL-75D',
    defectTypes: 4,
    lastUsed: '2024-03-14',
    usageCount: 86,
    tags: ['涤纶', '高精度', '欧标'],
    config: {
      confidence: 80,
      iou: 0.6,
      region: '全画面',
      defects: [1, 2, 3, 6]
    }
  },
  {
    id: 3,
    name: '食品包装膜',
    icon: 'P',
    color: '#ff9800',
    category: '包装',
    model: 'SP-001',
    defectTypes: 6,
    lastUsed: '2024-03-13',
    usageCount: 45,
    tags: ['食品级', '高速', '美标'],
    config: {
      confidence: 75,
      iou: 0.55,
      region: '中心80%',
      defects: [1, 2, 4, 5, 7, 8]
    }
  },
  {
    id: 4,
    name: '工业帆布',
    icon: 'I',
    color: '#9c27b0',
    category: '工业用',
    model: 'GY-1000',
    defectTypes: 3,
    lastUsed: '2024-03-10',
    usageCount: 23,
    tags: ['厚重', '耐磨', '工业'],
    config: {
      confidence: 60,
      iou: 0.4,
      region: '中心80%',
      defects: [1, 3, 5]
    }
  },
  {
    id: 5,
    name: '混纺布通用型',
    icon: 'H',
    color: '#f44336',
    category: '布料',
    model: 'HF-65/35',
    defectTypes: 5,
    lastUsed: '2024-03-12',
    usageCount: 67,
    tags: ['混纺', '通用', '国标'],
    config: {
      confidence: 70,
      iou: 0.5,
      region: '中心80%',
      defects: [1, 2, 3, 4, 5]
    }
  },
  {
    id: 6,
    name: '医用无纺布',
    icon: 'M',
    color: '#00bcd4',
    category: '工业用',
    model: 'YW-25g',
    defectTypes: 7,
    lastUsed: '2024-03-09',
    usageCount: 34,
    tags: ['医用', '无菌', '高要求'],
    config: {
      confidence: 85,
      iou: 0.7,
      region: '全画面',
      defects: [1, 2, 3, 4, 5, 6, 7]
    }
  }
])

// 状态变量
const currentTemplate = ref(1)
const searchQuery = ref('')
const categoryFilter = ref('all')
const sortBy = ref('name')
const currentPage = ref(1)
const pageSize = 6
const isLoading = ref(false)
const exportProgress = ref(0)

// 模板对比
const compareA = ref('')
const compareB = ref('')
const showComparison = ref(false)

// 新建模板
const showNewTemplateModal = ref(false)
const newTemplate = ref({
  name: '',
  model: '',
  category: 'fabric',
  basedOn: '',
  tags: ''
})

// 表单验证
const validationErrors = ref({
  name: '',
  model: ''
})

// 计算属性
const filteredTemplates = computed(() => {
  let filtered = templates.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.name.toLowerCase().includes(query) ||
      t.model.toLowerCase().includes(query) ||
      t.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  if (categoryFilter.value !== 'all') {
    filtered = filtered.filter(t => t.category === categoryFilter.value)
  }

  filtered.sort((a, b) => {
    if (sortBy.value === 'name') {
      return a.name.localeCompare(b.name)
    } else if (sortBy.value === 'date') {
      return new Date(b.lastUsed) - new Date(a.lastUsed)
    } else if (sortBy.value === 'usage') {
      return b.usageCount - a.usageCount
    }
    return 0
  })

  return filtered
})

const paginatedTemplates = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredTemplates.value.slice(start, start + pageSize)
})

const totalPages = computed(() => {
  return Math.ceil(filteredTemplates.value.length / pageSize)
})

const visiblePages = computed(() => {
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

const recentTemplates = computed(() => {
  return [...templates.value]
    .sort((a, b) => new Date(b.lastUsed) - new Date(a.lastUsed))
    .slice(0, 4)
})

const isFormValid = computed(() => {
  return newTemplate.value.name.trim() && newTemplate.value.model.trim()
})

// 方法
const formatDate = (date) => {
  if (!date) return '从未使用'
  const d = new Date(date)
  const now = new Date()
  const diffTime = Math.abs(now - d)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '今天'
  if (diffDays === 1) return '昨天'
  if (diffDays < 7) return `${diffDays}天前`
  return date
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleFilterChange = () => {
  currentPage.value = 1
}

const handleSortChange = () => {
  currentPage.value = 1
}

const getTemplateName = (id) => {
  const template = templates.value.find(t => t.id === id)
  return template ? template.name : ''
}

const getTemplateConfig = (id) => {
  const template = templates.value.find(t => t.id === id)
  return template ? template.config : { confidence: 0, iou: 0 }
}

const validateField = (field) => {
  if (field === 'name' && !newTemplate.value.name.trim()) {
    validationErrors.value.name = '模板名称不能为空'
  } else {
    validationErrors.value.name = ''
  }
  
  if (field === 'model' && !newTemplate.value.model.trim()) {
    validationErrors.value.model = '产品型号不能为空'
  } else {
    validationErrors.value.model = ''
  }
}

const closeModal = () => {
  showNewTemplateModal.value = false
  newTemplate.value = {
    name: '',
    model: '',
    category: 'fabric',
    basedOn: '',
    tags: ''
  }
  validationErrors.value = {
    name: '',
    model: ''
  }
}

const createTemplate = async () => {
  validateField('name')
  validateField('model')
  
  if (!isFormValid.value) return
  
  isLoading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const tagArray = newTemplate.value.tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag)
    
    const newId = Math.max(...templates.value.map(t => t.id)) + 1
    
    const template = {
      id: newId,
      name: newTemplate.value.name,
      icon: newTemplate.value.name.charAt(0).toUpperCase(),
      color: '#00bcd4',
      category: newTemplate.value.category === 'fabric' ? '布料' : 
                newTemplate.value.category === 'packaging' ? '包装' : '工业用',
      model: newTemplate.value.model,
      defectTypes: 0,
      lastUsed: new Date().toISOString().split('T')[0],
      usageCount: 0,
      tags: tagArray,
      config: newTemplate.value.basedOn 
        ? { ...templates.value.find(t => t.id === Number(newTemplate.value.basedOn)).config }
        : { confidence: 70, iou: 0.5, defects: [] }
    }
    
    templates.value.push(template)
    alert('模板创建成功！')
    closeModal()
  } catch (error) {
    alert('创建失败，请重试')
  } finally {
    isLoading.value = false
  }
}

const editTemplate = (template) => {
  console.log('编辑模板:', template)
  alert(`编辑模板: ${template.name} (功能开发中)`)
}

const copyTemplate = async (template) => {
  isLoading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const newId = Math.max(...templates.value.map(t => t.id)) + 1
    const newTemplate = {
      ...template,
      id: newId,
      name: `${template.name} (副本)`,
      usageCount: 0,
      lastUsed: new Date().toISOString().split('T')[0]
    }
    
    templates.value.push(newTemplate)
    alert(`已复制模板: ${template.name}`)
  } finally {
    isLoading.value = false
  }
}

const deleteTemplate = (template) => {
  if (template.id === currentTemplate.value) {
    alert('不能删除当前使用的模板')
    return
  }
  
  if (confirm(`确定要删除模板 "${template.name}" 吗？此操作不可恢复。`)) {
    templates.value = templates.value.filter(t => t.id !== template.id)
    alert(`模板已删除: ${template.name}`)
  }
}

const applyTemplate = async (template) => {
  if (template.id === currentTemplate.value) {
    alert('此模板已在使用中')
    return
  }
  
  isLoading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const index = templates.value.findIndex(t => t.id === template.id)
    if (index !== -1) {
      templates.value[index] = {
        ...template,
        lastUsed: new Date().toISOString().split('T')[0],
        usageCount: template.usageCount + 1
      }
    }
    
    currentTemplate.value = template.id
    alert(`已切换到模板: ${template.name}`)
  } catch (error) {
    alert('应用失败，请重试')
  } finally {
    isLoading.value = false
  }
}

const importTemplate = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    isLoading.value = true
    try {
      const text = await file.text()
      const template = JSON.parse(text)
      
      const newId = Math.max(...templates.value.map(t => t.id)) + 1
      template.id = newId
      template.usageCount = 0
      template.lastUsed = new Date().toISOString().split('T')[0]
      
      templates.value.push(template)
      alert('模板导入成功！')
    } catch (error) {
      alert('导入失败，文件格式不正确')
    } finally {
      isLoading.value = false
    }
  }
  
  input.click()
}

const exportTemplate = (template) => {
  const data = JSON.stringify(template, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${template.name}.json`
  a.click()
  URL.revokeObjectURL(url)
}

const exportAllTemplates = async () => {
  isLoading.value = true
  exportProgress.value = 0
  
  try {
    for (let i = 0; i < templates.value.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 100))
      exportProgress.value = Math.round(((i + 1) / templates.value.length) * 100)
    }
    
    const data = JSON.stringify(templates.value, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `templates_backup_${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
    
    setTimeout(() => {
      exportProgress.value = 0
    }, 1000)
  } finally {
    isLoading.value = false
  }
}

const compareTemplates = () => {
  showComparison.value = true
  console.log('对比模板:', compareA.value, compareB.value)
}

// 键盘快捷键
const handleKeyDown = (e) => {
  if (e.ctrlKey && e.key === 'n') {
    e.preventDefault()
    showNewTemplateModal.value = true
  }
  
  if (e.key === 'Escape' && showNewTemplateModal.value) {
    closeModal()
  }
}

// 生命周期
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})

// 监听筛选条件变化
watch([searchQuery, categoryFilter, sortBy], () => {
  currentPage.value = 1
})
</script>

<style scoped>
.templates {
  height: 100%;
  overflow-y: auto;
  padding-right: 8px;
  position: relative;
  /* Firefox 滚动条样式 */
  scrollbar-width: thin;
  scrollbar-color: #555 #2a2a2a;
}

/* Chrome, Edge, Safari 滚动条样式 */
.templates::-webkit-scrollbar {
  width: 8px;
}

.templates::-webkit-scrollbar-track {
  background: #2a2a2a;
  border-radius: 4px;
}

.templates::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.templates::-webkit-scrollbar-thumb:hover {
  background: #777;
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

/* 加载状态 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #3a3a3a;
  border-top-color: #00bcd4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 模板列表区域 */
.templates-section {
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
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0;
}

.header-controls {
  display: flex;
  gap: 12px;
}

.btn-icon {
  margin-right: 4px;
}

/* 搜索栏 */
.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.search-input {
  flex: 1;
  display: flex;
  align-items: center;
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  border-radius: 4px;
  padding: 0 12px;
  position: relative;
}

.search-icon {
  color: #666;
  margin-right: 8px;
}

.search-input input {
  flex: 1;
  background: none;
  border: none;
  color: #e0e0e0;
  padding: 10px 0;
  outline: none;
  font-size: 13px;
}

.clear-search {
  background: none;
  border: none;
  color: #666;
  font-size: 18px;
  cursor: pointer;
  padding: 0 4px;
}

.clear-search:hover {
  color: #fff;
}

.filter-select {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 0 12px;
  border-radius: 4px;
  font-size: 13px;
  min-width: 120px;
  cursor: pointer;
}

.filter-select:hover {
  border-color: #00bcd4;
}

/* 模板统计 */
.template-stats {
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 12px;
  margin-bottom: 16px;
  padding: 0 4px;
}

/* 模板卡片网格 */
.template-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 20px;
  min-height: 400px;
}

.template-card {
  background: #1e1e1e;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
  position: relative;
  transition: all 0.2s;
}

.template-card:hover {
  transform: translateY(-2px);
  border-color: #00bcd4;
  box-shadow: 0 4px 12px rgba(0, 188, 212, 0.2);
}

.template-card.active {
  border-color: #00bcd4;
  box-shadow: 0 0 0 2px rgba(0, 188, 212, 0.3);
}

.current-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #00bcd4;
  color: #fff;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  z-index: 1;
}

.card-header {
  padding: 16px;
  background: #252525;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  align-items: center;
  gap: 12px;
}

.template-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.template-info {
  flex: 1;
}

.template-info h4 {
  font-size: 14px;
  color: #e0e0e0;
  margin: 0 0 4px 0;
}

.template-category {
  font-size: 11px;
  color: #888;
}

.template-actions {
  display: flex;
  gap: 4px;
}

.action-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #3a3a3a;
  color: #fff;
}

.card-body {
  padding: 16px;
}

.template-detail {
  display: flex;
  margin-bottom: 8px;
  font-size: 12px;
}

.detail-label {
  width: 70px;
  color: #888;
}

.detail-value {
  flex: 1;
  color: #e0e0e0;
}

.card-footer {
  padding: 12px 16px;
  background: #252525;
  border-top: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag-list {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.tag {
  background: #2a2a2a;
  color: #888;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
}

/* 空状态 */
.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 40px;
  color: #888;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.empty-state h4 {
  font-size: 18px;
  color: #e0e0e0;
  margin-bottom: 8px;
}

.empty-state p {
  margin-bottom: 20px;
}

/* 快速切换区域 */
.quick-switch-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.quick-switch-section h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0 0 16px 0;
}

.quick-switch-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.quick-switch-item {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  border-radius: 6px;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-switch-item:hover {
  border-color: #00bcd4;
  background: #252525;
}

.item-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: 13px;
  color: #e0e0e0;
  margin-bottom: 2px;
}

.item-model {
  font-size: 11px;
  color: #888;
}

.apply-btn {
  background: #3a3a3a;
  border: none;
  color: #e0e0e0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
}

.quick-switch-item:hover .apply-btn {
  opacity: 1;
}

.apply-btn:hover:not(:disabled) {
  background: #00bcd4;
}

.apply-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  background: #2a2a2a;
}

/* 模板对比区域 */
.compare-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.compare-section h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0 0 16px 0;
}

.compare-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.compare-select {
  flex: 1;
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 10px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.compare-select:hover {
  border-color: #00bcd4;
}

.vs {
  color: #888;
  font-weight: 600;
  font-size: 14px;
}

.compare-result {
  background: #1e1e1e;
  border-radius: 6px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
}

.compare-table {
  width: 100%;
}

.compare-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  border-bottom: 1px solid #3a3a3a;
}

.compare-row.header {
  background: #252525;
  font-weight: 600;
}

.compare-cell {
  padding: 12px;
  font-size: 13px;
  color: #e0e0e0;
  border-right: 1px solid #3a3a3a;
}

.compare-cell:last-child {
  border-right: none;
}

.header .compare-cell {
  color: #888;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}

.page-numbers {
  display: flex;
  gap: 4px;
}

.page-btn, .page-number {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-number {
  width: auto;
  min-width: 32px;
  padding: 0 4px;
}

.page-btn:hover:not(:disabled),
.page-number:hover:not(.active) {
  background: #3a3a3a;
  border-color: #00bcd4;
}

.page-number.active {
  background: #00bcd4;
  border-color: #00bcd4;
  color: #fff;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  color: #888;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-container {
  width: 500px;
  background: #2a2a2a;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 16px 20px;
  background: #252525;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  font-size: 16px;
  color: #e0e0e0;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 20px;
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #3a3a3a;
  color: #fff;
}

.modal-body {
  padding: 20px;
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

.required {
  color: #f44336;
}

.help-text {
  display: block;
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.form-control {
  width: 100%;
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  transition: all 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #00bcd4;
}

.form-group.has-error .form-control {
  border-color: #f44336;
}

.error-message {
  display: block;
  font-size: 11px;
  color: #f44336;
  margin-top: 4px;
}

.modal-footer {
  padding: 16px 20px;
  background: #252525;
  border-top: 1px solid #3a3a3a;
  display: flex;
  justify-content: flex-end;
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
}

.btn.secondary {
  background: #3a3a3a;
  color: #e0e0e0;
}

.btn.secondary:hover:not(:disabled) {
  background: #4a4a4a;
}

.btn.small {
  padding: 6px 12px;
  font-size: 12px;
}

/* 导出进度 */
.export-progress {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #2a2a2a;
  border: 1px solid #00bcd4;
  border-radius: 8px;
  padding: 16px;
  min-width: 200px;
  z-index: 1500;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.progress-bar {
  height: 4px;
  background: #1e1e1e;
  border-radius: 2px;
  margin-bottom: 8px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #00bcd4;
  transition: width 0.3s ease;
}

/* 响应式 */
@media (max-width: 1400px) {
  .template-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .quick-switch-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .search-bar {
    flex-direction: column;
  }
  
  .filter-select {
    width: 100%;
  }
  
  .compare-selector {
    flex-direction: column;
  }
  
  .vs {
    align-self: center;
  }
  
  .page-numbers {
    display: none;
  }
}

@media (max-width: 900px) {
  .template-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-switch-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-container {
    width: 90%;
  }
  
  .header-controls {
    flex-direction: column;
  }
}
</style>