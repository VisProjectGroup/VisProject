<!-- app.vue -->
<template>
  <div class="container">
    <div class="sidebar-container">
      <el-container style="height: 100vh;">
        <!-- 移除 el-aside 的固定宽度，使用 class 控制 -->
        <el-aside>
          <el-menu :default-active="activeIndex" class="el-menu-vertical-demo" @select="handleSelect"
            :collapse="isCollapse" router="false">
            <el-menu-item index="Dashboard"
              style="background-color:rgb(77, 79, 82) ;color: aliceblue;">首页</el-menu-item>
            <el-sub-menu v-for="item in ChartData" :key="item.id" :index="item.id">
              <template #title>
                <span>{{ item.functionName }}</span>
              </template>
              <el-menu-item v-for="subItem in item.children" :key="subItem.id" :index="subItem.id" >
                {{ subItem.functionName }}
              </el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
      <div class="collapse-button" @click="toggleCollapse">
        <i :class="isCollapse ? 'el-icon-arrow-right' : 'el-icon-arrow-left'"></i>
      </div>
    </div>
    <div class="map-area">
      <MapComponent @CityClick="handleCityClick" />
    </div>
    <div class="polar-area" v-if="columAQIshow">
      <ColumnAQIComponent :CityName="selectedCity" />
    </div>
    <div class="polar-area" v-if="columRainshow">
      <ColumnRainComponent :CityName="selectedCity" />
    </div>
    <div class="polar-area" v-if="columWindshow">
      <ColumnWindComponent :CityName="selectedCity" />
    </div>
    <div class="polar-area" v-if="columFactoryshow">
      <ColumnFactoryComponent :CityName="selectedCity" />
    </div>
    <div class="polar-area" v-if="roseAQIrainshow">
      <PolarAQIRainComponent :CityName="selectedCity"/>
    </div>
    <div class="polar-area" v-if="roseAQIwindshow">
      <PolarAQIWindComponent :CityName="selectedCity"/>
    </div>
    <div class="right-panel" v-if="parallelmonthshow">
      <ParallelMonthlyComponent :CityName="selectedCity"/>
    </div>
    <div class="right-panel" v-if="parallelyearshow">
      <ParallelYearlyComponent :CityName="selectedCity"/>
    </div>
  </div>
</template>

<script setup>
import { ElContainer, ElAside, ElMenu, ElSubMenu, ElMenuItem } from 'element-plus';
import { ref } from 'vue';
import MapComponent from './components/Map.vue';
import ColumnAQIComponent from './components/ColumnAQI.vue';
import ColumnRainComponent from './components/ColumnRain.vue';
import ColumnWindComponent from './components/ColumnWind.vue';
import ColumnFactoryComponent from './components/ColumnFactory.vue';
import PolarAQIRainComponent from './components/polar_aqi_rain.vue';
import PolarAQIWindComponent from './components/polar_aqi_wind.vue';
import ParallelMonthlyComponent from './components/parralel_monthly.vue';
import ParallelYearlyComponent from './components/parralel_yearly.vue';

const selectedCity = ref('杭州市');
const handleCityClick = (CityName) => {
  selectedCity.value = CityName;
};

const ChartData = [
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
    return {
      columAQIshow: true,
      columRainshow: false,
      columWindshow: false,
      columFactoryshow: false,
      roseAQIrainshow: false,
      roseAQIwindshow: false,
      lineshow: false,
      bubbleshow: false,
      heatmapshow: false,
      parallelmonthshow: false,
      parallelyearshow: false,
      activeIndex: 11,
      isCollapse: false
    }
  },
  methods: {
    handleSelect(key) {
      this.activeIndex = key;
    },
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    }
  },
  watch: {
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
  }
}
</script>

<style>
.container {
  display: flex !important;
  gap: 0 !important;
  padding: 70px 0 0 0 !important;
  margin-top: -20px !important;
}

.map-area { 
  width: 60% !important;
  background-color: #e8e8f0 !important;
  padding: 15px !important;
  margin-left: 20px !important;
}

.polar-area, .right-panel {
  width: 40% !important;
  background-color: #f5f5f5 !important;
  padding: 15px !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 4px !important;
  margin-left: 15px !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}
</style>

<style scoped>
:root {
  --menu-width: 150px;
}

.sidebar-container {
  display: flex !important;
  flex-direction: column !important;
  width: var(--menu-width) !important;
  min-height: 100vh !important;
  background-color: transparent !important; /* 移除侧边栏容器的背景色 */
  box-shadow: none !important; /* 移除阴影 */
  transition: all 0.3s !important;
  margin-left: -10px !important;
  flex-shrink: 0 !important;
}

.collapse-button {
  margin: 10px !important;
  align-self: flex-end !important;
  background-color: transparent !important;
  color: #545c64 !important; /* 改变颜色以匹配菜单 */
  border: none !important;
  cursor: pointer !important;
  padding: 8px !important;
  transition: background-color 0.3s !important;
  position: relative !important;
  z-index: 1 !important;
}

.collapse-button:hover {
  background-color: rgba(67, 74, 80, 0.1) !important; /* 降低悬停时的背景色透明度 */
  border-radius: 4px !important;
}

.el-menu-vertical-demo {
  flex: 1 !important;
  border-right: none !important;
  background-color: #545c64 !important;
  transition: all 0.3s !important;
  border-radius: 4px !important; /* 添加圆角 */
  margin: 0 10px !important; /* 添加边距 */
}

/* 修改折叠样式，不改变宽度 */
.el-menu-vertical-demo.el-menu--collapse :deep(.el-sub-menu__title) span,
.el-menu-vertical-demo.el-menu--collapse :deep(.el-menu-item) span {
  visibility: hidden !important;
  opacity: 0 !important;
  transition: opacity 0.3s !important;
}

:deep(.el-menu) {
  border-right: none !important;
  width: 90% !important;
}

:deep(.el-menu-vertical-demo .el-menu-item),
:deep(.el-menu-vertical-demo .el-sub-menu__title) {
  color: #fff !important;
  background-color: #545c64 !important;
  height: 50px !important;
  line-height: 50px !important;
  padding: 0 20px !important;
  width: 90% !important;
}

:deep(.el-menu-vertical-demo .el-menu-item:hover),
:deep(.el-menu-vertical-demo .el-sub-menu__title:hover) {
  background-color: #434a50 !important;
}

:deep(.el-menu-vertical-demo .el-menu-item.is-active) {
  background-color: #409EFF !important;
  color: #fff !important;
}

:deep(.el-sub-menu .el-menu-item) {
  width: var(--menu-width) !important;  /* 使用同样的宽度变量 */
  padding: 0 20px !important;
  margin: 0 !important;
  background-color: #363d40 !important;
}

:deep(.el-menu-item.is-active),
:deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: #409EFF !important;
}

:deep(.el-menu--inline) {
  background-color: #363d40 !important;
}

:deep(.el-sub-menu__icon-arrow) {
  display: none !important;
}
</style>