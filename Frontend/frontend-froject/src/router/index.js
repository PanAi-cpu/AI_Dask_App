// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/parameters',
    name: 'Parameters',
    component: () => import('../views/Parameters.vue')
  },
  {
    path: '/camera',
    name: 'Camera',
    component: () => import('../views/CameraSettings.vue')
  },
  {
    path: '/defect-config',
    name: 'DefectConfig',
    component: () => import('../views/DefectConfig.vue')
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('../views/Logs.vue')
  },
  {
    path: '/templates',
    name: 'Templates',
    component: () => import('../views/Templates.vue')
  },
  {
    path: '/diagnostics',
    name: 'Diagnostics',
    component: () => import('../views/Diagnostics.vue')
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue')
  },
  {
    path: '/dashboard-large',
    name: 'DashboardLarge',
    component: () => import('../views/DashboardLarge.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router