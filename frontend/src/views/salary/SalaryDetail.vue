<template>
  <div class="page" v-if="r">
    <PageHeader title="薪资详情" />
    <div class="card">
      <div class="head">
        <CompanyLogo :text="r.company.logo_text" :color="r.company.logo_color" :size="44" />
        <div class="col">
          <div class="cn">{{ r.company.name }} · {{ r.position }}</div>
          <div class="meta">{{ r.city }} · {{ r.education }} · {{ r.created_at }}</div>
        </div>
        <div class="salary">{{ r.salary_desc }}</div>
      </div>
      <div class="annual">折算年薪 {{ r.annual_min }} ~ {{ r.annual_max }} 万 · 可信度 {{ r.credibility }}</div>
      <div class="tags"><span v-for="t in r.tags" :key="t" class="os-tag">{{ t }}</span></div>
      <div class="remark">{{ r.remark }}</div>
    </div>
    <div class="actions">
      <div class="ai">👍 {{ r.likes }}</div>
      <div class="ai">👁 {{ r.views }}</div>
      <div class="ai">⭐ 收藏</div>
      <div class="ai">⚑ 举报</div>
    </div>
    <div class="card">
      <div class="card-h">评论 ({{ comments.length }})</div>
      <div v-if="!comments.length" class="empty">暂无评论，来抢沙发</div>
      <div v-for="c in comments" :key="c.id" class="cm">
        <div class="cmu">{{ c.user }}</div>
        <div class="cmc">{{ c.content }}</div>
      </div>
    </div>
    <div class="comment-bar">
      <input v-model="text" placeholder="说点什么…" />
      <van-button size="small" round type="primary" @click="postComment">发送</van-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { salaryApi } from '@/api'
import { showSuccessToast } from 'vant'
import CompanyLogo from '@/components/CompanyLogo.vue'
import PageHeader from '@/components/PageHeader.vue'

const route = useRoute()
const r = ref(null)
const comments = ref([])
const text = ref('')
async function load() { r.value = await salaryApi.get(route.params.id) }
function postComment() {
  if (!text.value.trim()) return
  comments.value.push({ id: Date.now(), user: '匿名用户', content: text.value })
  text.value = ''
  showSuccessToast('评论成功')
}
load()
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 60px; }
.card { background: #fff; margin: 8px 12px; border-radius: 12px; padding: 14px; }
.head { display: flex; gap: 10px; align-items: center; }
.col { flex: 1; min-width: 0; }
.cn { font-size: 15px; font-weight: 700; }
.meta { font-size: 11px; color: var(--os-text-3); margin-top: 4px; }
.salary { color: var(--os-orange); font-weight: 800; font-size: 18px; }
.annual { font-size: 12px; color: var(--os-text-2); margin-top: 10px; }
.tags { margin-top: 8px; }
.remark { font-size: 13px; line-height: 1.7; margin-top: 10px; color: var(--os-text); }
.actions { display: flex; justify-content: space-around; padding: 10px 0;
  .ai { font-size: 12px; color: var(--os-text-2); }
}
.card-h { border-left: 3px solid var(--os-primary); padding-left: 8px; font-weight: 700; margin-bottom: 12px; }
.empty { text-align: center; color: var(--os-text-3); padding: 14px 0; font-size: 13px; }
.cm { padding: 8px 0; border-bottom: 1px solid var(--os-border); }
.cmu { font-size: 12px; color: var(--os-text-3); }
.cmc { font-size: 14px; margin-top: 4px; }
.comment-bar { position: fixed; bottom: 0; left: 0; right: 0; background: #fff; padding: 8px 12px; display: flex; gap: 8px; border-top: 1px solid var(--os-border);
  input { flex: 1; height: 34px; border-radius: 17px; border: 1px solid var(--os-border); padding: 0 12px; outline: none; }
}
</style>
