<template>
  <el-container>
    <!-- 头部 -->
    <el-header>
      <div>
        <img src="../assets/monitor.png" alt />
        <span>人流密度监控系统</span>
      </div>
      <el-button type="info" @click="logout">退出</el-button>
    </el-header>
    <!-- 主体 -->
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <div class="toggle-button" @click="togleCollapse">|||</div>
        <el-menu unique-opened :collapse="isCollapse" :collapse-transition="false" router :default-active="activePath" background-color="#333744" text-color="#fff" active-text-color="#409FFF">
          <!-- :unique-opened="true"->只允许展开一个菜单 -->
          <!-- :collapse-transition="false" -> 关闭动画 -->
          <!-- router -> 导航开启路由模式 -->
          <!-- 一级菜单  -->
          <el-submenu :index="item.id+''" v-for="item in menuList" :key="item.id" >
            <!-- 一级菜单的模板区域 -->
            <template slot="title">
              <i :class="iconObj[item.id]"></i>
              <span>{{ item.authName}}</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item :index="'/' + subItem.path" v-for="subItem in item.children" :key="subItem.id" @click="saveNavState('/' + subItem.path)">
              <!-- 导航开启路由模式：
                将index值作为导航路由 -->
              <!-- 二级菜单的模板区域 -->
              <template slot="title">
                <i :class="iconObj[subItem.id]"></i>
                <span>{{ subItem.authName}}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <!-- 内容主体 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
    export default {
        name: "Home",
      data() {
          return {
            // 左侧菜单数据
            menuList: [
              {
                id: 101,
                authName: "人员管理",
                children:[
                  {
                    id: 110,
                    authName: "员工列表",
                    path: "users",
                  },
                ]
              },
              {
                id: 102,
                authName: "数据分析",
                children:[
                  {
                    id: 120,
                    authName: "视频分析",
                    path: "videos",
                  }
                ]
              },
              {
                id: 103,
                authName: "数据展示",
                children:[
                  {
                    id: 130,
                    authName: "人流变化",
                    path: "trends",
                  },
                  {
                    id: 131,
                    authName: "数据统计",
                    path: "report",
                  },
                ]
              },
            ],
            iconObj: {
              '101': 'el-icon-s-custom',
              '102': 'el-icon-s-data',
              '103': 'el-icon-s-platform',
              '110': 'el-icon-s-management',
              '120': 'el-icon-video-camera-solid',
              '130': 'el-icon-s-marketing',
              '131': 'el-icon-s-help',
            },
            // 默认不折叠
            isCollapse: false,
            // 被激活导航地址
            activePath: '/welcome',
          }
      },
      created () {
        this.activePath = window.sessionStorage.getItem('activePath')
      },
      methods: {
          logout(){
            this.$router.push('/login')
            window.sessionStorage.setItem('activePath', '/welcome')
            window.sessionStorage.setItem('video_name', '')
          },
        // 菜单的折叠与展开
        togleCollapse () {
          this.isCollapse = !this.isCollapse
        },
        // 保存连接的激活地址
        saveNavState (activePath) {
          window.sessionStorage.setItem('activePath', activePath)
          this.activePath = activePath
        }
      }
    }
</script>

<style scoped lang="less">
  .el-container {
    height: 100%;
  }
  .el-header {
    background-color: #373f41;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: #fff;
    font-size: 20px;
      > div {
        display: flex;
        align-items: center;
        img {
          height: 40px;
        }
        span {
          margin-left: 15px;
        }
      }
  }
  .el-aside {
    background-color: #333744;

    .el-menu {
      border: none;
    }
  }
  .el-main {
    background-color: #eaedf1;
  }
  .iconfont{
    margin-right: 10px;
  }
  .toggle-button {
    background-color: #4A5064;
    font-size: 10px;
    line-height: 24px;
    color: #fff;
    text-align: center;
    letter-spacing: 0.2em;
    // 鼠标放上去变成小手
    cursor: pointer;
  }
</style>
