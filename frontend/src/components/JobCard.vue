<template>
  <div class="job-card" @click="$router.push(`/jobs/${job.id}`)">
    <div class="left">
      <div class="title-row">
        <span v-if="job.is_official" class="os-tag os-tag--blue">官方直聘</span>
        <span class="title os-ellipsis">{{ job.title }}</span>
      </div>
      <div class="city-row">
        <span v-for="c in job.cities.slice(0,3)" :key="c" class="city">{{ c }}</span>
      </div>
      <div class="meta-row">
        <span class="os-tag os-tag--orange">{{ job.batch }}</span>
        <span class="meta-icon">👁 {{ job.views }}</span>
        <span class="meta-tag">{{ industryLabel }}</span>
      </div>
    </div>
    <CompanyLogo :text="job.company.logo_text || job.company.name" :color="job.company.logo_color || '#1E6EFF'" :size="56" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import CompanyLogo from './CompanyLogo.vue'
import { industries } from '@/api/mockData'
const props = defineProps({ job: { type: Object, required: true } })
const industryLabel = computed(() => industries.find(i => i.code === props.job.industry)?.name || props.job.industry)
</script>

<style scoped>
.job-card {
  display: flex; gap: 12px;
  padding: 14px 12px;
  background: #fff;
  border-bottom: 1px solid var(--os-border);
}
.left { flex: 1; min-width: 0; }
.title-row { display: flex; align-items: center; gap: 6px; }
.title { font-size: 15px; font-weight: 600; color: var(--os-text); }
.city-row { margin-top: 6px; display: flex; gap: 6px; flex-wrap: wrap; }
.city {
  font-size: 11px; color: var(--os-text-2);
  background: var(--os-tag-bg); border-radius: 4px;
  padding: 2px 6px;
}
.meta-row { margin-top: 8px; display: flex; align-items: center; gap: 10px; font-size: 11px; color: var(--os-text-3); }
.meta-icon { color: var(--os-text-3); }
.meta-tag { color: var(--os-text-2); }
</style>
