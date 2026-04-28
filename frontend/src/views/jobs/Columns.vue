<template>
  <div class="page">
    <PageHeader title="求职专栏" />
    <div class="grid">
      <div v-for="c in items" :key="c.id" class="col-card" @click="$router.push(`/columns/${c.id}`)">
        <div class="cover" :style="{ background: c.cover_color }">
          <span>{{ c.name }}</span>
        </div>
        <div class="meta">
          <span>{{ c.total }} 家正在招聘</span>
          <span class="dot">·</span>
          <span>{{ c.views }} 人次浏览</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { columnApi } from '@/api'
import PageHeader from '@/components/PageHeader.vue'

const items = ref([])
async function load() {
  const data = await columnApi.list({ scope: 'job', page: 1, page_size: 30 })
  items.value = data.items
}
load()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 12px; }
.col-card {
  background: #fff; border-radius: 12px; padding: 10px;
  .cover {
    border-radius: 10px; height: 80px; display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 14px; font-weight: 700; padding: 0 8px; text-align: center;
  }
  .meta { font-size: 11px; color: var(--os-text-3); margin-top: 6px; display: flex; gap: 4px; }
  .dot { opacity: .5; }
}
</style>
