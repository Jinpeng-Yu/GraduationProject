<template>
  <div class="login_container">
    <div class="login_box">
      <div class="avatar_box">
        <img src="../assets/monitor.png" alt="">
      </div>
      <el-form ref="loginFormRef"
               :model="loginForm"
               :rules="loginFormRules"
               label-width="60px" class="login_form">
<!--        用户名-->
        <el-form-item label="账号" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
<!--        密码-->
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
<!--        按钮-->
        <el-form-item class="buttons">
          <el-button type="primary" @click="login">登录</el-button>
          <el-button type="info" @click="resetLoginForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
    export default {
      data () {
        return {
          loginForm: {
            username: '',
            password: ''
          },
          // 表单验证
          loginFormRules: {
            username: [
              { required: true, message: '请输入用户名', trigger: 'blur' },
              { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
            ],
            password: [
              { required: true, message: '请输入用户密码', trigger: 'blur' },
              { min: 6, max: 18, message: '长度在 6 到 18 个字符', trigger: 'blur' }
            ]
          }
        }
      },
      methods: {
        // 表单重置按钮
        resetLoginForm () {
          // console.log(this)
          // resetFields：element-ui提供的表单方法
          this.$refs.loginFormRef.resetFields()
        },
        login () {
          // 表单预验证
          // valid：bool类型
          this.$refs.loginFormRef.validate(async valid => {
            // console.log(valid)
            if (!valid) return false
            // this.$http.post('login', this.loginForm): 返回值为promise
            // 返回值为promise，可加await简化操作 相应的也要加async
            const { data: res } = await this.$http.get('login', {params:this.loginForm})
            // console.log(res)
            if (res.error_num !== 0) return this.$message.error('登录失败')
            this.$message.success('登录成功')
            // 1、将登陆成功之后的token, 保存到客户端的sessionStorage中; localStorage中是持久化的保存
            //   1.1 项目中出现了登录之外的其他API接口，必须在登陆之后才能访问
            //   1.2 token 只应在当前网站打开期间生效，所以将token保存在sessionStorage中
            // window.sessionStorage.setItem('token', res.data.token)
            // 2、通过编程式导航跳转到后台主页, 路由地址为：/home
            this.$router.push('/home')
          })
        }
      },
      name: "Login"
    }
</script>

<style scoped>
.login_container {
  /*background-color: #2b4b6b;*/
  background-image: url("../assets/background.png");
  background-size: cover;
  height: 100%;
}
.login_box {
  width: 450px;
  height: 300px;
  background-color: #fff;
  border-radius: 3px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.avatar_box {
  height: 130px;
  width: 130px;
  border: 1px solid #eee;
  border-radius:50%;
  padding:10px;
  box-shadow: 0 0 10px #ddd;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #ffffff;
}
img {
  width: 100%;
  height: 100%;
  border-radius:50%;
  background-color: #eeeeee;
}
.login_form {
  position: absolute;
  bottom: 10px;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.buttons {
  display: flex;
  justify-content: center;
}
</style>
