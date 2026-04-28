<template>
  <div class="page" v-if="job">
    <PageHeader title="招聘详情" />
    <div class="hero">
      <CompanyLogo :text="job.company.logo_text" :color="job.company.logo_color" :size="56" />
      <div class="ti">
        <div class="title os-ellipsis-2">{{ job.title }}</div>
        <div class="meta">
          <span>{{ job.created_at }} 发布</span>
          <span>· {{ industryLabel }}</span>
        </div>
        <div class="meta">
          <span>👁 {{ job.views }} 人次浏览</span>
          <span class="dot">·</span>
          <span>👍 {{ job.interest_count }} 人感兴趣</span>
        </div>
      </div>
    </div>

    <div class="badges">
      <span class="badge orange">暑期投递榜 月榜 TOP 5</span>
      <span class="badge blue">求职专栏 春招早鸟专场</span>
    </div>

    <van-tabs v-model:active="tab" sticky offset-top="46px" line-width="20px" line-height="3px" color="#1E6EFF">
      <van-tab title="招聘信息">
        <div class="card">
          <div class="card-h">招聘信息</div>
          <div class="benefits">
            <span v-for="b in job.benefits" :key="b" class="benefit">{{ b }}</span>
          </div>
          <div class="kv"><span class="k">招聘批次</span><span class="v">{{ job.batch }}</span></div>
          <div class="kv"><span class="k">工作城市</span><span class="v">{{ job.cities.join(' | ') }}</span></div>
          <div class="kv"><span class="k">投递时间</span><span class="v">{{ job.deliver_start }} ~ {{ job.deliver_end }}</span></div>
          <div class="kv"><span class="k">招聘届属</span><span class="v">{{ job.graduation_range }}</span></div>
          <div class="kv">
            <span class="k">投递链接</span>
            <span class="v link" @click="copy(job.apply_url)">{{ job.apply_url }} 复制</span>
          </div>
        </div>

        <div class="refer-card">
          <div class="refer-title">参与 OfferShow 内推，简历优先筛选</div>
          <div class="refer-code-row">
            <span class="refer-code">{{ job.internal_code }}</span>
            <van-button size="small" round type="primary" @click="copy(job.internal_code)">复制</van-button>
          </div>
        </div>
      </van-tab>

      <van-tab title="招聘岗位">
        <div class="card">
          <div class="card-h">招聘岗位</div>
          <ol class="positions">
            <li v-for="p in job.positions" :key="p.id">{{ p.name }}</li>
          </ol>
          <div class="hint">*更多岗位详情可复制官网投递链接查看</div>
        </div>
      </van-tab>

      <van-tab title="招聘简介">
        <div class="card">
          <div class="card-h">招聘简介</div>
          <div class="rich" v-html="job.intro_html" />
        </div>
      </van-tab>

      <van-tab title="公司简介">
        <div class="card">
          <div class="company-row">
            <CompanyLogo :text="job.company.logo_text" :color="job.company.logo_color" :size="56" />
            <div class="cn">{{ job.company.name }}</div>
          </div>
          <div class="company-intro">{{ companyIntro }}</div>
        </div>
      </van-tab>
    </van-tabs>

    <div class="bottom-bar">
      <div class="b-item"><van-icon name="share-o" />分享</div>
      <div class="b-item"><van-icon name="calendar-o" />我的日程</div>
      <van-button type="default" plain class="b-btn">加入日程</van-button>
      <van-button type="primary" class="b-btn primary" @click="copy(job.apply_url)">复制投递链接</van-button>
    </div>
  </div>
  <van-loading v-else class="loading" />
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { showToast } from 'vant'
import { jobApi } from '@/api'
import { industries } from '@/api/mockData'
import CompanyLogo from '@/components/CompanyLogo.vue'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const job = ref(null)
const tab = ref(0)
const industryLabel = computed(() => industries.find(i => i.code === job.value?.industry)?.name || '')
const companyIntro = computed(() => `${job.value?.company.name} —— 行业头部企业，提供具有竞争力的薪酬与福利待遇，欢迎投递。`)

async function load() {
  job.value = await jobApi.get(route.params.id)
}
function copy(text) {
  navigator.clipboard?.writeText(text)
  showToast('已复制：' + text)
}
load()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 70px; }
.loading { text-align: center; padding-top: 100px; }
.hero {
  background: linear-gradient(180deg, #2D7BFF 0%, #4D8FFF 100%);
  padding: 16px 14px 28px; display: flex; gap: 12px; color: #fff;
  .ti { flex: 1; min-width: 0; }
  .title { font-size: 17px; font-weight: 700; }
  .meta { font-size: 11px; margin-top: 6px; opacity: .9; display: flex; gap: 8px; }
  .dot { opacity: .6; }
}
.badges { padding: 8px 14px; display: flex; gap: 8px; margin-top: -12px; position: relative; z-index: 2; }
.badge { font-size: 11px; padding: 3px 8px; border-radius: 4px; background: #fff; }
.badge.orange { color: #C77E00; background: #FFEBC2; }
.badge.blue { color: var(--os-primary); background: #E3EEFF; }

.card {
  background: #fff; margin: 8px 12px; border-radius: 12px; padding: 14px;
  .card-h { border-left: 3px solid var(--os-primary); padding-left: 8px; font-weight: 700; font-size: 15px; margin-bottom: 12px; }
}
.benefits { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
.benefit {
  background: #FFF1E5; color: #C77E00; font-size: 11px;
  padding: 4px 8px; border-radius: 4px;
}
.kv { display: flex; padding: 6px 0; font-size: 13px;
  .k { width: 80px; color: var(--os-text-3); }
  .v { flex: 1; word-break: break-all; }
  .v.link { color: var(--os-primary); }
}
.refer-card {
  margin: 8px 12px; padding: 14px; border-radius: 12px;
  background: linear-gradient(135deg, #1E6EFF, #4D8FFF); color: #fff;
  .refer-title { font-size: 13px; opacity: .9; margin-bottom: 10px; }
  .refer-code-row { display: flex; align-items: center; justify-content: space-between; }
  .refer-code { font-size: 22px; font-weight: 800; letter-spacing: 2px; }
}
.positions { padding-left: 22px; line-height: 2; font-size: 14px; }
.hint { font-size: 12px; color: var(--os-text-3); margin-top: 12px; }
.rich { font-size: 13px; line-height: 1.7; color: var(--os-text); }
.rich :deep(b) { color: var(--os-primary); }
.company-row { display: flex; gap: 12px; align-items: center; margin-bottom: 12px; }
.cn { font-size: 16px; font-weight: 700; }
.company-intro { font-size: 13px; line-height: 1.7; color: var(--os-text-2); }
.bottom-bar {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; align-items: center; gap: 8px; padding: 8px 12px;
  background: #fff; border-top: 1px solid var(--os-border); z-index: 99;
  .b-item { display: flex; flex-direction: column; align-items: center; font-size: 11px; color: var(--os-text-2); padding: 0 6px; }
  .b-btn { flex: 1; border-radius: 18px !important; height: 36px !important; }
  .b-btn.primary { background: var(--os-primary); border-color: var(--os-primary); color: #fff; }
}
</style>
