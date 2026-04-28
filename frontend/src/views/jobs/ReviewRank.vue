<template>
  <div class="page">
    <PageHeader title="实习点评榜" />
    <div class="hero">
      <div class="hero-title">实习点评榜</div>
      <div class="hero-stats">3,304 人次打分 · 110,678 人次浏览</div>
      <van-search v-model="q" placeholder="输入你想搜索的企业名称" shape="round" background="transparent" @search="reload" />
    </div>
    <van-tabs v-model:active="tab" line-width="20px" color="#1E6EFF" @change="reload">
      <van-tab title="高分" name="high" />
      <van-tab title="低分" name="low" />
      <van-tab title="热门" name="hot" />
      <van-tab title="最新" name="new" />
    </van-tabs>
    <div class="list">
      <div v-for="r in items" :key="r.rank" class="row">
        <div class="rank" :class="rankClass(r.rank)">No.{{ r.rank }}</div>
        <CompanyLogo :text="r.company.logo_text" :color="r.company.logo_color" :size="40" />
        <div class="col">
          <div class="cn">{{ r.company.name }}</div>
          <div class="latest os-ellipsis">{{ r.latest }}</div>
        </div>
        <div class="score-col">
          <div class="score">{{ r.score }}</div>
          <div class="reviews">{{ r.reviews }} 人评分</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { reviewApi } from '@/api'
import CompanyLogo from '@/components/CompanyLogo.vue'
import PageHeader from '@/components/PageHeader.vue'

const tab = ref('high')
const q = ref('')
const items = ref([])

async function reload() {
  const data = await reviewApi.rank({ tab: tab.value, q: q.value, page: 1, page_size: 50 })
  items.value = data.items
}
function rankClass(r) { return r === 1 ? 'g' : r === 2 ? 's' : r === 3 ? 'b' : '' }
reload()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.hero { background: linear-gradient(180deg, #1E6EFF, #4D8FFF); color: #fff; padding: 16px 0 4px; text-align: center; }
.hero-title { font-size: 22px; font-weight: 800; }
.hero-stats { font-size: 12px; opacity: .9; margin-top: 4px; }
.list { padding: 0 12px; }
.row {
  display: flex; align-items: center; gap: 12px; padding: 12px 0;
  border-bottom: 1px solid var(--os-border);
  .rank { width: 44px; font-weight: 700; color: var(--os-text-3); font-size: 13px;
    &.g { color: #E1A100; } &.s { color: #6B7780; } &.b { color: #B66B2B; }
  }
  .col { flex: 1; min-width: 0; }
  .cn { font-size: 14px; font-weight: 600; }
  .latest { font-size: 11px; color: var(--os-text-3); margin-top: 4px; }
  .score-col { text-align: right; }
  .score { font-size: 18px; font-weight: 800; color: var(--os-orange); }
  .reviews { font-size: 11px; color: var(--os-text-3); }
}
</style>
