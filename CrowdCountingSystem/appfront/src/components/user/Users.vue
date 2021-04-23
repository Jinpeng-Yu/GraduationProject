<template>
    <div>
      <!-- 面包屑导航区 -->
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>人员管理</el-breadcrumb-item>
        <el-breadcrumb-item>员工列表</el-breadcrumb-item>
      </el-breadcrumb>
      <!-- 卡片视图 -->
      <el-card>
        <!-- 搜索 添加 -->
        <el-row :gutter="20">
          <el-col :span="7">
            <el-input placeholder="请输入内容" v-model="queryInfo.query" clearable @clear="getUserList">
              <el-button slot="append" icon="el-icon-search" @click="getUserList"></el-button>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="addDialogVisible = true">添加用户</el-button>
          </el-col>
        </el-row>
        <!-- 用户列表区域 -->
        <el-table :data="userlist" border stripe>
          <!-- stripe: 斑马条纹
          border：边框-->
          <el-table-column type="index" label="#"></el-table-column>
          <el-table-column prop="fields.mg_name" label="姓名"></el-table-column>
          <el-table-column prop="fields.email" label="邮箱"></el-table-column>
          <el-table-column prop="fields.mobile" label="电话"></el-table-column>
          <el-table-column prop="fields.add_time" label="添加日期" :formatter="dateFormat"></el-table-column>
          <el-table-column label="状态">
            <template slot-scope="scope">
              <el-switch v-model="scope.row.fields.mg_state" @change="userStateChanged(scope.row)"></el-switch>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                circle
                @click="showEditDialog(scope.row.pk)"
              ></el-button>
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                circle
                @click="removeUserById(scope.row.pk)"
              ></el-button>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页区域 -->
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.pagenum"
          :page-sizes="[2, 5, 10, 15]"
          :page-size="queryInfo.pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        ></el-pagination>
      </el-card>

      <!-- 添加用户的对话框 -->
      <el-dialog title="添加用户" :visible.sync="addDialogVisible" width="50%" @close="addDialogClosed">
        <!-- 内容主体 -->
        <el-form
          :model="addUserForm"
          ref="addUserFormRef"
          :rules="addUserFormRules"
          label-width="100px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="addUserForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="addUserForm.password"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="addUserForm.email"></el-input>
          </el-form-item>
          <el-form-item label="手机" prop="mobile">
            <el-input v-model="addUserForm.mobile"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addUser">确 定</el-button>
      </span>
      </el-dialog>

      <!-- 修改用户的对话框 -->
      <el-dialog
        title="修改用户信息"
        :visible.sync="editDialogVisible"
        width="50%"
        @close="editDialogClosed"
      >
        <!-- 内容主体 -->
        <el-form
          :model="editUserForm"
          ref="editUserFormRef"
          :rules="editUserFormRules"
          label-width="70px"
        >
          <el-form-item label="用户名">
            <el-input v-model="editUserForm.mg_name" disabled></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="editUserForm.email"></el-input>
          </el-form-item>
          <el-form-item label="手机" prop="mobile">
            <el-input v-model="editUserForm.mobile"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editUser">确 定</el-button>
      </span>
      </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "Users",
      data () {
        // 自定义邮箱规则
        var checkEmail = (rule, value, callback) => {
          const regEmail = /^\w+@\w+(\.\w+)+$/
          if (regEmail.test(value)) {
            // 合法邮箱
            return callback()
          }
          callback(new Error('请输入合法邮箱'))
        }
        // 自定义手机号规则
        var checkMobile = (rule, value, callback) => {
          const regMobile = /^1[34578]\d{9}$/
          if (regMobile.test(value)) {
            return callback()
          }
          // 返回一个错误提示
          callback(new Error('请输入合法的手机号码'))
        }
        return {
          // 获取用户列表查询参数对象
          queryInfo: {
            query: '',
            // 当前页数
            pagenum: 1,
            // 每页显示多少数据
            pagesize: 5
          },
          userlist: [],
          total: 0,
          // 添加用户对话框
          addDialogVisible: false,
          // 用户添加
          addUserForm: {
            username: '',
            password: '',
            email: '',
            mobile: ''
          },
          // 用户添加表单验证规则
          addUserFormRules: {
            username: [
              { required: true, message: '请输入用户名', trigger: 'blur' },
              {
                min: 2,
                max: 10,
                message: '用户名的长度在2～10个字',
                trigger: 'blur'
              }
            ],
            password: [
              { required: true, message: '请输入用户密码', trigger: 'blur' },
              {
                min: 6,
                max: 18,
                message: '用户密码的长度在6～18个字',
                trigger: 'blur'
              }
            ],
            email: [
              { required: true, message: '请输入邮箱', trigger: 'blur' },
              { validator: checkEmail, trigger: 'blur' }
            ],
            mobile: [
              { required: true, message: '请输入手机号码', trigger: 'blur' },
              { validator: checkMobile, trigger: 'blur' }
            ]
          },
          // 修改用户
          editDialogVisible: false,
          editUserForm: {},
          // 编辑用户表单验证
          editUserFormRules: {
            email: [
              { required: true, message: '请输入邮箱', trigger: 'blur' },
              { validator: checkEmail, trigger: 'blur' }
            ],
            mobile: [
              { required: true, message: '请输入手机号码', trigger: 'blur' },
              { validator: checkMobile, trigger: 'blur' }
            ]
          },
          // 分配角色对话框
          setRoleDialogVisible: false,
          // 当前需要被分配角色的用户
          userInfo: {},
          // 所有角色数据列表
          rolesLsit: [],
          // 已选中的角色Id值
          selectRoleId: ''
        }
      },
      created () {
        this.getUserList()
      },
      methods: {
        async getUserList () {
          const { data: res } = await this.$http.get('show_managers', {
            params: this.queryInfo
          })
          if (res.error_num !== 0) {
            return this.$message.error('获取用户列表失败！')
          }
          this.userlist = res.managers
          this.total = res.total
        },
        dateFormat(row, column){
          // console.log(row.fields.add_time)
          return row.fields.add_time.replace(/T/g,' ').replace(/\.[\d]{3}/g,'')
        },
        // 监听 pagesize改变的事件
        handleSizeChange (newSize) {
          // console.log(newSize)
          this.queryInfo.pagesize = newSize
          this.getUserList()
        },
        // 监听 页码值 改变事件
        handleCurrentChange (newSize) {
          // console.log(newSize)
          this.queryInfo.pagenum = newSize
          this.getUserList()
        },
        // 监听 switch开关 状态改变
        async userStateChanged (userInfo) {
          // console.log(userInfo)
          const { data: res } = await this.$http.get(
            'update_manager_state', {params:{userid:userInfo.pk}}
          )
          if (res.error_num !== 0) {
            userInfo.mg_state = !userInfo.mg_state
            return this.$message.error('更新用户状态失败')
          }
          this.$message.success('更新用户状态成功！')
        },
        // 监听 添加用户对话框的关闭事件
        addDialogClosed () {
          this.$refs.addUserFormRef.resetFields()
        },
        // 添加用户
        addUser () {
          // 提交请求前，表单预验证
          this.$refs.addUserFormRef.validate(async valid => {
            // console.log(valid)
            // 表单预校验失败
            if (!valid) return
            const { data: res } = await this.$http.get('add_manager', {params:this.addUserForm})
            if (res.error_num !== 1) {
              this.$message.error('添加用户失败！')
            }
            this.$message.success('添加用户成功！')
            // 隐藏添加用户对话框
            this.addDialogVisible = false
            this.getUserList()
          })
        },
        // 编辑用户信息
        async showEditDialog (id) {
          const { data: res } = await this.$http.get('get_user_by_id' , {params: { userid : id} })
          if (res.error_num !== 0) {
            return this.$message.error('查询用户信息失败！')
          }
          this.editUserForm = res.manager[0].fields
          this.selectRoleId = res.manager[0].pk
          this.editDialogVisible = true
        },
        // 监听修改用户对话框的关闭事件
        editDialogClosed () {
          this.$refs.editUserFormRef.resetFields()
        },
        // 修改用户信息
        editUser () {
          // 提交请求前，表单预验证
          this.$refs.editUserFormRef.validate(async valid => {
            // console.log(valid)
            // 表单预校验失败
            if (!valid) return
            const { data: res } = await this.$http.get(
              'update_manager',
              { params : {userid: this.selectRoleId, email: this.editUserForm.email, mobile: this.editUserForm.mobile}}
            )
            if (res.error_num !== 0) {
              this.$message.error('更新用户信息失败！')
            }
            // 隐藏添加用户对话框
            this.editDialogVisible = false
            this.$message.success('更新用户信息成功！')
            this.getUserList()
          })
        },
        // 删除用户
        async removeUserById (id) {
          const confirmResult = await this.$confirm(
            '此操作将永久删除该用户, 是否继续?',
            '提示',
            {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }
          ).catch(err => err)
          // 点击确定 返回值为：confirm
          // 点击取消 返回值为： cancel
          if (confirmResult !== 'confirm') {
            return this.$message.info('已取消删除')
          }
          const { data: res } = await this.$http.get('delete_manager', {params:{userid : id}})
          if (res.error_num !== 0) return this.$message.error('删除用户失败！')
          this.$message.success('删除用户成功！')
          this.getUserList()
        },
      }
    }
</script>

<style scoped lang="less">

</style>
