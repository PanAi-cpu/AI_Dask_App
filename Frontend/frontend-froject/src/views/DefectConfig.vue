<!-- src/views/DefectConfig.vue -->
<!-- 识别项目设置页面 - 配置要检测的缺陷类型和规则 -->
<template>
  <div class="defect-config">
    <h2 class="page-title">识别项目设置</h2>
    <p class="page-desc">配置要检测的缺陷类型、等级和灵敏度</p>

    <!-- 产品型号选择 -->
    <div class="product-section">
      <div class="product-header">
        <h3>当前产品型号</h3>
        <div class="product-controls">
          <select v-model="selectedProduct" class="product-select">
            <option v-for="product in products" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
          <button class="btn secondary">另存为模板</button>
        </div>
      </div>
      <div class="product-info">
        <span class="info-item">规格: {{ currentProduct?.spec }}</span>
        <span class="info-item">客户: {{ currentProduct?.customer }}</span>
        <span class="info-item">标准: {{ currentProduct?.standard }}</span>
      </div>
    </div>

    <!-- 缺陷类型配置 -->
    <div class="defect-types-section">
      <div class="section-header">
        <h3>缺陷类型</h3>
        <button class="btn primary small">+ 添加类型</button>
      </div>

      <div class="defect-types-grid">
        <div v-for="defect in defectTypes" :key="defect.id" class="defect-type-card">
          <div class="card-header">
            <div class="defect-color" :style="{ background: defect.color }"></div>
            <h4>{{ defect.name }}</h4>
            <label class="switch">
              <input type="checkbox" v-model="defect.enabled">
              <span class="slider round"></span>
            </label>
          </div>

          <div class="card-body">
            <div class="severity-selector">
              <span class="label">等级:</span>
              <select v-model="defect.severity">
                <option value="critical">致命</option>
                <option value="major">重缺陷</option>
                <option value="minor">轻缺陷</option>
              </select>
            </div>

            <div class="sensitivity-slider">
              <span class="label">灵敏度:</span>
              <div class="slider-container">
                <input type="range" v-model="defect.sensitivity" min="0" max="100" step="1" class="slider">
                <span class="value">{{ defect.sensitivity }}%</span>
              </div>
            </div>

            <div class="threshold-input">
              <span class="label">阈值:</span>
              <input type="number" v-model="defect.threshold" min="0" max="100" step="1">
              <span>%</span>
            </div>

            <div class="size-limit">
              <span class="label">尺寸范围:</span>
              <div class="size-inputs">
                <input type="number" v-model="defect.minSize" placeholder="最小">
                <span>~</span>
                <input type="number" v-model="defect.maxSize" placeholder="最大">
                <span>mm²</span>
              </div>
            </div>
          </div>

          <div class="card-footer">
            <button class="btn-icon" @click="editDefect(defect)">编辑</button>
            <button class="btn-icon" @click="copyDefect(defect)">信息</button>
            <button class="btn-icon" @click="deleteDefect(defect)">删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 全局规则配置 -->
    <div class="global-rules-section">
      <h3>全局规则</h3>

      <div class="rules-grid">
        <div class="rule-item">
          <label>同一位置重复检测次数</label>
          <div class="number-input">
            <input type="number" v-model="globalRules.repeatCount" min="1" max="10">
            <span>次</span>
          </div>
        </div>

        <div class="rule-item">
          <label>缺陷最小间隔</label>
          <div class="number-input">
            <input type="number" v-model="globalRules.minSpacing" min="0" max="100">
            <span>mm</span>
          </div>
        </div>

        <div class="rule-item">
          <label>NG连续触发次数</label>
          <div class="number-input">
            <input type="number" v-model="globalRules.ngTriggerCount" min="1" max="20">
            <span>次</span>
          </div>
        </div>

        <div class="rule-item">
          <label>报警延迟</label>
          <div class="number-input">
            <input type="number" v-model="globalRules.alarmDelay" min="0" max="10">
            <span>秒</span>
          </div>
        </div>

        <div class="rule-item full-width">
          <label>停机条件</label>
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="globalRules.stopOnCritical">
              出现致命缺陷
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="globalRules.stopOnRepeated">
              同一位置连续NG
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="globalRules.stopOnCount">
              NG数量超过
              <input type="number" v-model="globalRules.stopCount" class="inline-input" min="1" max="100">
              个/分钟
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- 检测区域分组 -->
    <div class="region-section">
      <h3>检测区域分组</h3>

      <div class="region-list">
        <div v-for="region in regions" :key="region.id" class="region-item">
          <div class="region-header">
            <span class="region-name">{{ region.name }}</span>
            <div class="region-controls">
              <label class="switch small">
                <input type="checkbox" v-model="region.enabled">
                <span class="slider round"></span>
              </label>
              <button class="btn-icon small" @click="editRegion(region)">编辑</button>
            </div>
          </div>

          <div class="region-defects">
            <span v-for="defectId in region.defectIds" :key="defectId" 
                  class="defect-tag" 
                  :style="{ background: getDefectColor(defectId) }">
              {{ getDefectName(defectId) }}
            </span>
          </div>

          <div class="region-preview">
            <div class="preview-box" :style="getRegionStyle(region)">
              <span class="preview-label">{{ region.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <button class="btn secondary mt-2">+ 添加检测区域</button>
    </div>

    <!-- 底部操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <button class="btn secondary" @click="resetToDefault">恢复默认</button>
        <button class="btn primary" @click="saveConfig">保存配置</button>
        <button class="btn success" @click="applyConfig">应用到当前产品</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 产品列表
const products = ref([
  { id: 1, name: '纯棉布 A型', spec: '40支/130*70', customer: '纺织厂A', standard: '国标一等' },
  { id: 2, name: '涤纶布 B型', spec: '75D/190T', customer: '纺织厂B', standard: '欧标' },
  { id: 3, name: '混纺布 C型', spec: 'T/C 65/35', customer: '纺织厂C', standard: '美标' }
])

const selectedProduct = ref(1)
const currentProduct = computed(() => products.value.find(p => p.id === selectedProduct.value))

// 缺陷类型
const defectTypes = ref([
  { 
    id: 1, 
    name: '破洞', 
    color: '#f44336', 
    enabled: true, 
    severity: 'critical',
    sensitivity: 85,
    threshold: 70,
    minSize: 1,
    maxSize: 100
  },
  { 
    id: 2, 
    name: '脏污', 
    color: '#ff9800', 
    enabled: true, 
    severity: 'major',
    sensitivity: 70,
    threshold: 60,
    minSize: 2,
    maxSize: 200
  },
  { 
    id: 3, 
    name: '划痕', 
    color: '#2196f3', 
    enabled: true, 
    severity: 'major',
    sensitivity: 75,
    threshold: 65,
    minSize: 5,
    maxSize: 500
  },
  { 
    id: 4, 
    name: '色差', 
    color: '#9c27b0', 
    enabled: false, 
    severity: 'minor',
    sensitivity: 60,
    threshold: 50,
    minSize: 10,
    maxSize: 1000
  },
  { 
    id: 5, 
    name: '毛丝', 
    color: '#4caf50', 
    enabled: true, 
    severity: 'minor',
    sensitivity: 65,
    threshold: 55,
    minSize: 1,
    maxSize: 50
  }
])

// 全局规则
const globalRules = ref({
  repeatCount: 3,
  minSpacing: 10,
  ngTriggerCount: 5,
  alarmDelay: 2,
  stopOnCritical: true,
  stopOnRepeated: true,
  stopOnCount: false,
  stopCount: 10
})

// 检测区域
const regions = ref([
  {
    id: 1,
    name: '主检测区',
    enabled: true,
    defectIds: [1, 2, 3],
    x: 0.1,
    y: 0.1,
    width: 0.8,
    height: 0.8
  },
  {
    id: 2,
    name: '边缘检测区',
    enabled: false,
    defectIds: [1, 4],
    x: 0,
    y: 0,
    width: 0.2,
    height: 1
  }
])

// 获取缺陷颜色
const getDefectColor = (defectId) => {
  const defect = defectTypes.value.find(d => d.id === defectId)
  return defect?.color || '#999'
}

// 获取缺陷名称
const getDefectName = (defectId) => {
  const defect = defectTypes.value.find(d => d.id === defectId)
  return defect?.name || '未知'
}

// 获取区域样式
const getRegionStyle = (region) => {
  return {
    left: `${region.x * 100}%`,
    top: `${region.y * 100}%`,
    width: `${region.width * 100}%`,
    height: `${region.height * 100}%`,
    position: 'absolute',
    border: '2px solid #00bcd4',
    background: 'rgba(0, 188, 212, 0.1)'
  }
}

// 操作函数（后面再绑定实际功能）
const editDefect = (defect) => {
  console.log('编辑缺陷:', defect)
}

const copyDefect = (defect) => {
  console.log('复制缺陷:', defect)
}

const deleteDefect = (defect) => {
  console.log('删除缺陷:', defect)
}

const editRegion = (region) => {
  console.log('编辑区域:', region)
}

const resetToDefault = () => {
  console.log('恢复默认')
}

const saveConfig = () => {
  console.log('保存配置', {
    product: selectedProduct.value,
    defects: defectTypes.value,
    globalRules: globalRules.value,
    regions: regions.value
  })
  alert('配置已保存')
}

const applyConfig = () => {
  console.log('应用配置')
  alert('配置已应用到当前产品')
}
</script>

<style scoped>
.defect-config {
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

/* 产品型号区域 */
.product-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 16px 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.product-header h3 {
  font-size: 16px;
  color: #e0e0e0;
  margin: 0;
}

.product-controls {
  display: flex;
  gap: 12px;
}

.product-select {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  min-width: 200px;
}

.product-info {
  display: flex;
  gap: 20px;
}

.info-item {
  font-size: 13px;
  color: #888;
}

/* 缺陷类型区域 */
.defect-types-section {
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
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0;
}

.btn.small {
  padding: 6px 12px;
  font-size: 12px;
}

.defect-types-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.defect-type-card {
  background: #1e1e1e;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
  overflow: hidden;
}

.card-header {
  padding: 12px 16px;
  background: #252525;
  border-bottom: 1px solid #3a3a3a;
  display: flex;
  align-items: center;
  gap: 8px;
}

.defect-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.card-header h4 {
  flex: 1;
  font-size: 14px;
  color: #e0e0e0;
  margin: 0;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #3a3a3a;
  transition: .2s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: #888;
  transition: .2s;
}

input:checked + .slider {
  background-color: #00bcd4;
}

input:checked + .slider:before {
  transform: translateX(22px);
  background-color: #fff;
}

.slider.round {
  border-radius: 22px;
}

.slider.round:before {
  border-radius: 50%;
}

.card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.severity-selector,
.sensitivity-slider,
.threshold-input,
.size-limit {
  display: flex;
  align-items: center;
  gap: 8px;
}

.label {
  font-size: 12px;
  color: #888;
  min-width: 50px;
}

.severity-selector select {
  flex: 1;
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.slider-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.slider-container .slider {
  position: static;
  flex: 1;
  height: 4px;
  background: #3a3a3a;
  border-radius: 2px;
}

.slider-container .slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  background: #00bcd4;
  border-radius: 7px;
  cursor: pointer;
}

.slider-container .value {
  font-size: 12px;
  color: #00bcd4;
  min-width: 40px;
}

.threshold-input input,
.size-inputs input {
  width: 60px;
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 4px;
  border-radius: 4px;
  font-size: 12px;
  text-align: center;
}

.size-inputs {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 4px;
}

.size-inputs span {
  color: #888;
  font-size: 12px;
}

.card-footer {
  padding: 8px 16px;
  background: #252525;
  border-top: 1px solid #3a3a3a;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  color: #888;
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}

.btn-icon:hover {
  background: #3a3a3a;
  color: #fff;
}

/* 全局规则区域 */
.global-rules-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.global-rules-section h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0 0 16px 0;
}

.rules-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.rule-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rule-item label {
  font-size: 12px;
  color: #888;
}

.rule-item.full-width {
  grid-column: span 2;
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
  font-size: 13px;
}

.number-input span {
  color: #888;
  font-size: 12px;
  min-width: 40px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #e0e0e0;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.inline-input {
  width: 60px;
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  padding: 4px;
  border-radius: 4px;
  font-size: 12px;
  text-align: center;
}

/* 检测区域 */
.region-section {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #3a3a3a;
  margin-bottom: 24px;
}

.region-section h3 {
  font-size: 18px;
  color: #e0e0e0;
  margin: 0 0 16px 0;
}

.region-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.region-item {
  background: #1e1e1e;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #3a3a3a;
}

.region-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.region-name {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
}

.region-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.switch.small {
  width: 36px;
  height: 18px;
}

.switch.small .slider:before {
  height: 14px;
  width: 14px;
}

.switch.small input:checked + .slider:before {
  transform: translateX(18px);
}

.btn-icon.small {
  font-size: 12px;
}

.region-defects {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
}

.defect-tag {
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  color: #fff;
}

.region-preview {
  aspect-ratio: 4/3;
  background: #2a2a2a;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.preview-box {
  position: absolute;
  border: 2px solid #00bcd4;
  background: rgba(0, 188, 212, 0.1);
}

.preview-label {
  position: absolute;
  top: -20px;
  left: 0;
  background: #00bcd4;
  color: #fff;
  padding: 2px 4px;
  font-size: 10px;
  border-radius: 2px;
}

.mt-2 {
  margin-top: 8px;
}

/* 底部操作栏 */
.action-bar {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 16px 20px;
  border: 1px solid #3a3a3a;
  display: flex;
  justify-content: flex-end;
  position: sticky;
  bottom: 0;
  backdrop-filter: blur(8px);
  background: rgba(42, 42, 42, 0.95);
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
  .defect-types-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1200px) {
  .defect-types-grid {
    grid-template-columns: 1fr;
  }
  
  .region-list {
    grid-template-columns: 1fr;
  }
  
  .rules-grid {
    grid-template-columns: 1fr;
  }
  
  .rule-item.full-width {
    grid-column: span 1;
  }
}
</style>