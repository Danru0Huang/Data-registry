<template>
    <div>
        <div class="head">
            <h1>
                <i class="el-icon-s-flag" style="color: #2fb9c2"></i>
                数据语义共享演示验证及数据目录协同演化组件
                <i class="el-icon-s-flag" style="color: #2fb9c2"></i>
            </h1>
            <el-dropdown @command="handleCommand" style="margin-right:20px">
                <div class="avatar-dropdown-wrapper" >
                    <img src="../img/bgi2.jpg" alt="" style="margin-right:10px">
                    <div>
                        <span class="el-dropdown-link">
                            退出<i class="el-icon-arrow-down el-icon--right"></i>
                        </span>
                    </div>
                    
                </div>
                <el-dropdown-menu slot="dropdown" >
                    <el-dropdown-item command="back">退出登录</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
        <el-col :span="12">
            <el-menu 
            :default-active="activeMenu"
            class="el-menu-vertical-demo" 
            background-color="#f0f0f0"
            text-color="black"
            active-text-color="#2fb9c2"
            :router='true'
            style="width: 250px; position: fixed; height: 100vh; left: 0; top: 0; padding-top: 60px; ">
                <el-menu-item index="/Demonstration/header2">
                    <i class="el-icon-house"></i>
                    <span slot="title">首页</span>
                </el-menu-item>

                <el-menu-item index="/Demonstration/Data_Sharing">
                    <i class="el-icon-message"></i>
                    <span slot="title">数据共享</span>
                </el-menu-item>

                <el-menu-item index="/Demonstration/Co_evolution">
                    <i class="el-icon-s-finance"></i>
                    <span slot="title">协同演化</span>
                </el-menu-item>
                <!-- <el-submenu index="2">
                    <template slot="title">
                        <i class="el-icon-location"></i>
                        <span>协同演化</span>
                    </template>
                    <el-menu-item-group>
                        <el-menu-item index="/head/MDRregister">共享域数据目录注册</el-menu-item>
                        <el-menu-item index="/head/MDRsearch">共享域数据目录查询</el-menu-item>
                    </el-menu-item-group>
                </el-submenu> -->

                
            </el-menu>
        </el-col>
    </div>
</template>

<script>
export default {
    data(){
        return{
            activeMenu: this.$route.path,
        }
    },
    watch:{
        '$router'(to,from){
            this.defaultPage = to.path;
        }
    },
    methods: {
        back(){
            this.$router.replace({name:'hello'})
        },
        handleCommand(command) {
        //this.$message('click on item ' + command);
        if(command === "back")
            this.back();
        },
    },
}
</script>

<style>
.head {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 4px;
    border-bottom: 1px solid #eee;
    z-index: 1000; /* 设置一个较大的 z-index，确保头部在上层 */
    background-color: #fff;
   
}
h1{
    color: #2fb9c2; 
    margin: 0 auto;
}
.avatar-dropdown-wrapper {
    display: flex;
    align-items: center;
    justify-content: right; 
    height: 70px;
    
    
}
img{
    width: 40px;
    height: 40px;
    border-radius: 50%;
}
</style>