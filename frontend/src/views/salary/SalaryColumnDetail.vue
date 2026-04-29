<template>
  <div class="page" v-if="col">
    <PageHeader :title="col.name" />
    <div class="hero" :style="{ background: col.cover_color }">
      <div class="title">{{ col.name }}</div>
      <div class="desc">{{ col.desc }}</div>
      <div class="stats">{{ total }} 条爆料</div>
    </div>
    <div v-if="!items.length && !loading" class="empty">该专栏暂无数据</div>
    <SalaryCard v-for="r in items" :key="r.id" :item="r" />
    <PaginationBar :page="page" :pages="pages" @change="loadItems" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { columnApi } from '@/api'
import { salaryColumns } from '@/api/mockData'
import SalaryCard from '@/components/SalaryCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const route = useRoute()
const col = ref(null)
const items = ref([])
const total = ref(0)
const page = ref(1)
const pages = ref(0)
const loading = ref(false)

async function loadItems(nextPage = 1) {
  page.value = nextPage
  loading.value = true
  const data = await columnApi.salaryItems(route.params.id, { page: page.value, page_size: 5 })
  items.value = data.items
  total.value = data.total
  pages.value = data.pages
  loading.value = false
}

async function load() {
  col.value = salaryColumns.find(c => c.id === Number(route.params.id))
  await loadItems(1)
}
load()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 16px; }
.hero { color: #fff; padding: 22px 16px 18px; }
.title { font-size: 22px; font-weight: 800; }
.desc { font-size: 12px; opacity: .9; margin-top: 6px; }
.stats { font-size: 12px; opacity: .9; margin-top: 8px; background: rgba(255,255,255,.18); padding: 4px 10px; border-radius: 8px; display: inline-block; }
.empty { text-align: center; color: var(--os-text-3); font-size: 13px; padding: 60px 0; }
</style>
