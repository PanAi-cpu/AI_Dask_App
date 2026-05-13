<!-- src/App.vue -->
<template>
  <MainLayout />
</template>

<script setup>
import MainLayout from './components/layout/MainLayout.vue'
</script>
<style scoped>
/* 全局深色滚动条 */
*::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

*::-webkit-scrollbar-track {
  background: #2a2a2a;
}

*::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

*::-webkit-scrollbar-thumb:hover {
  background: #777;
}

/* Firefox */
* {
  scrollbar-width: thin;
  scrollbar-color: #555 #2a2a2a;
}
</style>