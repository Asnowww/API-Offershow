<template>
  <div class="page">
    <div class="top">
      <van-tabs v-model:active="rt" line-width="20px" color="#fff" title-active-color="#fff" title-inactive-color="rgba(255,255,255,.7)" background="transparent">
        <van-tab title="校招" name="campus" />
        <van-tab title="社招" name="social" />
        <van-tab title="实习" name="intern" />
      </van-tabs>
      <div class="search-bar">
        <van-icon name="search" />
        <input v-model="q" placeholder="请输入公司名 + 岗位/城市" @keyup.enter="reload" />
      </div>
      <div class="entries">
        <div class="ent" @click="$router.push('/salary/report')">
          <div class="ic">📤</div><div>薪资爆料</div>
        </div>
        <div class="ent" @click="$router.push('/salary/rank')">
          <div class="ic">🔥</div><div>薪资人气榜</div>
        </div>
        <div class="ent" @click="$router.push('/salary/campus')">
          <div class="ic">🎓</div><div>校招薪资</div>
        </div>
        <div class="ent" @click="$router.push('/salary/social')">
          <div class="ic">🧑‍💼</div><div>社招薪资</div>
        </div>
      </div>
    </div>

    <div class="section-h">薪资专栏</div>
    <div class="columns-row">
      <div v-for="c in cols" :key="c.id" class="col-chip" :style="{ background: c.cover_color }" @click="$router.push(`/salary/columns/${c.id}`)">{{ c.name }}</div>
    </div>

    <div class="section-h">最新爆料</div>
    <van-pull-refresh v-model="refreshing" @refresh="reload">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="loadMore">
        <SalaryCard v-for="r in items" :key="r.id" :item="r" />
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { salaryApi, columnApi } from '@/api'
import SalaryCard from '@/components/SalaryCard.vue'

const rt = ref('campus')
const q = ref('')
const items = ref([])
const cols = ref([])
const page = ref(0)
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)

async function reload() {
  page.value = 0
  finished.value = false
  items.value = []
  await loadMore()
  refreshing.value = false
}
async function loadMore() {
  page.value += 1
  const data = await salaryApi.list({ recruitment_type: rt.value, q: q.value, page: page.value, page_size: 10 })
  items.value.push(...data.items)
  loading.value = false
  if (!data.has_more) finished.value = true
}
columnApi.list({ scope: 'salary' }).then(d => cols.value = d.items)
watch(rt, reload)
reload()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 16px; }
.top {
  background: linear-gradient(180deg, #1E6EFF, #4D8FFF);
  padding: 12px 12px 18px;
}
.search-bar {
  background: rgba(255,255,255,.95); border-radius: 22px;
  height: 36px; padding: 0 14px; display: flex; align-items: center; gap: 6px;
  margin-top: 8px;
  input { flex: 1; border: none; outline: none; background: transparent; font-size: 13px; }
}
.entries {
  margin-top: 12px; background: #fff; border-radius: 12px;
  display: grid; grid-template-columns: repeat(4, 1fr); padding: 10px 0;
  .ent { text-align: center; font-size: 12px; color: var(--os-text-2);
    .ic { font-size: 22px; margin-bottom: 4px; }
  }
}
.section-h { padding: 14px 14px 6px; font-size: 15px; font-weight: 700; }
.columns-row {
  padding: 0 12px; display: flex; gap: 8px; overflow-x: auto;
  .col-chip {
    flex-shrink: 0; padding: 10px 14px; color: #fff;
    border-radius: 8px; font-size: 13px; font-weight: 600;
  }
}
</style>
