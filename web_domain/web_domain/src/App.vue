<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { apiBaseUrl } from './config.js'; 
export default {
  name: 'App',
  
}
</script>

<style>
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
