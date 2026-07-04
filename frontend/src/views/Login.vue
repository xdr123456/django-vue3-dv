<template>
  <div class="login-wrap">
    <el-card style="width: 420px;padding:20px">
      <h2 style="text-align:center;margin-bottom:20px">Django+Vue3 JWT登录</h2>
      <el-form ref="formRef" :model="form">
        <el-form-item label="账号">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width:100%" @click="doLogin">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { rsaEncrypt } from '../utils/encrypt'

const { proxy } = getCurrentInstance()
const router = useRouter()
const form = ref({
  username: 'admin',
  password: '123456'
})

const doLogin = async () => {
  const params = {
    username: form.value.username,
    password: rsaEncrypt(form.value.password)
  }
  const res = await proxy.$http.post('/login', params)
  localStorage.setItem('token', res.data.access)
  localStorage.setItem('refreshToken', res.data.refresh)
  localStorage.setItem('userInfo', JSON.stringify(res.data.userInfo))
  ElMessage.success('登录成功')
  router.push('/userList')
}
</script>

<style scoped>
.login-wrap{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f5f5f5;
}
</style>