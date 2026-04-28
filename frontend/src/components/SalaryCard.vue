<template>
  <div class="sc" @click="$router.push(`/salary/${item.id}`)">
    <div class="head">
      <CompanyLogo :text="item.company.logo_text || item.company.name" :color="item.company.logo_color" :size="36" :round="6" />
      <div class="name-col">
        <div class="name os-ellipsis">{{ item.company.name }} · {{ item.position }}</div>
        <div class="meta">
          <span>{{ item.city }}</span>
          <span>·</span>
          <span>{{ item.education }}</span>
          <span v-for="t in item.edu_tags" :key="t">·{{ t }}</span>
        </div>
      </div>
      <div class="salary-col">
        <div class="salary">{{ item.salary_desc }}</div>
        <div class="cred">可信度 {{ item.credibility }}</div>
      </div>
    </div>
    <div v-if="item.remark" class="remark os-ellipsis-2">{{ item.remark }}</div>
    <div class="foot">
      <span v-for="t in item.tags.slice(0,3)" :key="t" class="os-tag">{{ t }}</span>
      <span class="grow"></span>
      <span class="views">👁 {{ item.views }}</span>
      <span class="month">{{ item.created_at?.slice(5) }}</span>
    </div>
  </div>
</template>

<script setup>
import CompanyLogo from './CompanyLogo.vue'
defineProps({ item: { type: Object, required: true } })
</script>

<style scoped>
.sc {
  background: #fff; padding: 12px; margin: 8px 12px;
  border-radius: 12px;
}
.head { display: flex; gap: 10px; align-items: center; }
.name-col { flex: 1; min-width: 0; }
.name { font-size: 14px; font-weight: 600; }
.meta { font-size: 11px; color: var(--os-text-3); margin-top: 4px; display: flex; gap: 4px; flex-wrap: wrap; }
.salary-col { text-align: right; }
.salary { font-size: 16px; font-weight: 700; color: var(--os-orange); }
.cred { font-size: 11px; color: var(--os-text-3); margin-top: 2px; }
.remark { font-size: 13px; color: var(--os-text-2); margin-top: 8px; line-height: 1.4; }
.foot { display: flex; gap: 6px; align-items: center; margin-top: 8px; font-size: 11px; color: var(--os-text-3); }
.grow { flex: 1; }
.views { margin-right: 6px; }
</style>
