<template>
    <div class="box">
        <div class="box_search" v-if="show_search">
            <Demonstration_search @send-data="handleData" @send-data2="handleData2"></Demonstration_search>
        </div>
        <div class="box_graph" v-if="show_graph">
            <Demonstration_graph :parentData="parentData" @backsearch="backshow_search"></Demonstration_graph>
        </div>
    </div>
</template>

<script>
import Demonstration_search from '../../components/Demonstration_components/Demonstration_search.vue'
import Demonstration_graph from '../../components/Demonstration_components/Demonstration_graph.vue'
export default {
    components:{
        Demonstration_search,
        Demonstration_graph,
    },
    data(){
        return{
            receivedData: '',
            show_search:true,
            show_graph:false,
            parentData:'',
            wdf:''
        }
    },
    mounted(){
        if(this.$route.query.identifier === undefined){
        }else{
            this.parentData = this.$route.query.identifier;
            this.wdf = this.$route.query.wdf;
            this.show_search = false;
            this.show_graph = true;
        }
    },
    methods:{
        handleData2(nodeidentifier){
            console.log('接收到的数据2：', );
            this.parentData = nodeidentifier;
            // if(this.parentData=='undefine')
            // {
            //     this.parentData = data.model_name;
            // }
            // console.log(this.parentData);
            this.show_search = false;
            this.show_graph = true;
        },
        handleData(data) {
            // console.log('接收到的数据：', data);
            this.receivedData = data;
            this.parentData = data.identifier;
            // if(this.parentData=='undefine')
            // {
            //     this.parentData = data.model_name;
            // }
            // console.log(this.parentData);
            this.show_search = false;
            this.show_graph = true;
        },
        backshow_search(){
            this.show_graph = false;
            this.show_search = true;
        }
        
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