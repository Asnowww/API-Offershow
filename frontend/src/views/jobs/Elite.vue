<template>
  <div class="page">
    <PageHeader title="顶尖人才计划" />
    <div class="hero">
      <div class="big">顶尖人才计划</div>
      <div class="stats">27 个超高薪机会 · 123,595 人次浏览</div>
      <div class="tabs">
        <span class="t active">超高薪机会</span>
        <span class="t">高薪数据分享</span>
      </div>
    </div>
    <div class="card" v-for="e in items" :key="e.id">
      <div class="head">
        <CompanyLogo :text="e.company.logo_text" :color="e.company.logo_color" :size="40" />
        <div class="col">
          <div class="name">{{ e.name }}</div>
          <div class="company">{{ e.company.name }}</div>
        </div>
        <div class="salary">{{ e.salary_range }}</div>
      </div>
      <div class="desc">{{ e.description }}</div>
      <van-button block size="small" round type="primary" @click="open(e.apply_url)">查看详情</van-button>
    </div>
    <PaginationBar :page="page" :pages="pages" @change="load" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { eliteApi } from '@/api'
import CompanyLogo from '@/components/CompanyLogo.vue'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const items = ref([])
const page = ref(1)
const pages = ref(1)
async function load(nextPage = 1) {
  page.value = nextPage
  const data = await eliteApi.list({ page: page.value, page_size: 2 })
  items.value = data.items
  pages.value = data.pages || 1
}
function open(url) { window.open(url, '_blank') }
load()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.hero {
  background: linear-gradient(180deg, #1E2A78, #3858E9); color: #fff; padding: 18px 14px;
  .big { font-size: 22px; font-weight: 800; }
  .stats { font-size: 12px; margin-top: 4px; opacity: .9; }
  .tabs { margin-top: 12px; display: flex; gap: 16px; font-size: 13px; opacity: .8;
    .t.active { opacity: 1; font-weight: 700; }
  }
}
.card {
  background: #fff; border-radius: 12px; margin: 10px 12px; padding: 14px;
  .head { display: flex; gap: 10px; align-items: center; }
  .col { flex: 1; }
  .name { font-size: 15px; font-weight: 700; }
  .company { font-size: 12px; color: var(--os-text-3); margin-top: 2px; }
  .salary { color: var(--os-orange); font-weight: 700; font-size: 14px; }
  .desc { font-size: 13px; color: var(--os-text-2); margin: 10px 0; line-height: 1.6; }
}
</style>
