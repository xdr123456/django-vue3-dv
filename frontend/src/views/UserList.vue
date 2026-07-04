<template>
  <div style="padding:20px">
    <div style="display: flex; justify-content: space-between;">
      <div>
        <el-button type="primary" @click="openDialog">新增用户</el-button>
        <el-button type="info" @click="downloadTemplate">下载导入模板</el-button>
          
        <el-upload
          action=""
          :http-request="handleImport"
          accept=".xlsx,.xls"
          :show-file-list="false"
          style="display: inline-block; margin-left: 10px"
        >
          <el-button type="primary">批量导入用户</el-button>
        </el-upload>

        <el-button type="success" @click="handleExport" style="margin-left: 10px">
          导出用户数据
        </el-button>
      </div>
      
      <el-button type="primary" @click="handleLogout" style="margin-left: 10px">
        退出登录
      </el-button>
    </div>

    <el-table :data="tableData" border style="margin-top:20px">
      <el-table-column prop="username" label="账号"/>
      <el-table-column prop="nickname" label="昵称"/>
      <el-table-column prop="age" label="年龄"/>
      <el-table-column label="状态">
        <template #default="scope">
          <el-tag :type="scope.row.status?'success':'danger'">
            {{scope.row.status?'正常':'禁用'}}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="editRow(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="delRow(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 弹窗 -->
    <el-dialog v-model="dialogVisible" title="用户信息">
      <el-form :model="form">
        <el-form-item label="账号">
          <el-input v-model="form.username" :disabled="isEdit"></el-input>
        </el-form-item>
        <el-form-item label="密码" v-if="!isEdit">
          <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname"></el-input>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model.number="form.age"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>


    <!-- 导入失败明细弹窗 -->
    <el-dialog v-model="failDialogVisible" title="导入失败明细" width="500px">
      <el-alert
        :title="`共失败 ${failList.length} 条`"
        type="warning"
        :closable="false"
        style="margin-bottom: 15px"
      />
      <div style="max-height: 300px; overflow-y: auto">
        <div
          v-for="(item, index) in failList"
          :key="index"
          style="padding: 6px 0; border-bottom: 1px solid #eee; color: #f56c6c"
        >
          {{ item }}
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const { proxy } = getCurrentInstance()
const router = useRouter()
const tableData = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const failDialogVisible = ref(false)
const failList = ref([])
const form = ref({
  id: null,
  username: '',
  password: '',
  nickname: '',
  age: null,
  status: true
})

// 获取列表
const getList = async () => {
  const res = await proxy.$http.get('/user')
  tableData.value = res.data.results
}

// 退出登录
const handleLogout = async () => {
  // await proxy.$http.post('/logout')
  localStorage.removeItem('token')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('userInfo')
  ElMessage.success('退出登录成功')
  router.push('/login')
}



// 新增
const openDialog = () => {
  isEdit.value = false
  form.value = {username:'',password:'',nickname:'',age:null,status:true}
  dialogVisible.value = true
}

// 编辑
const editRow = (row) => {
  isEdit.value = true
  form.value = {...row}
  dialogVisible.value = true
}

// 提交
const submitForm = async () => {
  if(isEdit.value){
    await proxy.$http.put(`/user/${form.value.id}`, form.value)
  }else{
    await proxy.$http.post('/user', form.value)
  }
  dialogVisible.value = false
  ElMessage.success('操作成功')
  getList()
}

// 删除
const delRow = (id) => {
  ElMessageBox.confirm('确定删除?').then(async ()=>{
    await proxy.$http.delete(`/user/${id}`)
    ElMessage.success('删除成功')
    getList()
  })
}

// 下载导入模板
const downloadTemplate = async () => {
  try {
    const res = await proxy.$http.get('/user/template', {
      responseType: 'blob'
    })
    downloadFile(res, '用户导入模板.xlsx')
    ElMessage.success('模板下载成功')
  } catch (e) {
    ElMessage.error('模板下载失败')
  }
}

// 导出用户数据
const handleExport = async () => {
  try {
    const res = await proxy.$http.get('/user/export', {
      responseType: 'blob'
    })
    downloadFile(res, '用户列表数据.xlsx')
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error('导出失败')
  }
}

// 导入用户数据
const handleImport = async (params) => {
  const formData = new FormData()
  formData.append('file', params.file)

  try {
    const res = await proxy.$http.post('/user/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (res.code === 200) {
      ElMessage.success(res.msg)
      // 导入后刷新列表
      getList()
      // 有失败明细就弹出来
      if (res.data && res.data.length > 0) {
        failList.value = res.data
        failDialogVisible.value = true
      }
    } else {
      ElMessage.error(res.msg)
    }
  } catch (e) {
    ElMessage.error('导入失败，请重试')
  }
}

// 下载文件公共方法
const downloadFile = (blobData, fileName) => {
  const blob = new Blob([blobData], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = fileName
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(()=>{
  getList()
})
</script>