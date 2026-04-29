<template>
  <div class="page">
    <PageHeader title="OfferShow 社招计划合集" />
    <div class="banner">📌 仅展示社会招聘机会，跳槽必看</div>
    <JobCard v-for="j in items" :key="j.id" :job="j" />
    <PaginationBar :page="page" :pages="pages" @change="load" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { jobApi } from '@/api'
import JobCard from '@/components/JobCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const items = ref([])
const page = ref(1)
const pages = ref(1)
async function load(nextPage = 1) {
  page.value = nextPage
  const data = await jobApi.list({ recruitment_type: 'social', page: page.value, page_size: 5 })
  items.value = data.items
  pages.value = data.pages || 1
}
load()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.banner {
  background: linear-gradient(90deg, #E3EEFF, #EAF2FF);
  color: var(--os-primary); padding: 10px 14px; font-size: 12px; margin: 8px 12px; border-radius: 8px;
}
</style>
