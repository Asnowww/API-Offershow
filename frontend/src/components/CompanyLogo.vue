<template>
  <div class="cl" :style="{ background: bg, width: size + 'px', height: size + 'px', fontSize: fontSize + 'px', borderRadius: round + 'px' }">
    <span>{{ shortName }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  text: { type: String, default: '' },
  color: { type: String, default: '#1E6EFF' },
  size: { type: Number, default: 44 },
  round: { type: Number, default: 8 },
})
const bg = computed(() => props.color)
const fontSize = computed(() => Math.floor(props.size * 0.36))
const shortName = computed(() => (props.text || '').slice(0, 2))
</script>

<style scoped>
.cl {
  display: inline-flex;
  align-items: center; justify-content: center;
  color: #fff; font-weight: 700;
  flex-shrink: 0;
  letter-spacing: 0;
}
</style>
