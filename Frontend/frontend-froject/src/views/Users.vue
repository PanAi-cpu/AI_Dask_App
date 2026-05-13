<!-- src/views/Users.vue -->
<!-- 用户管理 - 账号切换 -->
<template>
  <div class="users">
    <!-- 标题 -->
    <div class="title-bar">
      <h2>用户管理</h2>
    </div>

    <!-- 当前用户 -->
    <div class="current-user">
      <div class="user-info">
        <span class="user-avatar">张</span>
        <div>
          <div class="user-name">张伟</div>
          <div class="user-role">工程师 · 已登录</div>
        </div>
      </div>
      <button class="btn">切换账号</button>
    </div>

    <!-- 用户列表 -->
    <div class="card">
      <div class="card-header">
        <h3>账号列表</h3>
        <button class="btn" @click="showNewUserModal = true">
          <span class="btn-icon">+</span>新建
        </button>
      </div>

      <!-- 搜索 -->
      <div class="search-box">
        <input type="text" v-model="userSearch" placeholder="搜索用户名或姓名...">
      </div>

      <!-- 用户列表 -->
      <div class="user-list">
        <div v-for="user in filteredUsers" :key="user.id" class="user-item">
          <div class="user-item-info">
            <span class="user-avatar" :style="{ background: user.avatarColor }">{{ user.name.charAt(0) }}</span>
            <div>
              <div class="user-item-name">{{ user.name }}</div>
              <div class="user-item-detail">
                <span class="user-username">{{ user.username }}</span>
                <span class="badge" :class="`role-${user.role}`">{{ user.role === 'engineer' ? '工程师' : '操作员' }}</span>
                <span class="badge" :class="user.status === 'active' ? 'status-active' : 'status-inactive'">
                  {{ user.status === 'active' ? '激活' : '禁用' }}
                </span>
              </div>
            </div>
          </div>
          <div class="user-item-actions">
            <button class="icon-btn" @click="editUser(user)" title="编辑">✎</button>
            <button class="icon-btn" @click="toggleUserStatus(user)" :title="user.status === 'active' ? '禁用' : '启用'">
              {{ user.status === 'active' ? '🔒' : '🔓' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近登录 -->
    <div class="card">
      <h3>最近登录</h3>
      <div class="login-list">
        <div v-for="(log, index) in recentLogs" :key="index" class="login-item">
          <span class="login-time">{{ log.time }}</span>
          <span class="login-user">{{ log.user }}</span>
          <span class="login-ip">{{ log.ip }}</span>
        </div>
      </div>
    </div>

    <!-- 新建用户 -->
    <div v-if="showNewUserModal" class="modal" @click.self="showNewUserModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>新建账号</h3>
          <button class="close-btn" @click="showNewUserModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <label>用户名</label>
            <input type="text" v-model="newUser.username" placeholder="登录账号">
          </div>
          <div class="form-row">
            <label>姓名</label>
            <input type="text" v-model="newUser.name" placeholder="显示名称">
          </div>
          <div class="form-row">
            <label>密码</label>
            <input type="password" v-model="newUser.password" placeholder="初始密码">
          </div>
          <div class="form-row">
            <label>角色</label>
            <select v-model="newUser.role">
              <option value="engineer">工程师</option>
              <option value="operator">操作员</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn" @click="showNewUserModal = false">取消</button>
          <button class="btn primary" @click="createUser">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 用户数据 - 只保留工程师和操作员
const users = ref([
  { id: 2, username: 'zhang.wei', name: '张伟', role: 'engineer', status: 'active', avatarColor: '#2196f3', lastLogin: '08:45' },
  { id: 3, username: 'li.na', name: '李娜', role: 'operator', status: 'active', avatarColor: '#4caf50', lastLogin: '08:30' },
  { id: 4, username: 'wang.fang', name: '王芳', role: 'operator', status: 'inactive', avatarColor: '#ff9800', lastLogin: '昨天' },
  { id: 5, username: 'chen.qiang', name: '陈强', role: 'engineer', status: 'active', avatarColor: '#9c27b0', lastLogin: '14:15' },
  { id: 6, username: 'zhao.li', name: '赵丽', role: 'operator', status: 'active', avatarColor: '#00bcd4', lastLogin: '09:10' }
])

// 搜索
const userSearch = ref('')
const showNewUserModal = ref(false)
const newUser = ref({
  username: '',
  name: '',
  password: '',
  role: 'operator'  // 默认操作员
})

// 过滤用户
const filteredUsers = computed(() => {
  if (!userSearch.value) return users.value
  const query = userSearch.value.toLowerCase()
  return users.value.filter(u => 
    u.username.toLowerCase().includes(query) ||
    u.name.toLowerCase().includes(query)
  )
})

// 最近登录
const recentLogs = ref([
  { time: '08:45', user: '张伟', ip: '192.168.1.105' },
  { time: '08:30', user: '李娜', ip: '192.168.1.110' },
  { time: '09:10', user: '赵丽', ip: '192.168.1.120' },
  { time: '昨天', user: '陈强', ip: '192.168.1.108' }
])

// 操作
const editUser = (user) => {
  alert(`编辑: ${user.name}`)
}

const toggleUserStatus = (user) => {
  user.status = user.status === 'active' ? 'inactive' : 'active'
}

const createUser = () => {
  alert('账号已创建')
  showNewUserModal.value = false
  newUser.value = { username: '', name: '', password: '', role: 'operator' }
}
</script>

<style scoped>
.users {
  height: 100%;
  overflow-y: auto;
  padding: 16px;
  background: #1e1e1e;
}

/* 标题 */
.title-bar {
  margin-bottom: 20px;
  border-bottom: 1px solid #333;
  padding-bottom: 8px;
}

.title-bar h2 {
  font-size: 18px;
  font-weight: 400;
  color: #e0e0e0;
  margin: 0;
}

/* 当前用户 */
.current-user {
  background: #252525;
  border: 1px solid #333;
  padding: 12px;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #fff;
  border: 1px solid #444;
}

.user-name {
  font-size: 14px;
  color: #e0e0e0;
  margin-bottom: 4px;
}

.user-role {
  font-size: 11px;
  color: #888;
}

/* 卡片 */
.card {
  background: #252525;
  border: 1px solid #333;
  padding: 12px;
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card h3 {
  font-size: 14px;
  font-weight: 400;
  color: #ccc;
  margin: 0;
}

/* 搜索框 */
.search-box {
  margin-bottom: 12px;
}

.search-box input {
  width: 100%;
  background: #1e1e1e;
  border: 1px solid #333;
  color: #e0e0e0;
  padding: 8px;
  font-size: 12px;
  outline: none;
}

.search-box input:focus {
  border-color: #444;
}

/* 用户列表 */
.user-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-item {
  background: #1e1e1e;
  border: 1px solid #333;
  padding: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-item-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-item-name {
  font-size: 13px;
  color: #e0e0e0;
  margin-bottom: 4px;
}

.user-item-detail {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
}

.user-username {
  color: #888;
}

/* 徽章 */
.badge {
  display: inline-block;
  padding: 2px 6px;
  font-size: 10px;
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #ccc;
}

.role-engineer {
  background: #0a2a44;
  border-color: #154979;
  color: #bbdefb;
}

.role-operator {
  background: #1a472a;
  border-color: #2d6a4f;
  color: #c8e6c9;
}

.status-active {
  background: #1a472a;
  border-color: #2d6a4f;
  color: #c8e6c9;
}

.status-inactive {
  background: #5f0f0f;
  border-color: #8b1a1a;
  color: #ffcdd2;
}

/* 按钮 */
.btn {
  background: #333;
  border: 1px solid #444;
  color: #ccc;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.btn:hover {
  background: #3a3a3a;
  border-color: #555;
  color: #fff;
}

.btn.primary {
  background: #005f73;
  border-color: #0a7a8c;
  color: #fff;
}

.btn-icon {
  font-size: 14px;
}

.icon-btn {
  background: none;
  border: 1px solid #333;
  color: #888;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 12px;
}

.icon-btn:hover {
  background: #333;
  border-color: #444;
  color: #fff;
}

.user-item-actions {
  display: flex;
  gap: 4px;
}

/* 最近登录 */
.login-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.login-item {
  display: flex;
  gap: 12px;
  font-size: 12px;
  padding: 6px 0;
  border-bottom: 1px solid #2a2a2a;
}

.login-item:last-child {
  border-bottom: none;
}

.login-time {
  color: #888;
  min-width: 45px;
}

.login-user {
  color: #e0e0e0;
  min-width: 80px;
}

.login-ip {
  color: #666;
  font-family: monospace;
}

/* 模态框 */
.modal {
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
}

.modal-content {
  width: 350px;
  background: #252525;
  border: 2px solid #333;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #1e1e1e;
  border-bottom: 1px solid #333;
}

.modal-header h3 {
  font-size: 14px;
  font-weight: 400;
  color: #ccc;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 16px;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #fff;
}

.modal-body {
  padding: 12px;
}

.form-row {
  margin-bottom: 10px;
}

.form-row label {
  display: block;
  font-size: 11px;
  color: #888;
  margin-bottom: 4px;
}

.form-row input,
.form-row select {
  width: 100%;
  background: #1e1e1e;
  border: 1px solid #333;
  color: #e0e0e0;
  padding: 6px;
  font-size: 12px;
  outline: none;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 10px 12px;
  background: #1e1e1e;
  border-top: 1px solid #333;
}

/* 滚动条 */
.users::-webkit-scrollbar {
  width: 8px;
}

.users::-webkit-scrollbar-track {
  background: #1e1e1e;
}

.users::-webkit-scrollbar-thumb {
  background: #333;
  border: 1px solid #444;
}
</style>