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
    <PaginationBar :page="page" :pages="pages" @change="loadItems" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { columnApi } from '@/api'
import JobCard from '@/components/JobCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const route = useRoute()
const col = ref(null)
const items = ref([])
const page = ref(1)
const pages = ref(0)
async function loadItems(nextPage = 1) {
  page.value = nextPage
  const data = await columnApi.items(route.params.id, { page: page.value, page_size: 5 })
  items.value = data.items
  pages.value = data.pages
}
async function load() {
  col.value = await columnApi.get(route.params.id)
  await loadItems(1)
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
