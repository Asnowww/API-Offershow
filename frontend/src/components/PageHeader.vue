<template>
  <van-nav-bar
    :title="title"
    :left-arrow="back"
    @click-left="$router.back()"
    safe-area-inset-top
    :border="false"
    :style="{ background: bg, color: '#fff' }"
  >
    <template #title><span :style="{ color: '#fff' }">{{ title }}</span></template>
    <template v-if="back" #left>
      <van-icon name="arrow-left" color="#fff" size="20" />
    </template>
    <template v-if="$slots.right" #right><slot name="right" /></template>
  </van-nav-bar>
</template>

<script setup>
defineProps({
  title: String,
  back: { type: Boolean, default: true },
  bg: { type: String, default: '#1E6EFF' },
})
</script>

<style scoped>
:deep(.van-nav-bar__title) { color: #fff !important; font-weight: 600; }
:deep(.van-nav-bar) { background: v-bind(bg); }
</style>
