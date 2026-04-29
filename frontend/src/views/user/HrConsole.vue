<template>
  <div class="page">
    <PageHeader title="HR / 管理员后台" />
    <van-tabs v-model:active="tab" color="#1E6EFF">
      <van-tab title="发布招聘">
        <div class="form">
          <van-field v-model="form.title" label="标题" placeholder="如：极兔速递2026校园招聘" />
          <van-field v-model="form.batch" label="批次" placeholder="校招正式批" />
          <van-field v-model="form.cities" label="城市" placeholder="逗号分隔，如：北京,上海" />
          <van-field v-model="form.industry" label="行业" placeholder="如 internet" />
          <van-field v-model="form.apply_url" label="投递链接" />
          <van-field v-model="form.internal_code" label="内推码" />
          <van-button block type="primary" round @click="create">创建招聘信息（POST）</van-button>
        </div>
      </van-tab>
      <van-tab title="批量上传">
        <div class="form">
          <van-field v-model="csv" label="CSV 文本" type="textarea" rows="6" placeholder="title,batch,cities&#10;A招聘,春招正式批,北京;上海" />
          <van-button block type="primary" round @click="batch">批量上传（:batchCreate）</van-button>
          <div class="result" v-if="batchResult">{{ batchResult }}</div>
        </div>
      </van-tab>
      <van-tab title="管理列表">
        <JobCard v-for="j in items" :key="j.id" :job="j" />
        <PaginationBar :page="page" :pages="pages" @change="reload" />
      </van-tab>
    </van-tabs>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { jobApi } from '@/api'
import { showSuccessToast } from 'vant'
import JobCard from '@/components/JobCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import PaginationBar from '@/components/PaginationBar.vue'

const tab = ref(0)
const items = ref([])
const page = ref(1)
const pages = ref(1)
const batchResult = ref('')
const csv = ref('字节跳动2026春招,春招正式批,北京;上海\n腾讯2026春招,春招正式批,深圳')
const form = reactive({ title: '', batch: '春招正式批', cities: '北京,上海', industry: 'internet', apply_url: 'https://example.com', internal_code: 'OS-DEMO' })

async function create() {
  await jobApi.create({ ...form, cities: form.cities.split(',') })
  showSuccessToast('创建成功')
  reload(1)
}
async function batch() {
  const lines = csv.value.split('\n').filter(Boolean)
  const items = lines.map(l => {
    const [title, batch, cities] = l.split(',')
    return { title, batch, cities: cities.split(';'), industry: 'internet' }
  })
  const res = await jobApi.batchCreate(items)
  batchResult.value = `成功 ${res.success} 条 / 失败 ${res.failed} 条`
  showSuccessToast('批量提交完成')
}
async function reload(nextPage = 1) {
  page.value = nextPage
  const data = await jobApi.list({ page: page.value, page_size: 5 })
  items.value = data.items
  pages.value = data.pages || 1
}
reload()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.form { padding: 12px;
  :deep(.van-field) { background: #fff; border-radius: 8px; margin-bottom: 8px; }
  .van-button { margin-top: 12px; }
}
.result { margin-top: 12px; padding: 10px; background: #fff; border-radius: 8px; font-size: 13px; }
</style>
