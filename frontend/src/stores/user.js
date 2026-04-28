import { defineStore } from 'pinia'
import { authApi } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('os_token') || '',
    user: JSON.parse(localStorage.getItem('os_user') || 'null'),
  }),
  getters: {
    isLoggedIn: (s) => !!s.token,
    role: (s) => s.user?.role || 'guest',
    isMember: (s) => ['member','hr','admin'].includes(s.user?.role),
  },
  actions: {
    async login(payload) {
      const { token, user } = await authApi.login(payload)
      this.token = token
      this.user = user
      localStorage.setItem('os_token', token)
      localStorage.setItem('os_user', JSON.stringify(user))
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('os_token')
      localStorage.removeItem('os_user')
    },
  },
})
