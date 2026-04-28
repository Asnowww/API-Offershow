<template>
  <div class="page">
    <PageHeader title="OfferShow 社招薪资查询" />
    <div class="search">
      <van-search v-model="q" placeholder="搜索公司 / 城市 / 岗位" shape="round" background="transparent" @search="reload" />
    </div>
    <div class="banner-card">
      <div>📲 扫码加入 OfferShow 大厂社招群</div>
      <div class="sub">跳槽机会 · 职场经验 · 行业动态 · 大厂新闻</div>
    </div>
    <div class="filter-bar">
      <select v-model="industry" @change="reload">
        <option value="">行业 ▾</option>
        <option v-for="i in industries" :key="i.code" :value="i.code">{{ i.name }}</option>
      </select>
      <select v-model="education" @change="reload">
        <option value="">学历 ▾</option>
        <option>本科</option><option>硕士</option><option>博士</option>
      </select>
    </div>
    <SalaryCard v-for="r in items" :key="r.id" :item="r" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { salaryApi } from '@/api'
import { industries } from '@/api/mockData'
import SalaryCard from '@/components/SalaryCard.vue'
import PageHeader from '@/components/PageHeader.vue'

const q = ref('')
const industry = ref('')
const education = ref('')
const items = ref([])
async function reload() {
  const d = await salaryApi.list({ recruitment_type: 'social', q: q.value, industry: industry.value, education: education.value, page: 1, page_size: 30 })
  items.value = d.items
}
reload()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 16px; }
.search { background: linear-gradient(180deg, #1E6EFF, #4D8FFF); padding: 6px 0 12px; }
.banner-card {
  margin: 12px; padding: 14px; background: #fff; border-radius: 12px;
  font-size: 13px; font-weight: 600;
  .sub { font-size: 11px; color: var(--os-text-3); margin-top: 4px; font-weight: 400; }
}
.filter-bar { display: flex; gap: 10px; padding: 0 12px 12px;
  select { flex: 1; height: 34px; border: 1px solid var(--os-border); border-radius: 17px; padding: 0 12px; background: #fff; font-size: 13px; }
}
</style>
