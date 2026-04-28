<template>
  <div class="page">
    <PageHeader title="薪资爆料" />
    <div class="hero">
      <div class="big">薪资爆料</div>
      <div class="sub">薪资爆料，就上 OfferShow</div>
    </div>
    <van-form @submit="onSubmit" class="form">
      <div class="card">
        <div class="lh"><van-icon name="manager-o" /> 公司</div>
        <van-field v-model="form.company" placeholder="公司名称" :rules="[{required:true}]" />
        <div class="lh"><van-icon name="bag-o" /> 岗位</div>
        <van-field v-model="form.position" placeholder="岗位名称" :rules="[{required:true}]" />
        <div class="lh"><van-icon name="location-o" /> 城市</div>
        <van-field v-model="form.city" placeholder="岗位所在城市，如北京" :rules="[{required:true}]" />
        <div class="lh"><van-icon name="balance-o" /> 薪资描述</div>
        <van-field v-model="form.salary_desc" placeholder="薪资详情，如25W或者16*16" :rules="[{required:true}]" />
        <div class="lh"><van-icon name="exchange" /> 年薪范围换算（选填）</div>
        <div class="row">
          <van-field v-model="form.annual_min" placeholder="年薪下限" type="digit" />
          <span>—</span>
          <van-field v-model="form.annual_max" placeholder="年薪上限" type="digit" />
        </div>
        <div class="hint">注意：年薪以万为单位，年薪上限包含各类福利和年终奖</div>

        <div class="lh"><van-icon name="user-o" /> 类型 - 校招</div>
        <div class="seg">
          <span v-for="t in types" :key="t.value" :class="{active: form.recruitment_type===t.value}" @click="form.recruitment_type=t.value">{{ t.label }}</span>
        </div>
        <div class="lh"><van-icon name="award-o" /> 学历</div>
        <div class="seg">
          <span v-for="e in eduOpts" :key="e" :class="{active: form.education===e}" @click="form.education=e">{{ e }}</span>
        </div>
        <div class="lh"><van-icon name="apps-o" /> 行业</div>
        <div class="seg wrap">
          <span v-for="i in industries" :key="i.code" :class="{active: form.industry===i.code}" @click="form.industry=i.code">{{ i.name }}</span>
        </div>
        <div class="lh"><van-icon name="comment-o" /> 备注</div>
        <van-field v-model="form.remark" type="textarea" rows="3" placeholder="如：签字费 5w，工作作息 10-7-5" />
      </div>

      <div class="agree">
        <van-checkbox v-model="agree" /> 我已阅读并接受 OfferShow 免责声明
      </div>
      <div class="submit-wrap">
        <van-button block round type="primary" native-type="submit" :disabled="!agree">确认后爆料</van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showSuccessToast, showFailToast } from 'vant'
import { salaryApi } from '@/api'
import { industries, recruitmentTypes as types } from '@/api/mockData'
import PageHeader from '@/components/PageHeader.vue'

const router = useRouter()
const eduOpts = ['大专','本科','硕士','博士']
const agree = ref(false)
const form = reactive({
  company: '', position: '', city: '', salary_desc: '',
  annual_min: '', annual_max: '',
  recruitment_type: 'campus', education: '本科', industry: 'internet', remark: '',
})
async function onSubmit() {
  if (!agree.value) return showFailToast('请先勾选免责声明')
  await salaryApi.create(form)
  showSuccessToast('提交成功，等待审核')
  router.replace('/salary')
}
</script>

<style scoped lang="scss">
.page { background: var(--os-bg); min-height: 100vh; padding-bottom: 30px; }
.hero {
  background: linear-gradient(180deg, #1E6EFF, #4D8FFF); color: #fff;
  text-align: center; padding: 18px 0 36px;
  .big { font-size: 26px; font-weight: 800; }
  .sub { font-size: 13px; opacity: .9; margin-top: 4px; }
}
.form { margin-top: -24px; padding: 0 12px; }
.card { background: #fff; border-radius: 12px; padding: 14px; }
.lh { color: var(--os-primary); font-weight: 700; font-size: 13px; margin: 12px 0 6px; display: flex; align-items: center; gap: 4px; }
.row { display: flex; gap: 8px; align-items: center;
  :deep(.van-field) { flex: 1; }
}
.hint { font-size: 11px; color: var(--os-text-3); margin-top: 4px; }
.seg {
  display: flex; gap: 8px; flex-wrap: wrap;
  span { padding: 6px 14px; background: #F4F6F9; color: var(--os-text-2); border-radius: 6px; font-size: 13px;
    &.active { background: #E3EEFF; color: var(--os-primary); font-weight: 700; }
  }
  &.wrap { gap: 6px; span { padding: 4px 10px; font-size: 12px; } }
}
.agree { padding: 14px 14px 8px; font-size: 12px; color: var(--os-text-2); display: flex; align-items: center; gap: 6px; }
.submit-wrap { padding: 6px 14px 14px; }
:deep(.van-field) {
  background: #F4F6F9; border-radius: 8px; padding: 10px 12px !important; margin-top: 4px;
  &::after { display: none; }
}
</style>
