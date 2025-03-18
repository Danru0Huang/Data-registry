<template>
  <div class="box">
      <div class="box_search" v-show="show_search">
          <Demonstration_search @send-data="handleData" ></Demonstration_search>
      </div>
      <div class="box_graph" v-if="show_graph">
          <Demonstration_graph :parentData1="parentData1" :parentData2="parentData2" @backsearch="backshow_search" @send-data2="handleData2"></Demonstration_graph>
      </div>
      <div class="box_graph2" v-if="show_graph2">
          <Demonstration_graph2 :parentData3="parentData3" @backsearch="backshow_search"></Demonstration_graph2>
      </div>
  </div>
</template>

<script>
import Demonstration_search from '../../components/Demonstration_components/Co_evolution_search.vue'
import Demonstration_graph from '../../components/Demonstration_components/Co_evolution_graph.vue'
import Demonstration_graph2 from '../../components/Demonstration_components/Co_evolution_graph2.vue'
export default {
  components:{
    Demonstration_search,
    Demonstration_graph,
    Demonstration_graph2,
  },
  data(){
      return{
          receivedData: '',
          show_search:true,
          show_graph:false,
          show_graph2:false,
          parentData1:'',
          parentData2:'',
          parentData3:'',
      }
  },
  methods:{
      handleData(data) {
        //   console.log('接收到的数据：', data);
          this.receivedData = data;
          this.parentData1 = data.name;
          this.parentData2 = 'subDomain'
          if(this.parentData1==undefined)
          {
              this.parentData1 = data.model_name;
              this.parentData2 = 'model'
          }
          this.show_search = false;
          this.show_graph = true;
          this.show_graph2 = false;
      },
      handleData2(nodeidentifier){
            console.log('接收到的数据2：', nodeidentifier);
            this.parentData3 = nodeidentifier;
            // if(this.parentData=='undefine')
            // {
            //     this.parentData = data.model_name;
            // }
            // console.log(this.parentData);
            this.show_search = false;
            this.show_graph = false;
            this.show_graph2 = true;
        },
      backshow_search(){
          this.show_graph = false;
          this.show_search = true;
          this.show_graph2 = false;
      },  
  }
}
</script>

<style scoped>
/* .box{
  width: 100vw;
  height: 100vh;
  background-color: skyblue;
} */
</style>