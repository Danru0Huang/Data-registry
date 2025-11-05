<template>
    <div>
        <div class="header"> 
            <Demonstration></Demonstration>
        </div>
        <div class="body">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
import Demonstration from '../components/Demonstration.vue'
export default {
    components:{
        Demonstration
    }
}
</script>

<style>
    .body{
        margin-top: 60px;
    }
</style>