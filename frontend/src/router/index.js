import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import UserList from '../views/UserList.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/userList', name: 'UserList', component: UserList }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path === '/login') {
    next()
  } else {
    token ? next() : next('/login')
  }
})

export default router