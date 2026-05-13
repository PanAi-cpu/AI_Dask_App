// src/stores/defect.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useDefectStore = defineStore('defect', () => {
  // ========== 状态数据 ==========
  // 缺陷列表（从 MainLayout.vue 移过来）
  const defectList = ref([
    { id: 1, type: '破洞', confidence: 96, status: 'pending', time: '14:23:05', x: 0.3, y: 0.2, width: 0.15, height: 0.1, remarks: '', image: null },
    { id: 2, type: '脏污', confidence: 82, status: 'confirmed', time: '14:18:45', x: 0.6, y: 0.5, width: 0.2, height: 0.15, remarks: '轻微脏污，可接受', image: null },
    { id: 3, type: '划痕', confidence: 91, status: 'pending', time: '14:22:10', x: 0.2, y: 0.7, width: 0.25, height: 0.05, remarks: '', image: null },
    { id: 4, type: '破洞', confidence: 88, status: 'confirmed', time: '14:15:23', x: 0.4, y: 0.3, width: 0.1, height: 0.1, remarks: '已确认', image: null },
    { id: 5, type: '色差', confidence: 79, status: 'pending', time: '14:25:30', x: 0.7, y: 0.4, width: 0.18, height: 0.12, remarks: '', image: null },
    { id: 6, type: '毛丝', confidence: 93, status: 'pending', time: '14:28:15', x: 0.5, y: 0.6, width: 0.3, height: 0.08, remarks: '', image: null },
    { id: 7, type: '脏污', confidence: 85, status: 'confirmed', time: '14:30:22', x: 0.2, y: 0.3, width: 0.15, height: 0.15, remarks: '油污', image: null },
    { id: 8, type: '破洞', confidence: 97, status: 'pending', time: '14:32:45', x: 0.8, y: 0.5, width: 0.12, height: 0.1, remarks: '严重破洞', image: null },
    { id: 9, type: '划痕', confidence: 76, status: 'confirmed', time: '14:35:12', x: 0.3, y: 0.4, width: 0.2, height: 0.05, remarks: '表面划痕', image: null },
    { id: 10, type: '色差', confidence: 81, status: 'pending', time: '14:38:30', x: 0.6, y: 0.2, width: 0.25, height: 0.15, remarks: '', image: null },
    { id: 11, type: '毛丝', confidence: 89, status: 'pending', time: '14:41:18', x: 0.4, y: 0.7, width: 0.2, height: 0.1, remarks: '', image: null },
    { id: 12, type: '破洞', confidence: 94, status: 'confirmed', time: '14:45:03', x: 0.5, y: 0.3, width: 0.15, height: 0.12, remarks: '边缘破损', image: null }
  ])

  // 当前选中的缺陷
  const currentDefect = ref(null)
  
  // 编辑模态框显示状态
  const showEditModal = ref(false)

  // 加载状态
  const loading = ref(false)
  
  // 错误信息
  const error = ref(null)

  // ========== 计算属性 ==========
  // 缺陷总数
  const totalDefects = computed(() => defectList.value.length)
  
  // 待处理缺陷数量
  const pendingCount = computed(() => 
    defectList.value.filter(d => d.status === 'pending').length
  )
  
  // 已确认缺陷数量
  const confirmedCount = computed(() => 
    defectList.value.filter(d => d.status === 'confirmed').length
  )

  // ========== 操作方法 ==========
  
  // 打开编辑模态框
  const openEditModal = (defect) => {
    currentDefect.value = defect
    showEditModal.value = true
  }

  // 关闭编辑模态框
  const closeEditModal = () => {
    showEditModal.value = false
    currentDefect.value = null
  }

  // 保存缺陷
  const saveDefect = (updatedDefect) => {
    const index = defectList.value.findIndex(d => d.id === updatedDefect.id)
    if (index !== -1) {
      defectList.value[index] = updatedDefect
      console.log('缺陷已更新:', updatedDefect)
    }
    closeEditModal()
  }

  // 删除缺陷
  const deleteDefect = (defectId) => {
    defectList.value = defectList.value.filter(d => d.id !== defectId)
    console.log('缺陷已删除, ID:', defectId)
    closeEditModal()
  }

  // 查找下一个待处理的缺陷
  const findNextPendingDefect = (currentId) => {
    const currentIndex = defectList.value.findIndex(d => d.id === currentId)
    
    // 找下一个待处理的
    for (let i = currentIndex + 1; i < defectList.value.length; i++) {
      if (defectList.value[i].status === 'pending') {
        return defectList.value[i]
      }
    }
    
    // 如果后面没有，从头找
    for (let i = 0; i < currentIndex; i++) {
      if (defectList.value[i].status === 'pending') {
        return defectList.value[i]
      }
    }
    
    return null
  }

  // 切换到下一个缺陷
  const nextDefect = () => {
    if (!currentDefect.value) return
    
    const next = findNextPendingDefect(currentDefect.value.id)
    if (next) {
      currentDefect.value = next
      showEditModal.value = true
    } else {
      alert('没有更多待处理的缺陷了')
      closeEditModal()
    }
  }

  // ========== 后端 API 调用（等后端好了再实现）==========
  
  // 从后端获取缺陷列表
  const fetchDefects = async () => {
    loading.value = true
    try {
      // TODO: 等后端接口
      // const res = await window.pywebview.api.get_defects()
      // defectList.value = res.data
      
      // 现在先用假数据
      console.log('从后端获取缺陷列表')
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  // 更新缺陷到后端
  const updateDefect = async (defect) => {
    try {
      // TODO: 等后端接口
      // await window.pywebview.api.update_defect(defect)
      saveDefect(defect)
    } catch (err) {
      error.value = err.message
    }
  }

  return {
    // 状态
    defectList,
    currentDefect,
    showEditModal,
    loading,
    error,
    
    // 计算属性
    totalDefects,
    pendingCount,
    confirmedCount,
    
    // 方法
    openEditModal,
    closeEditModal,
    saveDefect,
    deleteDefect,
    nextDefect,
    fetchDefects,
    updateDefect
  }
})