<template>
  <div class="page">
    <PageHeader title="薪资人气榜单" />
    <div class="hero">
      <div class="big">薪资人气榜</div>
      <div class="stats">累计 205,260 人次浏览 · 数据来自社区匿名爆料</div>
    </div>
    <van-tabs v-model:active="period" line-width="20px" color="#1E6EFF" @change="reload">
      <van-tab title="周榜" name="week" />
      <van-tab title="月榜" name="month" />
    </van-tabs>
    <div class="list">
      <div v-for="(r, i) in items" :key="r.id" class="row">
        <div class="rank" :class="rankClass(i+1)">No.{{ i+1 }}</div>
        <CompanyLogo :text="r.company.logo_text" :color="r.company.logo_color" :size="38" />
        <div class="col">
          <div class="cn">{{ r.company.name }} · {{ r.position }}</div>
          <div class="meta">{{ r.city }} · {{ r.education }}</div>
        </div>
        <div class="right">
          <div class="salary">{{ r.salary_desc }}</div>
          <div class="hot">🔥 {{ r.views }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { salaryApi } from '@/api'
import CompanyLogo from '@/components/CompanyLogo.vue'
import PageHeader from '@/components/PageHeader.vue'

const period = ref('week')
const items = ref([])
async function reload() {
  const data = await salaryApi.rank({ period: period.value, page: 1, page_size: 30 })
  items.value = data.items
}
function rankClass(r) { return r === 1 ? 'g' : r === 2 ? 's' : r === 3 ? 'b' : '' }
reload()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.hero { background: linear-gradient(180deg, #1E6EFF, #4D8FFF); color: #fff; padding: 16px; text-align: center; }
.big { font-size: 22px; font-weight: 800; }
.stats { font-size: 12px; opacity: .9; margin-top: 4px; }
.list { padding: 0 12px; }
.row {
  display: flex; align-items: center; gap: 12px; padding: 12px 0;
  border-bottom: 1px solid var(--os-border);
  .rank { width: 44px; font-weight: 700; color: var(--os-text-3); font-size: 13px;
    &.g { color: #E1A100; } &.s { color: #6B7780; } &.b { color: #B66B2B; }
  }
  .col { flex: 1; min-width: 0; }
  .cn { font-size: 14px; font-weight: 600; }
  .meta { font-size: 11px; color: var(--os-text-3); margin-top: 4px; }
  .right { text-align: right; }
  .salary { color: var(--os-orange); font-weight: 800; font-size: 14px; }
  .hot { font-size: 11px; color: var(--os-text-3); margin-top: 2px; }
}
</style>
