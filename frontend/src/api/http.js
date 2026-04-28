import axios from 'axios'
import { showFailToast } from 'vant'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api/v1',
  timeout: 15000,
})

http.interceptors.request.use((cfg) => {
  const token = localStorage.getItem('os_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

http.interceptors.response.use(
  (res) => {
    const body = res.data
    if (body && typeof body === 'object' && 'code' in body) {
      if (body.code === 0) return body.data
      showFailToast(body.message || `错误 ${body.code}`)
      return Promise.reject(body)
    }
    return body
  },
  (err) => {
    showFailToast(err?.response?.data?.message || err.message || '网络错误')
    return Promise.reject(err)
  }
)

export default http
