<template>
  <div class="correlation-heatmap">
    <div style="font-size: 22px; font-weight: bold; margin-bottom: 16px;">
        {{ cityData.name }} 的历年数据热力图
    </div>
    <!-- <div>
      ccc
      {{ corrMatrix }}
    </div> -->

    <div ref="chartContainer" class="chart-container"></div>
    <div class="controls">
      <label>
        显示方式：
        <select v-model="displayMode">
          <option value="full">完整矩阵</option>
          <option value="upper">上三角</option>
          <option value="lower">下三角</option>
        </select>
      </label>
      <label>
        色系：
        <select v-model="colorScheme">
          <option value="diverging">发散色 (红蓝)</option>
          <option value="sequential">顺序色 (蓝白红)</option>
        </select>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

// 接收父组件传递的城市名称
const props = defineProps({
  CityName: {
    type: String,
    required: true
  }
})

// 统一使用单个图表实例
const chartContainer = ref(null)
let chart = null

// 城市数据（响应式）
const cityData = ref({
  name: '',
  matrix: [],       // 热力图矩阵数据
  indicators: ['AQI', '降水量', '风力', '工业能耗']
})

// debug变量
// const debugdb = ref({
//   AQI :[],
//   Rainfall: [],
//   Wind: [],
//   Energy: []
// })
const debugmatrix = ref([])

const displayMode = ref('full')
const colorScheme = ref('diverging')

// 监听城市变化
watch(() => props.CityName, async (newCity) => {
  if (newCity) {
    await loadCityData(newCity)
    corrMatrix.value = cityData.value.matrix
    initChart()
  }
}, { immediate: true })

// 加载城市数据
// 在 HeatMapComponent.vue 的 <script setup> 中修改 loadCityData 函数
const loadCityData = async (cityName) => {
  try {
    // 1. 并行加载四个数据文件
    const [aqiData, rainfallData, windData, energyData] = await Promise.all([
      import('../assets/data/heatmapdata/aqi.json'),
      import('../assets/data/heatmapdata/precipitation.json'),
      import('../assets/data/heatmapdata/wind.json'),
      import('../assets/data/heatmapdata/factory.json')
    ])

    

    // 2. 提取目标城市数据
    const findCityData = (dataset) => {
      const city = dataset.default.find(item => item.city === cityName)
      return city ? Object.values(city.years).map(Number) : Array(7).fill(0)
    }

    const cityAQI = findCityData(aqiData)
    const cityRainfall = findCityData(rainfallData)
    const cityWind = findCityData(windData)
    const cityEnergy = findCityData(energyData)

    // 3. 准备时间序列数据（2015-2021）
    const datasets = {
      AQI: cityAQI,
      Rainfall: cityRainfall,
      Wind: cityWind,
      Energy: cityEnergy
    }

    // 3. 准备时间序列数据（2015-2021）
    // const years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021']
    // const datasets = {
    //   AQI: years.map(year => parseFloat(cityAQI[year]) || 0),
    //   Rainfall: years.map(year => parseFloat(cityRainfall[year]) || 0),
    //   Wind: years.map(year => parseFloat(cityWind[year]) || 0),
    //   Energy: years.map(year => parseFloat(cityEnergy[year]) || 0)
    // }

    // debugdb.value = datasets.value

    // 4. 计算相关系数矩阵
    const matrix = calculateCorrelationMatrix(datasets)

    


    // 5. 更新响应式数据
    cityData.value = {
      name: cityName,
      indicators :  ['AQI', '降水量', '风力', '工业能耗'],
      matrix : matrix
    }
    debugmatrix.value = cityData.value.matrix
  } catch (error) {
    console.error('加载城市数据失败:', error)
  }
}

// 相关系数计算函数
const calculateCorrelationMatrix = (datasets) => {
  const keys = ['AQI', 'Rainfall', 'Wind', 'Energy']
  const n = 4
  const matrix = Array(n).fill().map(() => Array(n).fill(0))

  // 计算每对指标间的相关系数
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i === j) {
        matrix[i][j] = 1.0 // 对角线为1
      } else if (i < j) {
        const corr = pearsonCorrelation(
          datasets[keys[i]],
          datasets[keys[j]]
        )
        matrix[i][j] = corr
        matrix[j][i] = corr // 对称矩阵
      }
    }
  }
  return matrix
}

// 皮尔逊相关系数计算
const pearsonCorrelation = (x, y) => {
  const n = x.length
  const sumX = x.reduce((a, b) => a + b, 0)
  const sumY = y.reduce((a, b) => a + b, 0)
  const sumXY = x.map((val, i) => val * y[i]).reduce((a, b) => a + b, 0)
  const sumX2 = x.map(val => val ** 2).reduce((a, b) => a + b, 0)
  const sumY2 = y.map(val => val ** 2).reduce((a, b) => a + b, 0)

  const numerator = sumXY - (sumX * sumY / n)
  const denominator = Math.sqrt(
    (sumX2 - sumX ** 2 / n) * (sumY2 - sumY ** 2 / n)
  )

  return denominator === 0 ? 0 : numerator / denominator
}


// 示例相关系数矩阵 (4x4)
const corrMatrix = ref([
  [1.00, 0.85, -0.32, 0.42],
  [0.85, 1.00, -0.18, 0.63],
  [-0.32, -0.18, 1.00, -0.55],
  [0.42, 0.63, -0.55, 1.00]
])

const variableNames = ['AQI', '降水量', '风力', '工业能耗']

// 根据显示模式过滤数据
const filteredData = () => {
  return corrMatrix.value.flatMap((row, i) => 
    row.map((value, j) => {
      if (displayMode.value === 'upper' && i > j) return null
      if (displayMode.value === 'lower' && i < j) return null
      return [i, j, value]
    }).filter(Boolean)
  )
}

// 获取色系配置
const getVisualMap = () => {
  return colorScheme.value === 'diverging' 
    ? {
        min: -1,
        max: 1,
        inRange: {
          color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', 
                 '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        }
      }
    : {
        min: -1,
        max: 1,
        inRange: {
          color: ['#053061', '#2166ac', '#4393c3', '#92c5de', '#d1e5f0',
                 '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b', '#67001f']
        }
      }
}

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) return
  
  chart = echarts.init(chartContainer.value)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chart) return
  
  const option = {
    tooltip: {
      position: 'top',
      formatter: params => {
        return `${variableNames[params.data[1]]} vs ${variableNames[params.data[0]]}<br/>
                相关系数: ${params.data[2].toFixed(2)}`
      }
    },
    grid: {
      top: 50,
      left: 100,
      right: 100,
      bottom: 80
    },
    xAxis: {
      type: 'category',
      data: variableNames,
      splitArea: { show: true },
      axisLabel: { rotate: 45 }
    },
    yAxis: {
      type: 'category',
      data: variableNames,
      splitArea: { show: true }
    },
    visualMap: {
      ...getVisualMap(),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 20
    },
    series: [{
      name: '相关系数',
      type: 'heatmap',
      data: filteredData(),
      label: {
        show: true,
        formatter: params => params.data[2].toFixed(2),
        color: '#333'
      },
      itemStyle: {
        borderColor: '#fff',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
  
  chart.setOption(option, true)
}

// 响应窗口变化
const handleResize = () => chart?.resize()

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

watch([displayMode, colorScheme], updateChart)

</script>

<style scoped>
.correlation-heatmap {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
.chart-container {
  width: 100%;
  height: 500px;
}
.controls {
  margin-top: 20px;
  display: flex;
  gap: 20px;
  justify-content: center;
}
select {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
</style>