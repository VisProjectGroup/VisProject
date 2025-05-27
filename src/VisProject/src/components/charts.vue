<template>
    <div class="chart-container">
      <div class="date-selector">
        <label>起始日期：</label>
        <input type="date" v-model="startDate">
        <label>结束日期：</label>
        <input type="date" v-model="endDate">
      </div>
      <div>
        <svg :width="width":height="height"></svg>
      </div>
    </div>
</template>
<script>
  import * as d3 from 'd3';
  
  export default {
    name: "Gradient-encoding",
    data(){//本模块私有数据
      return {
        databelong: "",//储存当前储存的数据对应的城市
        data1: [],//用于绘图的数据
        filteredData: [], // 经过日期筛选的数据
        readdatanum: 0,
        debugmessage: "not read data yet",
        errorMessage: "",
        startDate: "2015-01-02", // 起始日期
        endDate: "2021-12-31", // 结束日期
      };
    },
    props:{//从 app.vue 传来的数据
      CityName:{//城市名
          type: String,
          default: ""
      },
      width: {
          type: Number,
          default: 500
      },
      height: {
          type: Number,
          default: 300
      }
    },
    mounted(){
        this.fetchCityData();
      
    },
    watch:{
      CityName(newVal, oldVal) {
        this.fetchCityData();//因为这是个异步函数，所以后面导入完成之后才绘图
      },
      startDate() {
        this.filterDataByDate();
      },
      endDate() {
        this.filterDataByDate();
      }
    },
    methods: {
      async fetchCityData() {
        try {
          //先检查是否存在该文件
          const response = await fetch(`../assets/data/AQI/cities_json/${this.CityName}.json`);
          if (!response.ok) {
            this.data1 = [];
            this.filteredData = [];
            this.readdatanum = 0;
            this.debugmessage = "read data finish no data";  
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          else{
            // 动态导入对应城市的 JSON 文件
            const module = await import(`../assets/data/AQI/cities_json/${this.CityName}.json`);
            this.data1 = module.default;
            this.databelong = this.CityName;
            this.debugmessage = "read data successfully";            
            this.filterDataByDate(); // 应用日期过滤
          }
        } catch (error) {
          this.errorMessage = `无法加载 ${this.CityName} 的数据`;
        } 
      },
      filterDataByDate() {
        if (!this.startDate && !this.endDate) {
          this.filteredData = this.data1;
        } else {
          this.filteredData = this.data1.filter(item => {
            const itemDate = item.date.replace(/\//g, '-'); // 将数据中的日期格式转换为与输入框相同的格式
            const isAfterStart = !this.startDate || itemDate >= this.startDate;
            const isBeforeEnd = !this.endDate || itemDate <= this.endDate;
            return isAfterStart && isBeforeEnd;
          });
        }
        this.readdatanum = this.filteredData.length;
        this.drawChart();
      },
      drawChart() {//绘制柱形图
        const svg = d3.select("svg");
        svg.selectAll("*").remove(); // 清除之前的内容
        
        if (!this.filteredData || this.filteredData.length === 0) {
          return; // 如果没有数据，直接返回
        }

        const x = d3.scaleBand()//设置x轴
          .domain(this.filteredData.map(d => d.date))
          .range([0, this.width])
          .padding(0);

        const y = d3.scaleLinear()
          .domain([0, d3.max(this.filteredData, d => d.aqi)])
          .nice()
          .range([this.height, 0]);

        svg.append("g")
          .attr("transform", `translate(0, ${this.height})`)
          .call(d3.axisBottom(x));

        svg.append("g")
          .call(d3.axisLeft(y));

        svg.selectAll(".bar")
          .data(this.filteredData)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("x", d => x(d.date))
          .attr("y", d => y(d.aqi))
          .attr("width", x.bandwidth())
          .attr("height", d => this.height - y(d.aqi))
          .attr("fill", "steelblue")
          .on("mouseover", function (event, d) {
            d3.select(this).attr("fill", "orange");
          })
          .on("mouseout", function (event, d) {
            d3.select(this).attr("fill", "steelblue");
          });
      }
    }
  };
</script>
<style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    .chart-container {
      display: flex;
      flex-direction: row;
      align-items: flex-start;
      margin-top: 20px;
      position: relative;
    }
    .date-selector {
      position: absolute;
      right: -150px;
      top: 10px;
      background: rgba(255, 255, 255, 0.9);
      padding: 10px;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .date-selector label {
      display: block;
      margin: 5px 0;
    }
    .date-selector input {
      padding: 5px;
      border: 1px solid #ddd;
      border-radius: 4px;
      width: 140px;
    }
    .axis-label {
      font-size: 12px;
      fill: #666;
    }
    .grid line {
      stroke: lightgrey;
      stroke-opacity: 0.7;
      shape-rendering: crispEdges;
    }
    .grid path {
      stroke-width: 0;
    }
    .line {
      fill: none;
      stroke: #165DFF;
      stroke-width: 2px;
    }
    .dot {
      fill: white;
      stroke: #165DFF;
      stroke-width: 2px;
    }
    .tooltip {
      position: absolute;
      background-color: white;
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 8px;
      font-size: 12px;
      box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
      pointer-events: none;
    }
</style>
<style scoped>
  .bar {
    transition: fill 0.2s;
  }
</style>