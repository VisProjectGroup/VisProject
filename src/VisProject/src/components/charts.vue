<template>
    <div class="chart-container">
      <div>
        <p>{{this.debugmessage}}绘图器被输入 {{databelong}}的 {{ readdatanum }} 个数据</p>
      </div>
      <div>
        <svg :width="width":height="height"></svg>
      </div>
        
    </div>
</template>
<script>
  import * as d3 from 'd3';
  import { DOM } from 'd3-selection';
  
  export default {
    name: "Gradient-encoding",
    data(){//本模块私有数据
      return {
        databelong: "",//储存当前储存的数据对应的城市
        data1: [],//用于绘图的数据
        readdatanum: 0,
        debugmessage: "not read data yet",
        errorMessage: ""

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
      }
    },
    methods: {
      async fetchCityData() {
        try {
          //先检查是否存在该文件
          const response = await fetch(`../assets/data/AQI/cities_json/${this.CityName}.json`);
          if (!response.ok) {
            this.data1 = [];
            this.readdatanum = this.data1.length;
            this.debugmessage = "read data finish no data";  
            throw new Error(`HTTP error! status: ${response.status}`);

          }
          else{
            // 动态导入对应城市的 JSON 文件
            const module = await import(`../assets/data/AQI/cities_json/${this.CityName}.json`);
            this.data1 = module.default;
            this.databelong = this.CityName;
            this.readdatanum = this.data1.length;
            this.debugmessage = "read data successfully";            

            this.drawChart();//绘制图表
          }

        } catch (error) {
          this.errorMessage = `无法加载 ${this.CityName} 的数据`;
        } 
      },
      drawChart() {//绘制柱形图
        const svg = d3.select("svg");
        svg.selectAll("*").remove(); // 清除之前的内容
        const x = d3.scaleBand()//设置x轴
          .domain(this.data1.map(d => d.date))
          .range([0, this.width])
          .padding(0);

        const y = d3.scaleLinear()
          .domain([0, d3.max(this.data1, d => d.aqi)])
          .nice()
          .range([this.height, 0]);
        
        const color = d3.scaleSequential(y.domain(), d3.interpolateTurbo);
        const line = d3.line()
          .curve(d3.curveStep)
          .defined(d => !isNaN(d.aqi))
          .x(d => x(d.date))
          .y(d => y(d.aqi));


        svg.append("g")
          .attr("transform", `translate(0, ${this.height})`)
          .call(d3.axisBottom(x));

        svg.append("g")
          .call(d3.axisLeft(y));

        svg.selectAll(".bar")
          .data(this.data1)
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
        

        // Append the color gradient.
        const gradient = DOM.uid();
        svg.append("linearGradient")
            .attr("id", gradient.id)
            .attr("gradientUnits", "userSpaceOnUse")
            .attr("x1", 0)
            .attr("y1", this.height)
            .attr("x2", 0)
            .attr("y2", 10)
          .selectAll("stop")
            .data(d3.ticks(0, 1, 10))
          .join("stop")
            .attr("offset", d => d)
            .attr("stop-color", color.interpolator());

        // Append the line.
        svg.append("path")
            .datum(this.data1)
            .attr("fill", "none")
            .attr("stroke", gradient)
            .attr("stroke-width", 1.5)
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("d", line);
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
      justify-content: center;
      margin-top: 20px;
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