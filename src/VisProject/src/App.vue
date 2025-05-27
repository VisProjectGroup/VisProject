<!-- app.vue -->
<template>
  <div class="container">
    <!-- 侧边栏容器 -->
    <div class="sidebar-container">
      <!-- Element UI容器组件，高度为整个视口高度 -->
      <el-container style="height: 100vh;">
        <!-- 侧边栏区域，宽度200px -->
        <el-aside width="200px">
          <!-- 侧边栏菜单 -->
          <el-menu :default-active="activeIndex" class="el-menu-vertical-demo" @select="handleSelect"
            :collapse="isCollapse" router="false">
            <!-- 首页菜单项 -->
            <el-menu-item index="Dashboard"
              style="background-color:rgb(77, 79, 82) ;color: aliceblue;">首页</el-menu-item>
            <!-- 一级菜单，使用v-for指令循环渲染 -->
            <el-sub-menu v-for="item in ChartData" :key="item.id" :index="item.id">
              <template #title>
                <!-- 菜单标题 -->
                <span>{{ item.functionName }}</span>
              </template>
              <!-- 二级菜单，循环渲染子菜单项 -->
              <el-menu-item v-for="subItem in item.children" :key="subItem.id" :index="subItem.id" >
                {{ subItem.functionName }}
              </el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-aside>
        <!-- 主内容区域 -->
        <el-main>
          <!-- 路由视图，根据当前路由动态渲染组件 -->
          <router-view></router-view>
        </el-main>
      </el-container>
      <!-- 折叠按钮，点击切换侧边栏展开/折叠状态 -->
      <div class="collapse-button" @click="toggleCollapse">
        <i :class="isCollapse ? 'el-icon-arrow-right' : 'el-icon-arrow-left'"></i>
      </div>
    </div>
    <div class="map-area">
      <!-- 使用地图组件并监听点击事件 -->
      <MapComponent @CityClick="handleCityClick" />
    </div>
    <!-- 右侧面板：显示选中的省份 -->
    <div class="polar-area" v-if="columAQIshow">
      <ChartComponent :CityName="selectedCity" />
    </div>
    
    <div class="polar-area" v-if="roseAQIrainshow">
      <PolarAQIRainComponent :CityName="selectedCity"/>
    </div>
    <div class="polar-area" v-if="roseAQIwindshow">
      <PolarAQIWindComponent :CityName="selectedCity"/>
    </div>
    <div class="right-panel"v-if="parallelmonthshow">
      <ParallelMonthlyComponent :CityName="selectedCity"/>
    </div>
    <div class="right-panel"v-if="parallelyearshow">
      <ParallelYearlyComponent :CityName="selectedCity"/>
    </div>
  </div>
</template>

<script setup>
// 导入Element UI组件和Vue的ref函数
import { ElContainer, ElAside, ElMenu, ElSubMenu, ElMenuItem, ElMenuItemGroup } from 'element-plus';
import { ref } from 'vue';
import MapComponent from './components/Map.vue'; // 引入地图组件
import ChartComponent from './components/charts.vue'; // 引入图表组件
import PolarAQIRainComponent from './components/polar_aqi_rain.vue';
import PolarAQIWindComponent from './components/polar_aqi_wind.vue';
import ParallelMonthlyComponent from './components/parralel_monthly.vue';
import ParallelYearlyComponent from './components/parralel_yearly.vue';
import { active } from 'd3';

const selectedCity = ref('');

const handleCityClick = (CityName) => {
  selectedCity.value = CityName;
};


  const ChartData =[ // 储存侧边栏需要的图表类型
  {
    id : 1,
    functionName: "柱状图",
    children : [
      {
        id : 11,
        functionName : "AQI"
      },
      {
        id : 12,
        functionName : "降水",
      },
      {
        id : 13,
        functionName : "风速"
      },
      {
        id : 14,
        functionName : "工业产值"
      }
    ]
  },
  {
    id : 2,
    functionName: "折线图",
    children : [
      {
        id : 21,
        functionName : "折线图"
      }
    ]
  },
  {
    id : 3,
    functionName: "气泡图",
    children : [
      {
        id : 31,
        functionName : "气泡图"
      }
    ]
  },
  {
    id : 4,
    functionName: "玫瑰图",
    children : [
      {
        id : 41,
        functionName : "雨量-空气质量玫瑰图"
      },
      {
        id : 42,
        functionName : "风力-空气质量玫瑰图"
      },
      {
        id : 43,
        functionName : "工业产值-空气质量玫瑰图",
      }

    ]
  },
  {
    id : 5,
    functionName: "热力图",
    children : [
      {
        id : 51,
        functionName : "热力图",
      }
    ]
  },
  {
    id : 6,
    functionName: "平行坐标图",
    children : [
      {
        id : 61,
        functionName : "月平行坐标图"
      },
      {
        id : 62,
        functionName : "年平行坐标图"
      }
    ]
  }
];


</script>

<script>



export default {
  data() {
    // 从localStorage中获取用户信息
    // 如果存在用户信息，则返回数据对象
    
      return {
        columAQIshow: true, // AQI 柱状图是否显示
        columRainshow: false, // 降水 柱状图是否显示
        columWindshow: false, // 风速 柱状图是否显示
        columFactoryshow: false, // 工业产值 柱状图是否显示

        roseAQIrainshow: false, // 雨玫瑰图是否显示
        roseAQIwindshow: false, // 风玫瑰图是否显示
        roseFactoryshow: false, // 工业产值玫瑰图是否显示

        lineshow: false, // 折线图是否显示
        bubbleshow: false, // 气泡图是否显示
        heatmapshow: false, // 热力图是否显示

        parallelmonthshow : false, // 平行坐标图是否显示
        parallelyearshow : false, // 平行坐标图是否显示

        activeIndex: 11, // 当前激活的菜单项    过会用来选表
        isCollapse: false // 侧边栏是否折叠
      }
    
  },
  components: {
    // 注册Element UI组件
    ElContainer,
    ElAside,
    ElMenu,
    ElSubMenu,
    ElMenuItem,
    ElMenuItemGroup
  },
  watch:{
  activeIndex(newval, oldval){
    if(newval === 11){
      this.columAQIshow = true;
    }
    if(newval === 12){
      this.columRainshow = true;
    }
    if(newval === 13){
      this.columWindshow = true;
    }
    if(newval === 14){
      this.columFactoryshow = true;
    }
    if(newval === 41){
      this.roseAQIrainshow = true;
    }
    if(newval === 42){
      this.roseAQIwindshow = true;
    }
    if(newval === 43){
      this.roseFactoryshow = true;
    }
    if(newval === 21){
      this.lineshow = true;
    }
    if(newval === 31){
      this.bubbleshow = true;
    }
    if(newval === 51){
      this.heatmapshow = true;
    }
    if(newval === 61){
      this.parallelmonthshow = true;
    }
    if(newval === 62){
      this.parallelyearshow = true;
    }
    if(oldval === 11){
      this.columAQIshow = false;
    }
    if(oldval === 12){
      this.columRainshow = false;
    }
    if(oldval === 13){
      this.columWindshow = false;
    }
    if(oldval === 14){
      this.columFactoryshow = false;
    }
    if(oldval === 41){
      this.roseAQIrainshow = false;
    }
    if(oldval === 42){
      this.roseAQIwindshow = false;
    }
    if(oldval === 43){
      this.roseFactoryshow = false;
    }
    if(oldval === 21){
      this.lineshow = false;
    }
    if(oldval === 31){
      this.bubbleshow = false;
    }
    if(oldval === 51){
      this.heatmapshow = false;
    }
    if(oldval === 61){
      this.parallelmonthshow = false;
    }
    if(oldval === 62){
      this.parallelyearshow = false;
    }
  }
},
  methods: {
    // 菜单展开回调
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    // 菜单关闭回调
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    // 菜单项选择回调
    handleSelect(key, keyPath) {

      this.activeIndex = key;
      
    },
    // 切换侧边栏折叠状态
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    },

  }


}  

</script>

<style>
.container {
  display: flex;
  gap: 20px;
  padding: 20px;
}
.right-panel {
  border: 1px solid #e5e7eb;
  padding: 15px;
  border-radius: 4px;
}

/* 地图组件样式 */

.map-area { 
  width: 50%;
  background-color: #e8e8f0;
  padding: 20px;
}

/* 图表组件样式 */

.chart-area {
  width: 50%;
  background-color: #f5f5f5;
  padding: 20px;
}

.polar-area {
  width: 80%;
  background-color: #f5f5f5;
  padding: 20px;
}
</style>


 
<style scoped>
.dashboard-container {
  display: flex;
  /* 使用flex布局 */
  justify-content: space-between;
  /* 子元素之间的间隔 */
  align-items: flex-start;
  /* 子元素垂直方向顶部对齐 */
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #71e4ae;
}
 
h1 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}
 
.info-list {
  list-style-type: none;
  /* 移除列表项前的标记 */
  padding: 0;
}
 
.info-list li {
  margin-bottom: 10px;
  font-size: 16px;
  color: #666;
}
 
.sidebar {
  width: 200px;
  /* 侧边栏宽度 */
  background-color: #f4f4f4;
  /* 侧边栏背景色 */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
 
.sidebar ul {
  list-style-type: none;
  padding: 0;
}
 
.sidebar li {
  margin-bottom: 10px;
}
 
.sidebar a {
  color: #333;
  text-decoration: none;
  font-size: 16px;
  display: block;
  /* 使链接占据整行 */
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
  /* 平滑过渡效果 */
}
 
.sidebar a:hover {
  background-color: #c6ec97;
  /* 鼠标悬停时的背景色 */
}
 
.app-container {
  display: flex;
}
 
.main-content {
  flex: 1;
  /* 剩余空间 */
  padding: 20px;
  /* 内容区域的内边距 */
}
 
.sidebar-container {
  display: flex;
  flex-direction: column;
  width: 200px;
  min-height: 100vh;
  background-color: #545c64;
}
 
.collapse-button {
  margin: 10px;
  align-self: flex-end;
  background-color: #545c64;
  color: #fff;
  border: none;
}
 
.el-menu-vertical-demo {
  flex: 1;
  background-color: #4d4f52;
}
 
:deep(.el-menu-vertical-demo .el-menu-item) {
  color: #fff;
  background-color: cadetblue;
}
 
:deep(.el-menu-vertical-demo .el-sub-menu__title) {
  color: #fff;
}
 
:deep(.el-menu-vertical-demo .el-menu-item:hover),
:deep(.el-menu-vertical-demo .el-sub-menu__title:hover) {
  background-color: #1f2d3d;
}
 
:deep(.el-menu-vertical-demo .el-menu-item.is-active),
:deep(.el-menu-vertical-demo .el-sub-menu__title.is-active) {
  background-color: #ffd04b;
  color: #545c64;
}
 
:deep(.el-menu-vertical-demo .el-sub-menu__title) i,
:deep(.el-menu-vertical-demo .el-menu-item) i {
  margin-right: 10px;
}
 
.router-link-active {
  color: #ffd04b;
}
</style>