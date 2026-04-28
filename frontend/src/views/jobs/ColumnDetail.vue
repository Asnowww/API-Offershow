<template>
  <div class="page" v-if="col">
    <PageHeader :title="col.name" />
    <div class="hero" :style="{ background: col.cover_color }">
      <div class="title">{{ col.name }}</div>
      <div class="stats">
        <span>{{ col.total }} 家正在招聘</span>
        <span class="dot">·</span>
        <span>{{ col.views }} 人次浏览</span>
      </div>
    </div>
    <JobCard v-for="j in items" :key="j.id" :job="j" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { columnApi } from '@/api'
import JobCard from '@/components/JobCard.vue'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const col = ref(null)
const items = ref([])
async function load() {
  col.value = await columnApi.get(route.params.id)
  const data = await columnApi.items(route.params.id, { page: 1, page_size: 30 })
  items.value = data.items
}
load()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.hero { color: #fff; padding: 24px 16px; }
.title { font-size: 20px; font-weight: 800; }
.stats { font-size: 12px; margin-top: 6px; opacity: .9; display: flex; gap: 6px; }
.dot { opacity: .6; }
</style>
