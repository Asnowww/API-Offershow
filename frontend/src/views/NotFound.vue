<template>
  <div class="nf">
    <div class="big">404</div>
    <div class="sub">页面不存在</div>
    <van-button round type="primary" @click="$router.replace('/')">回首页</van-button>
  </div>
</template>

<style scoped>
.nf { padding-top: 30vh; text-align: center; min-height: 100vh; background: var(--os-bg); }
.big { font-size: 64px; font-weight: 800; color: var(--os-primary); }
.sub { color: var(--os-text-3); margin-bottom: 24px; }
</style>
