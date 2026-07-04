import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000
})

// 请求拦截
service.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截
let isRefreshing = false
let requests = []
service.interceptors.response.use(
  res => {
    return res.data
  },
  async err => {
    const config = err.config
    // 401 令牌过期
    if (err.response?.status === 401 && !isRefreshing) {
      isRefreshing = true
      const refreshToken = localStorage.getItem('refreshToken')
      if (!refreshToken) {
        ElMessage.warning('登录已失效，请重新登录')
        localStorage.clear()
        router.push('/login')
        return Promise.reject(err)
      }

      try {
        // 调用刷新接口
        const res = await axios.post('/token/refresh', {
          refresh: refreshToken
        })
        // 更新新token
        localStorage.setItem('accessToken', res.data.access)
        // 重新执行之前失败请求
        config.headers.Authorization = `Bearer ${res.data.access}`
        requests.forEach(cb => cb(res.data.access))
        requests = []
        return service(config)
      } catch {
        // 刷新失败，跳转登录
        localStorage.clear()
        router.push('/login')
        ElMessage.error('登录过期，请重新登录')
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(err)
  }
)

export default service