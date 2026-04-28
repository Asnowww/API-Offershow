<template>
  <div class="page">
    <PageHeader title="薪资最新动态" />
    <SalaryCard v-for="r in items" :key="r.id" :item="r" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { salaryApi } from '@/api'
import SalaryCard from '@/components/SalaryCard.vue'
import PageHeader from '@/components/PageHeader.vue'

const items = ref([])
salaryApi.list({ page: 1, page_size: 30 }).then(d => items.value = d.items)
</script>

<style scoped>
.page { background: var(--os-bg); min-height: 100vh; }
</style>
