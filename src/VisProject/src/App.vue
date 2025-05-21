<!-- app.vue -->
<template>
  <div class="container">
    <div class="map-area">
      <!-- 使用地图组件并监听点击事件 -->
      <MapComponent @CityClick="handleCityClick" />
    </div>
    <!-- 右侧面板：显示选中的省份 -->
    <div class="chart-area">
      <p>app.vue 接收map.vue传递出的点击城市： {{ selectedCity}}</p>
      <ChartComponent :CityName="selectedCity" />
    </div>
      
  </div>
</template>

<script setup>
import { ref } from 'vue';
import MapComponent from './components/Map.vue'; // 引入地图组件
import ChartComponent from './components/charts.vue'; // 引入图表组件

const selectedCity = ref('');

const handleCityClick = (CityName) => {
  selectedCity.value = CityName;
};


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
</style>