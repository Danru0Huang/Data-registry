<template>
    <div class="index">
        <el-container style="height: 100vh;">
        <el-main>
            <el-row type="flex" justify="center" align="middle" style="height: 100%;">
                <el-col :span="18">
                    <div id="centerShow" style="margin-bottom: 40px; text-align: center;font-size: 25px;">
                        <h2 style="font-family: bold; color: #d9ecff">数据语义共享演示验证及数据目录协同演化组件</h2>
                    </div>
                    <el-button type="primary" size="large" id="search-enter-btn" @click="gobanner" style="width:150px">管理员登入</el-button>
                    <!-- // <p style="font-size: 14px;">A system based on konwledge graph</p> -->
                    <el-button type="primary" size="large" id="search-enter-btn" @click="goDemonstration_Banner" style="width:200px">用户登入</el-button>
                </el-col>
            </el-row>
        </el-main>
    </el-container>
    </div>
   
</template>

<script>
export default {
    methods:{
        goDemonstration_Banner(){
            this.$router.push({path:'/Demonstration/header2'})
            this.$message({
                showClose: true,
                message: '登入成功',
                type: 'success',
                duration: 1000
            });
        },
        gobanner(){
            this.$router.push({path:'/head/index2'})
            // 登录成功消息提示
            this.$message({
                showClose: true,
                message: '登入成功',
                type: 'success',
                duration: 1000
            });
        }
    }
}
</script>

<style scoped>
    .index{
        background-image: url('../img/bg.jpg');
        background-size: cover;
        /* background-size: 100% 100%; */
        background-position: center;
        text-align: center;
        font-family: Arial, sans-serif;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    #search-enter-btn {
        display: inline-block;
        font-weight: 500;
        text-align: center;
        white-space: nowrap;
        vertical-align: middle;
        user-select: none;
        border: .0625rem solid transparent;
        padding: .55rem 1.8rem;
        line-height: 3.0;
        border-radius: .375rem;
        border-bottom: 1px solid #0f97b9;
        box-shadow: none;
        cursor: pointer;
        font-size: 18px;
    }
</style>