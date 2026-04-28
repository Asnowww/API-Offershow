<template>
  <div class="page">
    <div class="hero">
      <div class="user-row">
        <div class="avatar">{{ avatar }}</div>
        <div class="col" v-if="user.isLoggedIn">
          <div class="nick">{{ user.user.nickname }}</div>
          <div class="role">角色：{{ user.role }}</div>
        </div>
        <div class="col" v-else>
          <div class="nick">未登录</div>
          <div class="role" @click="$router.push('/login')">点此登录 / 注册</div>
        </div>
      </div>
    </div>
    <div class="grid">
      <div class="g" @click="$router.push('/salary/report')"><div class="ic">📤</div>我要爆料</div>
      <div class="g" @click="toast"><div class="ic">⭐</div>我的收藏</div>
      <div class="g" @click="toast"><div class="ic">📅</div>我的日程</div>
      <div class="g" @click="$router.push('/daily-brief')"><div class="ic">📰</div>我的订阅</div>
    </div>
    <van-cell-group inset class="menu">
      <van-cell title="求职好课" is-link @click="$router.push('/courses')" icon="bookmark-o" />
      <van-cell title="求职专栏" is-link @click="$router.push('/columns')" icon="apps-o" />
      <van-cell title="实习点评榜" is-link @click="$router.push('/review-rank')" icon="star-o" />
      <van-cell title="顶尖人才计划" is-link @click="$router.push('/elite')" icon="medal-o" />
    </van-cell-group>
    <van-cell-group inset class="menu" v-if="user.isLoggedIn && (user.role === 'hr' || user.role === 'admin')">
      <van-cell title="HR / 管理员后台" is-link @click="$router.push('/hr')" icon="setting-o" />
    </van-cell-group>
    <van-cell-group inset class="menu" v-if="user.isLoggedIn">
      <van-cell title="退出登录" is-link @click="logout" icon="close" />
    </van-cell-group>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { showToast } from 'vant'
const user = useUserStore()
const avatar = computed(() => user.user?.nickname?.slice(0,1) || 'O')
function logout() { user.logout(); showToast('已退出登录') }
function toast() { showToast('演示页面：暂未实现') }
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 16px; }
.hero { background: linear-gradient(180deg, #1E6EFF, #4D8FFF); color: #fff; padding: 30px 20px; }
.user-row { display: flex; gap: 14px; align-items: center; }
.avatar { width: 60px; height: 60px; border-radius: 50%; background: rgba(255,255,255,.25); display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; }
.col .nick { font-size: 18px; font-weight: 700; }
.col .role { font-size: 12px; opacity: .85; margin-top: 4px; }
.grid {
  margin: -14px 12px 0; background: #fff; border-radius: 12px; padding: 12px 0;
  display: grid; grid-template-columns: repeat(4, 1fr); position: relative;
  .g { text-align: center; font-size: 12px;
    .ic { font-size: 22px; margin-bottom: 4px; }
  }
}
.menu { margin-top: 12px !important; }
:deep(.van-cell-group--inset) { border-radius: 12px; overflow: hidden; }
</style>
