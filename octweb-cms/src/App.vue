<template>
  <div class="frame">
    <el-container class="frame-container">
      <el-header class="header">
        <a href="/" class="brand"><strong>灵眸健康</strong>管理系统</a>
        <div class="header-content">
          <div class="greet">欢迎，{{$auth.user.username}}</div>
          <div class="signout">回到首页</div>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="aside">
          <el-row class="menu-row">
            <el-col :span="24">
              <el-menu
                default-active="1"
                background-color="#545c64"
                active-text-color="#fff"
                text-color="#ddd"
                :router="true"
              >
                <el-menu-item index="1" :route="{name: 'home'}">
                  <template #title>
                    <el-icon><House /></el-icon>
                    <span>首页</span>
                  </template>
                </el-menu-item>

                <el-menu-item index="2" :route="{name: 'banner'}">
                  <template #title>
                    <el-icon><PictureRounded /></el-icon>
                    <span>轮播图</span>
                  </template>
                </el-menu-item>

                <el-menu-item index="3" :route="{name: 'post'}">
                  <template #title>
                    <el-icon><Postcard /></el-icon>
                    <span>帖子管理</span>
                  </template>
                </el-menu-item>

                <el-menu-item index="4" :route="{name: 'comment'}">
                  <template #title>
                    <el-icon><Comment /></el-icon>
                    <span>评论管理</span>
                  </template>
                </el-menu-item>

                <el-menu-item index="5" :route="{name: 'user'}">
                  <template #title>
                    <el-icon><User /></el-icon>
                    <span>用户管理</span>
                  </template>
                </el-menu-item>
              </el-menu>
            </el-col>
          </el-row>
        </el-aside>
        <el-container>
          <el-main class="main">
            <router-view></router-view>
          </el-main>
          <el-footer class="footer"></el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "App",
  
  mounted() {
  if(!this.$auth.is_staff){
    window.location = "http://localhost:5000/"
  }
}
};


</script>

<style scoped>
.frame-container {
  height: 100vh;
}
.header {
  height: 60px;
  background: #006fa6;
  display: flex;
}

.header .brand {
  width: 200px;
  margin-left: -20px;
  background-color: #00508d;
  font-size: 20px;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
}
.header .header-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-left: 20px;
  color: #fff;
}

.header-content .signout {
    cursor: pointer;
  }

.aside {
  background-color: #545c64;
}

.aside .el-menu .is-active {
  background-color: #434a50 !important;
}

.footer {
  background: white;
}
</style>

<style scoped>
.el-menu{
  border-right: none;
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  border: 0;
  text-decoration: none;
  vertical-align: baseline;
}
</style>