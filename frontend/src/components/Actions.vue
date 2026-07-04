<template>
  <div class="user-page">
    <!-- 顶部操作按钮 -->
    <div class="toolbar">
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
import { ref, getCurrentInstance } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
const { proxy } = getCurrentInstance()

const failDialogVisible = ref(false)
const failList = ref([])

// ==========================================
// 1. 下载导入模板
// ==========================================
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

const getList = async () => {
  const res = await proxy.$http.get('/user')
  tableData.value = res.data.results
}

// ==========================================
// 2. 导出用户数据
// ==========================================
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

// ==========================================
// 3. 批量导入用户
// ==========================================
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

// ==========================================
// 工具：下载文件公共方法
// ==========================================
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
</script>

<style scoped>
.toolbar {
  margin-bottom: 15px;
}
</style>