<template>
  <div class="page">
    <PageHeader title="薪资最新动态" />
    <SalaryCard v-for="r in items" :key="r.id" :item="r" />
    <PaginationBar :page="page" :pages="pages" @change="reload" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { salaryApi } from '@/api'
import SalaryCard from '@/components/SalaryCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const items = ref([])
const page = ref(1)
const pages = ref(0)
async function reload(nextPage = 1) {
  page.value = nextPage
  const d = await salaryApi.list({ page: page.value, page_size: 5 })
  items.value = d.items
  pages.value = d.pages
}
reload(1)
</script>

<style scoped>
.page { background: var(--os-bg); min-height: 100vh; }
</style>
