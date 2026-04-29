<template>
  <div v-if="pages > 1" class="pager">
    <button class="nav" :disabled="page <= 1" aria-label="上一页" @click="go(page - 1)">
      <van-icon name="arrow-left" />
    </button>
    <button
      v-for="p in visiblePages"
      :key="p"
      :class="['num', { active: p === page }]"
      @click="go(p)"
    >
      {{ p }}
    </button>
    <button class="nav" :disabled="page >= pages" aria-label="下一页" @click="go(page + 1)">
      <van-icon name="arrow" />
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  page: { type: Number, required: true },
  pages: { type: Number, required: true },
})
const emit = defineEmits(['change'])

const visiblePages = computed(() => {
  const total = Math.max(props.pages || 0, 0)
  if (total <= 5) return Array.from({ length: total }, (_, i) => i + 1)
  let start = Math.max(props.page - 2, 1)
  let end = Math.min(start + 4, total)
  start = Math.max(end - 4, 1)
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

function go(next) {
  if (next < 1 || next > props.pages || next === props.page) return
  emit('change', next)
}
</script>

<style scoped lang="scss">
.pager {
  height: 60px;
  padding: 0 18px 12px;
  display: grid;
  grid-template-columns: 44px repeat(5, minmax(36px, 1fr)) 44px;
  align-items: center;
  gap: 4px;
  background: var(--os-bg);
}
button {
  height: 44px;
  border: 0;
  background: transparent;
  color: var(--os-text-2);
  font-size: 16px;
}
.nav {
  font-size: 22px;
  color: var(--os-text-3);
  &:disabled {
    opacity: .25;
  }
}
.num {
  position: relative;
  font-weight: 500;
  &.active {
    color: #111827;
    font-weight: 700;
    &::after {
      content: '';
      position: absolute;
      left: 50%;
      bottom: 5px;
      width: 34px;
      height: 3px;
      transform: translateX(-50%);
      background: #333;
    }
  }
}
</style>

