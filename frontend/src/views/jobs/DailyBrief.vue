<template>
  <div class="page">
    <PageHeader title="求职早报" />
    <div class="hero">
      <div class="hero-title">OfferShow</div>
      <div class="hero-big">求职早报</div>
      <div class="hero-sub">订阅早报，获取当日最新招聘信息</div>
      <van-button class="sub-btn" round type="default" @click="subscribe">
        <van-icon name="bell" /> {{ subscribed ? '已订阅' : '订阅' }}
      </van-button>
    </div>

    <div class="weekbar">
      <div
        v-for="d in week"
        :key="d.date"
        :class="['day', { active: d.active }]"
        @click="active = d.date"
      >
        <span class="dn">{{ d.label }}</span>
        <span class="dd">{{ d.day }}</span>
      </div>
    </div>

    <div class="join-group">
      <span>💬 加入群聊，接收最新招聘推送</span>
      <van-button size="small" round type="primary">立即进群</van-button>
    </div>

    <div class="section-h">24h 新招（{{ total }}）</div>
    <JobCard v-for="j in items" :key="j.id" :job="j" />
    <PaginationBar :page="page" :pages="pages" @change="load" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { showToast } from 'vant'
import { dailyBriefApi } from '@/api'
import JobCard from '@/components/JobCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const items = ref([])
const total = ref(0)
const page = ref(1)
const pages = ref(0)
const subscribed = ref(false)
const active = ref('today')

const week = computed(() => {
  const labels = ['周二','周三','周四','周五','周六','周日','周一']
  const days = ['21','22','23','24','25','26','今天']
  return labels.map((l, i) => ({ label: l, day: days[i], date: i, active: days[i] === '今天' }))
})

async function subscribe() {
  subscribed.value = !subscribed.value
  showToast(subscribed.value ? '已订阅每日早报' : '已取消订阅')
}

async function load(nextPage = 1) {
  page.value = nextPage
  const data = await dailyBriefApi.list({ page: page.value, page_size: 5 })
  items.value = data.items
  total.value = data.total
  pages.value = data.pages
}
load(1)
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.hero {
  background: linear-gradient(180deg, #1E6EFF 0%, #4D8FFF 100%);
  color: #fff; padding: 20px 16px 24px; position: relative;
  .hero-title { font-size: 16px; font-weight: 700; }
  .hero-big { font-size: 32px; font-weight: 800; margin-top: 4px; }
  .hero-sub { font-size: 12px; margin-top: 8px; opacity: .9; padding: 6px 10px; background: rgba(255,255,255,.18); border-radius: 8px; display: inline-block; }
  .sub-btn { position: absolute; right: 16px; top: 60px; }
}
.weekbar {
  display: flex; gap: 4px; padding: 0 8px; margin-top: -16px;
  background: linear-gradient(180deg, transparent, var(--os-bg) 70%);
  .day {
    flex: 1; text-align: center; padding: 10px 0;
    background: rgba(255,255,255,.18); color: rgba(255,255,255,.85);
    border-radius: 8px; font-size: 11px;
    &.active { background: #fff; color: var(--os-primary); font-weight: 700; box-shadow: 0 4px 10px rgba(0,0,0,.05); }
    .dn { display: block; }
    .dd { font-size: 16px; font-weight: 700; display: block; margin-top: 2px; }
  }
}
.join-group {
  margin: 12px; padding: 12px 14px;
  background: #fff; border-radius: 12px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 13px;
}
.section-h { padding: 12px 14px 4px; font-weight: 700; font-size: 15px; }
</style>
