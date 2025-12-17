import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫，检查登录状态
router.beforeEach((to, from, next) => {
  // 登录页面不需要验证
  if (to.path === '/login') {
    next()
    return
  }
  
  // 检查登录状态，实际项目中可以使用真实的登录状态检查
  const isLoggedIn = localStorage.getItem('isLoggedIn') || false
  
  if (isLoggedIn) {
    next()
  } else {
    // 未登录，跳转到登录页面
    next('/login')
  }
})

export default router