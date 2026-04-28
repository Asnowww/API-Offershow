// 统一对外 API。开发期 VITE_USE_MOCK=true 时全部走内存 mock；
// 否则走 http 实例（FastAPI 后端就绪后）。
import http from './http'
import * as M from './mockData'

const USE_MOCK = String(import.meta.env.VITE_USE_MOCK || 'true') === 'true'
const delay = (ms = 200) => new Promise((r) => setTimeout(r, ms))

function paginate(items, { page = 1, page_size = 20 } = {}) {
  page = Number(page) || 1
  page_size = Number(page_size) || 20
  const total = items.length
  const start = (page - 1) * page_size
  return {
    items: items.slice(start, start + page_size),
    page,
    page_size,
    total,
    pages: Math.ceil(total / page_size),
    has_more: start + page_size < total,
  }
}

function matchKw(s, q) {
  if (!q) return true
  return String(s || '').toLowerCase().includes(String(q).toLowerCase())
}

// ========== 字典 ==========
export const dict = {
  industries: async () => { await delay(); return M.industries },
  cities: async () => { await delay(); return M.cities },
  batches: async () => { await delay(); return M.batches },
  recruitmentTypes: async () => { await delay(); return M.recruitmentTypes },
}

// ========== 公司 ==========
export const companyApi = {
  get: async (id) => {
    if (USE_MOCK) { await delay(); return M.jobPostings.find(j => j.company.id === Number(id))?.company || null }
    return http.get(`/companies/${id}`)
  },
  list: async (params = {}) => {
    if (USE_MOCK) {
      await delay()
      const set = new Map()
      M.jobPostings.forEach(j => set.set(j.company.id, j.company))
      let arr = Array.from(set.values())
      if (params.q) arr = arr.filter(c => matchKw(c.name, params.q))
      return paginate(arr, params)
    }
    return http.get('/companies', { params })
  },
}

// ========== 招聘信息 ==========
function filterJobs(params = {}) {
  let arr = M.jobPostings.slice()
  const { q, industry, cities: cs, recruitment_type, batch, has_internal_code, sort } = params
  if (q) arr = arr.filter(j => matchKw(j.company.name, q) || matchKw(j.title, q) || j.positions.some(p => matchKw(p.name, q)))
  if (industry && industry !== 'all') arr = arr.filter(j => j.industry === industry)
  if (cs && cs.length) {
    const wanted = Array.isArray(cs) ? cs : String(cs).split(',')
    arr = arr.filter(j => j.cities.some(c => wanted.includes(c)))
  }
  if (recruitment_type) arr = arr.filter(j => j.recruitment_type === recruitment_type)
  if (batch && batch !== '不限') arr = arr.filter(j => j.batch === batch)
  if (has_internal_code) arr = arr.filter(j => !!j.internal_code)
  if (sort === 'hot') arr.sort((a,b) => b.views - a.views)
  else if (sort === 'deadline') arr.sort((a,b) => a.deliver_end.localeCompare(b.deliver_end))
  else arr.sort((a,b) => b.created_at.localeCompare(a.created_at))
  return arr
}

export const jobApi = {
  list: async (params = {}) => {
    if (USE_MOCK) { await delay(); return paginate(filterJobs(params), params) }
    return http.get('/job-postings', { params })
  },
  get: async (id) => {
    if (USE_MOCK) { await delay(); return M.jobPostings.find(j => j.id === Number(id)) || null }
    return http.get(`/job-postings/${id}`)
  },
  create: async (body) => USE_MOCK ? (await delay(), { ...body, id: Date.now() }) : http.post('/job-postings', body),
  update: async (id, body) => USE_MOCK ? (await delay(), { id, ...body }) : http.patch(`/job-postings/${id}`, body),
  replace: async (id, body) => USE_MOCK ? (await delay(), { id, ...body }) : http.put(`/job-postings/${id}`, body),
  delete: async (id) => USE_MOCK ? (await delay(), { id }) : http.delete(`/job-postings/${id}`),
  batchCreate: async (items) => USE_MOCK ? (await delay(500), { success: items.length, failed: 0 }) : http.post('/job-postings:batchCreate', { items }),
}

// ========== 求职早报 ==========
export const dailyBriefApi = {
  list: async (params = {}) => {
    if (USE_MOCK) { await delay(); return paginate(M.dailyBriefs, params) }
    return http.get('/daily-briefs', { params })
  },
}

// ========== 求职好课 ==========
export const courseApi = {
  list: async (params = {}) => {
    if (USE_MOCK) {
      await delay()
      let arr = M.courses
      if (params.category && params.category !== '全部课程') arr = arr.filter(c => c.category === params.category)
      if (params.q) arr = arr.filter(c => matchKw(c.title, params.q))
      return paginate(arr, params)
    }
    return http.get('/courses', { params })
  },
}

// ========== 专栏 ==========
export const columnApi = {
  list: async (params = {}) => {
    if (USE_MOCK) {
      await delay()
      const scope = params.scope || 'job'
      const arr = scope === 'salary' ? M.salaryColumns : M.columns
      return paginate(arr, params)
    }
    return http.get('/columns', { params })
  },
  get: async (id) => USE_MOCK ? (await delay(), M.columns.find(c => c.id === Number(id)) || M.salaryColumns.find(c => c.id === Number(id))) : http.get(`/columns/${id}`),
  items: async (id, params = {}) => {
    if (USE_MOCK) { await delay(); return paginate(filterJobs({ industry: 'all' }), params) }
    return http.get(`/columns/${id}/items`, { params })
  },
  salaryItems: async (id, params = {}) => {
    if (USE_MOCK) {
      await delay()
      const col = M.salaryColumns.find(c => c.id === Number(id))
      if (!col) return paginate([], params)
      return paginate(filterSalary({ filter_rule: col.filter_rule, ...params }), params)
    }
    return http.get(`/columns/${id}/salary-items`, { params })
  },
}

// ========== 实习点评榜 ==========
export const reviewApi = {
  rank: async (params = {}) => {
    if (USE_MOCK) {
      await delay()
      let arr = M.reviewRank.slice()
      if (params.q) arr = arr.filter(r => matchKw(r.company.name, params.q))
      const tab = params.tab || 'high'
      if (tab === 'high') arr.sort((a,b) => b.score - a.score)
      else if (tab === 'low') arr.sort((a,b) => a.score - b.score)
      else if (tab === 'hot') arr.sort((a,b) => b.reviews - a.reviews)
      arr.forEach((r, i) => r.rank = i + 1)
      return paginate(arr, params)
    }
    return http.get('/companies:reviewRank', { params })
  },
  create: async (body) => USE_MOCK ? (await delay(), { id: Date.now(), ...body }) : http.post('/reviews', body),
}

// ========== 顶尖人才计划 ==========
export const eliteApi = {
  list: async (params = {}) => {
    if (USE_MOCK) {
      await delay()
      let arr = M.elitePrograms
      if (params.q) arr = arr.filter(e => matchKw(e.company.name, params.q) || matchKw(e.name, params.q))
      return paginate(arr, params)
    }
    return http.get('/elite-programs', { params })
  },
}

// ========== 薪资爆料 ==========
function filterSalary(params = {}) {
  let arr = M.salaryReports.slice()
  const { q, recruitment_type, industry, education, city, sort, filter_rule } = params
  if (q) {
    const tokens = String(q).split(/\s+/).filter(Boolean)
    arr = arr.filter(r => tokens.every(t =>
      matchKw(r.company.name, t) || matchKw(r.position, t) || matchKw(r.city, t)
    ))
  }
  if (recruitment_type) arr = arr.filter(r => r.recruitment_type === recruitment_type)
  if (industry && industry !== 'all') arr = arr.filter(r => r.industry === industry)
  if (education) arr = arr.filter(r => r.education === education)
  if (city) arr = arr.filter(r => r.city === city)
  if (filter_rule) {
    const f = filter_rule
    if (f.industry) arr = arr.filter(r => r.industry === f.industry)
    if (f.edu_tags_any) arr = arr.filter(r => r.edu_tags?.some(t => f.edu_tags_any.includes(t)))
    if (f.position_any) arr = arr.filter(r => f.position_any.includes(r.position))
    if (f.company_id_any) arr = arr.filter(r => f.company_id_any.includes(r.company.id))
    if (f.annual_min_gte != null) arr = arr.filter(r => r.annual_max >= f.annual_min_gte)
    if (f.annual_min_lte != null) arr = arr.filter(r => r.annual_max <= f.annual_min_lte)
  }
  if (sort === 'hot') arr.sort((a,b) => (b.views + b.likes*5) - (a.views + a.likes*5))
  else if (sort === 'credibility') arr.sort((a,b) => b.credibility - a.credibility)
  else arr.sort((a,b) => b.created_at.localeCompare(a.created_at))
  return arr
}

export const salaryApi = {
  list: async (params = {}) => USE_MOCK ? (await delay(), paginate(filterSalary(params), params)) : http.get('/salary-reports', { params }),
  get: async (id) => USE_MOCK ? (await delay(), M.salaryReports.find(r => r.id === Number(id))) : http.get(`/salary-reports/${id}`),
  create: async (body) => USE_MOCK ? (await delay(500), { id: Date.now(), credibility: 65, ...body }) : http.post('/salary-reports', body),
  rank: async (params = {}) => {
    if (USE_MOCK) {
      await delay()
      const arr = M.salaryReports.slice().sort((a,b) => (b.views + b.likes*5) - (a.views + a.likes*5))
      return paginate(arr, params)
    }
    return http.get('/salary-reports:rank', { params })
  },
}

// ========== 用户 / 登录 ==========
export const authApi = {
  login: async ({ username, password }) => {
    if (USE_MOCK) {
      await delay()
      const u = M.adminAccounts.find(a => a.username === username && a.password === password)
      if (!u) throw { code: 40101, message: '账号或密码错误' }
      const token = 'mock-token-' + u.id + '-' + Date.now()
      const { password: _, ...user } = u
      return { token, token_type: 'bearer', expires_in: 7200, user }
    }
    return http.post('/auth/login', { username, password })
  },
  wxLogin: async ({ code }) => {
    if (USE_MOCK) {
      await delay()
      const u = M.adminAccounts[0]
      const token = 'mock-wx-token-' + Date.now()
      return { token, expires_in: 7200, user: { ...u, password: undefined } }
    }
    return http.post('/auth/wx-login', { code })
  },
  me: async () => {
    if (USE_MOCK) {
      await delay()
      const userStr = localStorage.getItem('os_user')
      return userStr ? JSON.parse(userStr) : null
    }
    return http.get('/users/me')
  },
}

// ========== 订阅 ==========
export const subscriptionApi = {
  toggle: async (type) => USE_MOCK ? (await delay(), { type, status: 'on' }) : http.post('/subscriptions', { type }),
}

// ========== 统一搜索 ==========
export const searchApi = {
  search: async (params = {}) => {
    if (USE_MOCK) {
      await delay()
      const q = params.q || ''
      const scope = params.scope || 'job'
      if (scope === 'salary') return paginate(filterSalary({ q }), params)
      if (scope === 'company') return companyApi.list({ q, ...params })
      return paginate(filterJobs({ q }), params)
    }
    return http.get('/search', { params })
  },
}
