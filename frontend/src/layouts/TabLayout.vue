<template>
  <div class="tab-layout">
    <router-view />
    <van-tabbar v-model="active" route active-color="#1E6EFF" inactive-color="#999">
      <van-tabbar-item replace to="/jobs" icon="bag-o">找名企</van-tabbar-item>
      <van-tabbar-item replace to="/salary" icon="balance-o">查薪资</van-tabbar-item>
      <van-tabbar-item replace to="/me" icon="user-o">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const active = ref(0)
</script>

<style scoped>
.tab-layout { padding-bottom: 50px; min-height: 100vh; background: var(--os-bg); }
</style>
