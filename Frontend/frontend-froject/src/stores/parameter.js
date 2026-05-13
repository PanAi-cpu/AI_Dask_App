// src/stores/parameter.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useParameterStore = defineStore('parameter', () => {
  console.log('Parameter store initializing...')
  
  // ========== 核心参数 ==========
  const confidenceThreshold = ref(65)
  const iouThreshold = ref(0.5)
  const ngCount = ref(3)
  
  // ========== 高级参数 ==========
  const minArea = ref(50)
  const maxArea = ref(5000)
  const sensitivity = ref('medium')
  const mergeStrategy = ref('nearby')
  
  // ========== ROI区域 ==========
  const roi = ref({
    x: 0.2,
    y: 0.15,
    width: 0.6,
    height: 0.7
  })
  
  console.log('ROI initialized:', roi.value)
  
  // ========== 预设 ==========
  const selectedPreset = ref('default')
  
  // ========== 方法 ==========
  const applyPreset = (preset) => {
    console.log('Applying preset:', preset)
    selectedPreset.value = preset
    
    switch (preset) {
      case 'default':
        confidenceThreshold.value = 65
        iouThreshold.value = 0.5
        ngCount.value = 3
        minArea.value = 50
        maxArea.value = 5000
        sensitivity.value = 'medium'
        mergeStrategy.value = 'nearby'
        break
      case 'strict':
        confidenceThreshold.value = 85
        iouThreshold.value = 0.7
        ngCount.value = 5
        minArea.value = 100
        maxArea.value = 3000
        sensitivity.value = 'low'
        mergeStrategy.value = 'overlap'
        break
      case 'sensitive':
        confidenceThreshold.value = 45
        iouThreshold.value = 0.3
        ngCount.value = 2
        minArea.value = 20
        maxArea.value = 8000
        sensitivity.value = 'high'
        mergeStrategy.value = 'nearby'
        break
    }
  }

  const resetRoi = () => {
    roi.value = { x: 0.2, y: 0.15, width: 0.6, height: 0.7 }
  }

  const setFullRoi = () => {
    roi.value = { x: 0, y: 0, width: 1, height: 1 }
  }

  const saveParameters = () => {
    console.log('保存参数', {
      confidence: confidenceThreshold.value,
      iou: iouThreshold.value,
      ngCount: ngCount.value,
      minArea: minArea.value,
      maxArea: maxArea.value,
      sensitivity: sensitivity.value,
      mergeStrategy: mergeStrategy.value,
      roi: roi.value
    })
    return Promise.resolve({ status: 'success' })
  }

  return {
    confidenceThreshold,
    iouThreshold,
    ngCount,
    minArea,
    maxArea,
    sensitivity,
    mergeStrategy,
    roi,
    selectedPreset,
    applyPreset,
    resetRoi,
    setFullRoi,
    saveParameters
  }
})