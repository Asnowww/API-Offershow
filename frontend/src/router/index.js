import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/jobs' },
  {
    path: '/',
    component: () => import('@/layouts/TabLayout.vue'),
    children: [
      { path: 'jobs', name: 'jobs', component: () => import('@/views/jobs/JobList.vue'), meta: { title: '找名企' } },
      { path: 'salary', name: 'salary', component: () => import('@/views/salary/SalaryHome.vue'), meta: { title: '查薪资' } },
      { path: 'me', name: 'me', component: () => import('@/views/user/Me.vue'), meta: { title: '我的' } },
    ],
  },
  // 找名企
  { path: '/jobs/:id', name: 'job-detail', component: () => import('@/views/jobs/JobDetail.vue') },
  { path: '/daily-brief', name: 'daily-brief', component: () => import('@/views/jobs/DailyBrief.vue') },
  { path: '/courses', name: 'courses', component: () => import('@/views/jobs/Courses.vue') },
  { path: '/columns', name: 'columns', component: () => import('@/views/jobs/Columns.vue') },
  { path: '/columns/:id', name: 'column-detail', component: () => import('@/views/jobs/ColumnDetail.vue') },
  { path: '/refer', name: 'refer', component: () => import('@/views/jobs/Refer.vue') },
  { path: '/review-rank', name: 'review-rank', component: () => import('@/views/jobs/ReviewRank.vue') },
  { path: '/elite', name: 'elite', component: () => import('@/views/jobs/Elite.vue') },
  { path: '/social', name: 'social', component: () => import('@/views/jobs/Social.vue') },
  // 查薪资
  { path: '/salary/feed', name: 'salary-feed', component: () => import('@/views/salary/SalaryFeed.vue') },
  { path: '/salary/rank', name: 'salary-rank', component: () => import('@/views/salary/SalaryRank.vue') },
  { path: '/salary/campus', name: 'salary-campus', component: () => import('@/views/salary/SalaryCampus.vue') },
  { path: '/salary/social', name: 'salary-social', component: () => import('@/views/salary/SalarySocial.vue') },
  { path: '/salary/report', name: 'salary-report', component: () => import('@/views/salary/SalaryReport.vue'), meta: { auth: true } },
  { path: '/salary/columns/:id', name: 'salary-column-detail', component: () => import('@/views/salary/SalaryColumnDetail.vue') },
  { path: '/salary/:id', name: 'salary-detail', component: () => import('@/views/salary/SalaryDetail.vue') },
  // 用户 / HR / 登录
  { path: '/login', name: 'login', component: () => import('@/views/user/Login.vue') },
  { path: '/hr', name: 'hr', component: () => import('@/views/user/HrConsole.vue'), meta: { auth: true, role: 'hr' } },
  { path: '/:pathMatch(.*)*', component: () => import('@/views/NotFound.vue') },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  const userStr = localStorage.getItem('os_user')
  const user = userStr ? JSON.parse(userStr) : null
  if (to.meta.auth && !user) return { name: 'login', query: { redirect: to.fullPath } }
  if (to.meta.role && (!user || (user.role !== to.meta.role && user.role !== 'admin'))) {
    return { name: 'me' }
  }
  return true
})

export default router
