<template>
  <div class="page">
    <PageHeader title="校招薪资查询" />
    <div class="search">
      <van-search v-model="q" placeholder="请输入公司名称查询" shape="round" background="transparent" @search="reload" />
    </div>
    <div class="banners">
      <div class="banner b1">985/211 党专场<div class="sub">高校学生绝佳机会</div></div>
      <div class="banner b2">爆料合集<div class="sub">每周热门薪资</div></div>
    </div>
    <div class="grid">
      <div v-for="c in cols" :key="c.id" class="col" :style="{ background: c.cover_color }" @click="$router.push(`/salary/columns/${c.id}`)">{{ c.name }}</div>
    </div>
    <div class="section-h">相关爆料</div>
    <SalaryCard v-for="r in items" :key="r.id" :item="r" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { salaryApi, columnApi } from '@/api'
import SalaryCard from '@/components/SalaryCard.vue'
import PageHeader from '@/components/PageHeader.vue'

const q = ref('')
const items = ref([])
const cols = ref([])
async function reload() {
  const d = await salaryApi.list({ recruitment_type: 'campus', q: q.value, page: 1, page_size: 30 })
  items.value = d.items
}
columnApi.list({ scope: 'salary' }).then(d => cols.value = d.items)
reload()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 16px; }
.search { background: linear-gradient(180deg, #1E6EFF, #4D8FFF); padding: 6px 0 12px; }
.banners { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 12px; }
.banner {
  border-radius: 12px; padding: 16px; color: #fff; font-size: 16px; font-weight: 700;
  .sub { font-size: 11px; font-weight: 400; opacity: .9; margin-top: 4px; }
  &.b1 { background: linear-gradient(135deg, #FF8B3D, #FFB46B); }
  &.b2 { background: linear-gradient(135deg, #1E6EFF, #4D8FFF); }
}
.grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; padding: 0 12px 12px;
  .col {
    color: #fff; font-weight: 700; padding: 16px 12px; border-radius: 10px;
  }
}
.section-h { padding: 14px 14px 6px; font-size: 15px; font-weight: 700; }
</style>
