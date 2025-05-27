<template>
  <div class="map-container">
      <div id='mapDom'></div>
  </div>
</template>
<script setup>
    import { ref,nextTick, onMounted } from 'vue'
    import china from '../assets/data/map/china.json'
    import * as echarts from 'echarts'
    import cityToProvince from '../assets/data/map/city_to_province1.json';
    import provinceToColor from '../assets/data/map/province_to_color.json';

    // 定义 emit 用于触发父组件事件 即给 app.vue 传递城市名称
    const emit = defineEmits(['CityClick'])
    
    const mapEcharts = () =>{//初始化地图的函数
      let initMap = echarts.init(document.querySelector('#mapDom')
        , null, {
        width: '800px', // 地图大小
        height: '600px' // 地图大小
      });//初始化 ECharts 实例，将其绑定到之前模板中的mapDom元素
      echarts.registerMap('china', china);//注册中国地图
      // 为每个市添加省份信息并分配颜色
        
      // 根据市名获取对应的省份
      const getProvinceByCity = (cityName) => {
        return cityToProvince[cityName] || '未知省份'
      }
        
        // 根据省份获取对应的颜色
      const getColorByProvince = (provinceName) => {
        return provinceToColor[provinceName] || '#FFFFFF' // 默认灰色
      }
      
      // 生成带颜色的数据数组（从 cityToProvince 生成）
      const dataWithColors = Object.keys(cityToProvince).map(cityName => {
        const province = getProvinceByCity(cityName)
        const color = getColorByProvince(province)
        
        return {
          name: cityName, // 市名
          value: Math.floor(Math.random() * 1000), // 随机生成数值（0-1000）
          itemStyle: {
            color: color // 根据省份映射的颜色
          },
          tooltip: {
            formatter: `{b}<br/>销量: {c}<br/>省份: ${province}` // 自定义提示信息
          }
        }
      })


      let options = {
          title: {//配置地图标题，主标题是 "中国地图"，副标题设置了一个链接
          text: '中国地图',
          textStyle: {
              fontSize: 24,  // 加大字体
              fontWeight: 'bold'  // 加粗
          },
          left: 250, 
          top: 20,  // 距离顶部的距离
          sublink:
              'http://zh.wikipedia.org/wiki/%E9%A6%99%E6%B8%AF%E8%A1%8C%E6%94%BF%E5%8D%80%E5%8A%83#cite_note-12'
          },
          tooltip: {//配置鼠标悬停时的提示框，当鼠标悬停在地图区域上时，会显示区域名称和对应的值
          trigger: 'item',
          formatter: '{b}<br/>{c} (销量)'
          },
          // toolbox: {//配置工具栏，显示在右侧中间位置，包含数据视图、重置和保存为图片等功能。
          // show: true,
          // orient: 'vertical',
          // left: 'right',
          // top: 'center',
          // feature: {
          //     dataView: { readOnly: false },
          //     restore: {},
          //     saveAsImage: {}
          // }
          // },
          visualMap: {//配置视觉映射，用于将数值映射为颜色，最小值是 0，最大值是 1000，使用了从浅蓝色到黄色再到橙红色的渐变色。
          min: 0,
          max: 1000,
          text: ['High', 'Low'],
          realtime: false,
          calculable: true,
          inRange: {
              color: ['lightskyblue', 'yellow', 'orangered']
          }
          },
          series: [//配置地图系列，设置为中国地图，不显示区域标签，
          {
              name: '中国',
              type: 'map',
              map: 'china',
              label: {
              show: false
              },
              data: dataWithColors, // 使用带颜色的数据
              roam: true // 开启平移和缩放功能，若只想开启缩放，可设置为'roam: \'scale\''
          }
          ]
      }
      initMap.setOption(options)

      // 添加地图点击事件监听
      initMap.on('click', (params) => {
        // 点击的是地图区域
        if (params.componentType === 'series') {
          const CityName = params.name // 获取点击的市名
          // 触发自定义事件，传递省份名称
          emit('CityClick', CityName)
        }
      })
    }
    onMounted(()=>{//在组件挂载后，给dataList赋值，包含了中国各省市自治区的数据。
        
        nextTick(()=>{
            mapEcharts()
        })
    })
</script>


<style scoped>
.map-container {
  width: 100%;  /* 占满父容器宽度 */
  height: 80vh; /* 使用视口高度的80% */
  margin: 0 auto;
  overflow: hidden; /* 添加overflow:hidden使超出部分隐藏 */
}

#mapDom {
  width: 100%;
  height: 100%;
}
</style>