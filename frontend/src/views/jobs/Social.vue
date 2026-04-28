<template>
  <div class="page">
    <PageHeader title="OfferShow 社招计划合集" />
    <div class="banner">📌 仅展示社会招聘机会，跳槽必看</div>
    <JobCard v-for="j in items" :key="j.id" :job="j" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { jobApi } from '@/api'
import JobCard from '@/components/JobCard.vue'
import PageHeader from '@/components/PageHeader.vue'

const items = ref([])
async function load() {
  const data = await jobApi.list({ recruitment_type: 'social', page: 1, page_size: 30 })
  items.value = data.items
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
