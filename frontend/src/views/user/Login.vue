<template>
  <div class="page">
    <PageHeader title="登录" />
    <div class="hero">
      <div class="big">OfferShow</div>
      <div class="sub">薪资爆料 · 校招内推 · 求职社区</div>
    </div>
    <div class="card">
      <van-field v-model="username" label="账号" placeholder="演示账号：demo / hr / admin" />
      <van-field v-model="password" label="密码" type="password" placeholder="对应密码：demo / hr / admin" />
      <van-button block round type="primary" :loading="loading" @click="onLogin">登录</van-button>
      <div class="tips">
        <div>📌 演示账号说明：</div>
        <div>· demo / demo：普通用户</div>
        <div>· hr / hr：HR 角色（可访问 HR 后台）</div>
        <div>· admin / admin：管理员</div>
      </div>
      <div class="hr-line"><span>或</span></div>
      <van-button block round plain @click="wxLogin">通过微信公众号登录（演示）</van-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showSuccessToast } from 'vant'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api'
import PageHeader from '@/components/PageHeader.vue'

const username = ref('demo')
const password = ref('demo')
const loading = ref(false)
const user = useUserStore()
const router = useRouter()
const route = useRoute()

async function onLogin() {
  loading.value = true
  try {
    await user.login({ username: username.value, password: password.value })
    showSuccessToast('登录成功')
    router.replace(route.query.redirect || '/me')
  } finally { loading.value = false }
}
async function wxLogin() {
  const { token, user: u } = await authApi.wxLogin({ code: 'mock-code' })
  user.token = token
  user.user = u
  localStorage.setItem('os_token', token)
  localStorage.setItem('os_user', JSON.stringify(u))
  showSuccessToast('已通过公众号登录')
  router.replace(route.query.redirect || '/me')
}
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; }
.hero { background: linear-gradient(180deg, #1E6EFF, #4D8FFF); color: #fff; padding: 30px 0; text-align: center;
  .big { font-size: 28px; font-weight: 800; }
  .sub { font-size: 13px; opacity: .9; margin-top: 4px; }
}
.card { background: #fff; margin: -16px 12px 12px; border-radius: 12px; padding: 16px; }
.tips { font-size: 12px; color: var(--os-text-3); margin-top: 12px; line-height: 1.7; background: #F4F6F9; padding: 10px; border-radius: 8px; }
.hr-line { text-align: center; color: var(--os-text-3); font-size: 12px; margin: 12px 0; position: relative;
  &::before, &::after { content: ''; position: absolute; top: 50%; height: 1px; width: 38%; background: var(--os-border); }
  &::before { left: 0; } &::after { right: 0; }
}
</style>
