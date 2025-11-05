// 该文件专门用于创建整个应用的路由器
import VueRouter from 'vue-router'
//首页
import index from "../views/index"
//导入主界面
import banner from '../views/banner'
//导入信息模型组件
import register from '../views/information_model/register'
import search from '../views/information_model/search'
//导入MDR组件
import MDRregister from '../views/MDR/MDRregister.vue'
import MDRsearch from '../views/MDR/MDRsearch.vue'
//导入第二个首页
import index2 from '../views/index2/index2'
//导入子域查询
import register_subDomain from '../views/subDomain/register_subDomain'
import search_subDomain from '../views/subDomain/search_subDommain.vue'
// 引入演化界面
import Data_evolution from '../views/Data_evolution/Data_evolution'

// 引入系统演示界面组件
import Demonstration from '../views/Demonstration_Banner'
import Data_Sharing from '../views/Demonstration/Data_Sharing'
// import Demonstration_graph from '../components/Demonstration_components/Demonstration_graph.vue'
import Co_evolution from '../views/Demonstration/Co_evolution'
import header2 from '../views/Demonstration/header2'


//创建一个路由器
const router = new VueRouter({
    routes:[
       {
        name:'hello',
        path:'/',
        component:index,
        meta: { title: '首页' } // 设置默认标题
       },
       {
        path:'/head',
        component:banner,
        children:[
          {
            path:'information_model_register',
            component:register,
            meta: { title: '信息模型注册' }, 
          },
          {
            path:'information_model_search',
            component:search,
            meta:{title: '信息模型查询'}
          },
          {
            path:'MDRregister',
            component:MDRregister,
            meta:{title:'MDR注册'}
          },
          {
            path:'MDRsearch',
            component:MDRsearch,
            meta:{title:'MDR查询'}
          },
          {
            path:'index2',
            component:index2,
            meta:{title: '首页'}
          },
          {
            path:'register_subDomain',
            component:register_subDomain,
            meta:{title:'子域查询'}
          },
          {
            path:'search_subDomain',
            component:search_subDomain,
            meta:{title:'子域注册'}
          },
          {
            path: 'Data_evolution',
            component:Data_evolution,
            meta:{title:'数据演化'}
          }
        ]
       },
       {
        path:'/Demonstration', 
        component:Demonstration,
        meta: { title: '首页' },
        children:[
                {
                  path:'header2',
                  component:header2,
                  meta: { title: '首页' },
                },
                {
                  path:'Data_Sharing',
                  component:Data_Sharing,
                  meta: { title: '数据共享' },
                },
                {
                  path:'Co_evolution',
                  component:Co_evolution,
                  meta:{title: '协同演化'},
                },
                // {
                //   path:'Demonstration_graph',
                //   component:Demonstration_graph,
                //   meta:{title:'详细查询信息'}
                // }
          ]
       }
    ]
})
// 导航守卫，用于监听路由变化
router.beforeEach((to, from, next) => {
    document.title = to.meta.title || '默认标题'; // 在每次切换路由后更改网页标题
    next();
  });

//暴露路由器
export default router