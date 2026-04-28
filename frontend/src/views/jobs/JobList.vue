<template>
  <div class="page">
    <!-- 顶部蓝色区 -->
    <div class="top-bg">
      <div class="top-tabs">
        <span class="tab active">找名企</span>
        <span class="tab">榜单求职</span>
        <span class="tab">品牌馆</span>
      </div>
      <div class="search-bar" @click="onSearch">
        <van-icon name="search" />
        <span class="ph">校招信息持续更新中…</span>
      </div>

      <!-- 大入口卡 -->
      <div class="big-cards">
        <div class="big-card" style="background:#FFE2D2;color:#FF6B2B" @click="$router.push('/daily-brief')">
          <div class="bc-title">求职早报</div>
          <div class="bc-sub">今日新增12家招聘</div>
        </div>
        <div class="big-card" style="background:#FFE7AB;color:#C77E00" @click="$router.push('/courses')">
          <div class="bc-title">求职好课</div>
          <div class="bc-sub">高口碑/1V1私教</div>
        </div>
      </div>

      <!-- 九宫格入口 -->
      <div class="grid">
        <div class="g" @click="$router.push('/columns')">
          <div class="g-title">求职专栏</div><div class="g-sub">春招外企国企</div>
        </div>
        <div class="g" @click="goRank">
          <div class="g-title">招聘人气榜</div><div class="g-sub">大家都在投</div>
        </div>
        <div class="g" @click="$router.push('/refer')">
          <div class="g-title">内推专区</div><div class="g-sub">TOP名企</div>
        </div>
        <div class="g" @click="$router.push('/review-rank')">
          <div class="g-title">实习点评</div><div class="g-sub">真实企业点评</div>
        </div>
        <div class="g" @click="$router.push('/elite')">
          <div class="g-title">顶尖人才</div><div class="g-sub">行业TOP薪酬</div>
        </div>
        <div class="g" @click="$router.push('/social')">
          <div class="g-title">社招专区</div><div class="g-sub">社招跳槽机会</div>
        </div>
      </div>
    </div>

    <!-- 行业横滑 -->
    <div class="ind-bar">
      <div
        v-for="i in industries"
        :key="i.code"
        :class="['ind', { active: i.code === filter.industry }]"
        @click="filter.industry = i.code; reload()"
      >{{ i.name }}</div>
    </div>

    <!-- 排序 / 二级筛选 -->
    <div class="sort-bar">
      <span :class="{active: filter.sort==='latest'}" @click="filter.sort='latest'; reload()">最新</span>
      <span :class="{active: filter.sort==='hot'}" @click="filter.sort='hot'; reload()">热门</span>
      <span :class="{active: filter.sort==='deadline'}" @click="filter.sort='deadline'; reload()">即将截止</span>
      <span class="grow"></span>
      <span class="filter-btn" @click="showCity = true">
        城市<van-icon name="arrow-down" />
      </span>
      <span class="filter-btn" @click="showMore = true">
        筛选<van-icon name="filter-o" />
      </span>
    </div>

    <!-- 会员引导 -->
    <div class="member-banner">
      <span>🔓 开通会员，{{ totalCount }} 条最新招聘提前看</span>
    </div>

    <!-- 招聘列表 -->
    <van-pull-refresh v-model="refreshing" @refresh="reload">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="loadMore"
      >
        <JobCard v-for="j in items" :key="j.id" :job="j" />
      </van-list>
    </van-pull-refresh>

    <!-- 城市选择弹层 -->
    <van-popup v-model:show="showCity" position="bottom" round :style="{ height: '60%' }">
      <div class="popup">
        <div class="ph-title">意向城市</div>
        <div class="city-grid">
          <div
            v-for="c in cityList"
            :key="c"
            :class="['city-chip', { active: filter.cities.includes(c) }]"
            @click="toggleCity(c)"
          >{{ c }}</div>
        </div>
        <div class="popup-foot">
          <van-button block plain @click="filter.cities = []">重置</van-button>
          <van-button block type="primary" @click="showCity=false; reload()">确定</van-button>
        </div>
      </div>
    </van-popup>

    <!-- 更多筛选弹层 -->
    <van-popup v-model:show="showMore" position="bottom" round :style="{ height: '70%' }">
      <div class="popup">
        <div class="ph-title">所在行业</div>
        <div class="city-grid">
          <div
            v-for="i in industries"
            :key="i.code"
            :class="['city-chip', { active: filter.industry === i.code }]"
            @click="filter.industry = i.code"
          >{{ i.name }}</div>
        </div>
        <div class="ph-title">招聘类型</div>
        <div class="city-grid">
          <div
            v-for="b in batches"
            :key="b"
            :class="['city-chip', { active: filter.batch === b }]"
            @click="filter.batch = b"
          >{{ b }}</div>
        </div>
        <div class="popup-foot">
          <van-button block plain @click="resetMore">重置</van-button>
          <van-button block type="primary" @click="showMore=false; reload()">确定</van-button>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { jobApi } from '@/api'
import { industries, cities as cityList, batches } from '@/api/mockData'
import JobCard from '@/components/JobCard.vue'
import { showToast } from 'vant'

const router = useRouter()
const filter = reactive({ industry: 'all', cities: [], batch: '不限', sort: 'latest', q: '' })
const items = ref([])
const page = ref(0)
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const totalCount = ref(0)
const showCity = ref(false)
const showMore = ref(false)

async function reload() {
  page.value = 0
  finished.value = false
  items.value = []
  await loadMore()
  refreshing.value = false
}

async function loadMore() {
  page.value += 1
  const data = await jobApi.list({ ...filter, page: page.value, page_size: 10 })
  items.value.push(...data.items)
  totalCount.value = data.total
  loading.value = false
  if (!data.has_more) finished.value = true
}

function onSearch() {
  router.push({ name: 'jobs', query: { search: 1 } })
  showToast('搜索：试试输入"字节跳动"')
}
function goRank() { showToast('招聘人气榜：开发演示版') }
function toggleCity(c) {
  const i = filter.cities.indexOf(c)
  if (i >= 0) filter.cities.splice(i, 1)
  else filter.cities.push(c)
}
function resetMore() { filter.industry = 'all'; filter.batch = '不限' }

reload()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.top-bg {
  background: linear-gradient(180deg, #2D7BFF 0%, #4D8FFF 100%);
  padding: 12px 12px 16px;
  color: #fff;
}
.top-tabs {
  display: flex; gap: 18px; padding: 4px 4px 12px;
  font-size: 16px; color: rgba(255,255,255,.7);
  .tab.active { color: #fff; font-weight: 700; font-size: 18px; }
}
.search-bar {
  background: rgba(255,255,255,.85); border-radius: 22px;
  height: 36px; padding: 0 14px; display: flex; align-items: center; gap: 6px;
  color: var(--os-text-3); font-size: 13px;
  .ph { color: var(--os-text-3); }
}
.big-cards {
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px;
  .big-card {
    border-radius: 12px; padding: 12px 14px;
    .bc-title { font-size: 16px; font-weight: 700; }
    .bc-sub { font-size: 11px; margin-top: 4px; opacity: .85; }
  }
}
.grid {
  margin-top: 10px; background: #fff; border-radius: 12px; padding: 12px 6px;
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px 0;
  .g {
    text-align: center; padding: 8px 4px;
    .g-title { font-size: 13px; font-weight: 600; color: var(--os-text); }
    .g-sub { font-size: 10px; color: var(--os-text-3); margin-top: 2px; }
  }
}
.ind-bar {
  display: flex; gap: 14px; padding: 10px 12px;
  background: #fff; overflow-x: auto; white-space: nowrap;
  .ind {
    font-size: 13px; color: var(--os-text-2);
    padding: 4px 0; flex-shrink: 0;
    &.active { color: var(--os-primary); font-weight: 700; position: relative;
      &::after { content:''; position:absolute; left: 50%; transform: translateX(-50%); bottom: 0; width: 16px; height: 2px; background: var(--os-primary); border-radius: 2px; }
    }
  }
}
.sort-bar {
  display: flex; align-items: center; gap: 14px;
  background: #fff; padding: 8px 12px; border-top: 1px solid #f4f4f4;
  font-size: 13px; color: var(--os-text-2);
  span.active { color: var(--os-text); font-weight: 700; }
  .grow { flex: 1; }
  .filter-btn { display: inline-flex; align-items: center; gap: 2px; }
}
.member-banner {
  background: #FFF5E6; color: #C77E00; font-size: 12px;
  padding: 6px 12px; border-bottom: 1px solid #fff;
}
.popup { padding: 16px; }
.ph-title { font-weight: 700; margin-bottom: 8px; }
.city-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px; }
.city-chip {
  background: #F4F6F9; color: var(--os-text-2);
  border-radius: 6px; padding: 8px 0; text-align: center; font-size: 13px;
  &.active { background: #E3EEFF; color: var(--os-primary); }
}
.popup-foot { display: flex; gap: 10px; padding-top: 6px; }
</style>
