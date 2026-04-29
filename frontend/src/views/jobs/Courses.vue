<template>
  <div class="page">
    <PageHeader title="求职好课" />
    <van-tabs v-model:active="cat" line-width="20px" color="#1E6EFF">
      <van-tab v-for="c in categories" :key="c" :title="c" :name="c" />
    </van-tabs>
    <div class="grid">
      <div v-for="c in items" :key="c.id" class="course">
        <div class="cover" :style="{ background: c.cover_color }">
          <span class="logo-text">{{ c.title.slice(0,4) }}</span>
        </div>
        <div class="title os-ellipsis-2">{{ c.title }}</div>
        <div class="intro os-ellipsis">{{ c.intro }}</div>
        <div class="price">¥{{ c.price }}</div>
      </div>
    </div>
    <PaginationBar :page="page" :pages="pages" @change="load" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { courseApi } from '@/api'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const categories = ['全部课程','求职必备','行业好课','求职陪跑']
const cat = ref('全部课程')
const items = ref([])
const page = ref(1)
const pages = ref(0)

async function load(nextPage = 1) {
  page.value = nextPage
  const data = await courseApi.list({ category: cat.value, page: page.value, page_size: 5 })
  items.value = data.items
  pages.value = data.pages
}
watch(cat, () => load(1), { immediate: true })
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 12px; }
.course {
  background: #fff; border-radius: 12px; padding: 10px;
  .cover { height: 90px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700; }
  .title { font-size: 13px; font-weight: 600; margin-top: 8px; min-height: 36px; }
  .intro { font-size: 11px; color: var(--os-text-3); margin-top: 4px; }
  .price { color: var(--os-orange); font-weight: 700; margin-top: 6px; }
}
</style>
