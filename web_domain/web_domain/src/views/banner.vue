<template>
    <div>
        <div class="header"> 
            <lefthead></lefthead>
        </div>
        <div class="body">
            <router-view></router-view>
        </div>
    </div>
  
</template>

<script>
import lefthead from '../components/lefthead.vue'
export default {
    components:{
        lefthead
    }
}
</script>

<style>
    .body{
        margin-top: 60px;
    }
</style>