<template>
  <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
    <div class="date-selector">
      <label>起始日期：</label>
      <input type="date" v-model="startDate">
      <label>结束日期：</label>
      <input type="date" v-model="endDate">
    </div>
    <div style="width: 100%;">
      <div style="font-size: 22px; font-weight: bold; margin-bottom: 16px;">
        {{ CityName }} 的 AQI 历史数据
      </div>
      <div ref="chartContainer" class="chart-container" style="width: 100%; height: 600px;"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: "Gradient-encoding",
  data() {
    return {
      databelong: "",
      data1: [],
      filteredData: [],
      readdatanum: 0,
      debugmessage: "not read data yet",
      errorMessage: "",
      startDate: "2015-01-02",
      endDate: "2021-12-31",
      margin: { top: 50, right: 30, bottom: 70, left: 60 },
    };
  },
  props: {
    CityName: {
      type: String,
      default: "杭州市"
    },
    width: {
      type: Number,
      default: 800
    },
    height: {
      type: Number,
      default: 500
    }
  },
  computed: {
    innerWidth() {
      return this.width - this.margin.left - this.margin.right;
    },
    innerHeight() {
      return this.height - this.margin.top - this.margin.bottom;
    }
  },
  mounted() {
    this.fetchCityData();
  },
  watch: {
    CityName() {
      this.fetchCityData();
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
        const response = await fetch(`../assets/data/AQI/cities_json/${this.CityName}.json`);
        if (!response.ok) throw new Error();
        const module = await import(`../assets/data/AQI/cities_json/${this.CityName}.json`);
        this.data1 = module.default.map(d => ({
          ...d,
          dateObj: new Date(d.date.replace(/\//g, '-'))
        }));
        this.filterDataByDate();
      } catch {
        this.errorMessage = `无法加载 ${this.CityName} 的数据`;
      }
    },
    filterDataByDate() {
      const start = this.startDate ? new Date(this.startDate) : null;
      const end = this.endDate ? new Date(this.endDate) : null;

      this.filteredData = this.data1.filter(item => {
        return (!start || item.dateObj >= start) && (!end || item.dateObj <= end);
      });
      this.drawChart();
    },
    drawChart() {
      // 清空容器时使用正确选择器
      d3.select(this.$refs.chartContainer).selectAll("*").remove();

      // 修正容器尺寸计算
      const container = this.$refs.chartContainer.getBoundingClientRect();
      const width = container.width - this.margin.left - this.margin.right;
      const height = container.height - this.margin.top - this.margin.bottom;

      // 创建SVG容器
      const svg = d3.select(this.$refs.chartContainer)
        .append("svg")
        .attr("width", width + this.margin.left + this.margin.right)
        .attr("height", height + this.margin.top + this.margin.bottom)
        .append("g")
        .attr("transform", `translate(${this.margin.left},${this.margin.top})`);

      // 修正x轴定义
      const x = d3.scaleBand()
        .domain(this.filteredData.map(d => d.date))  // 使用实际存在的date字段
        .range([0, width])
        .padding(0.1);

      // 修正y轴定义
      const y = d3.scaleLinear()
        .domain([0, d3.max(this.filteredData, d => d.aqi)])  // 使用实际存在的aqi字段
        .nice()
        .range([height, 0]);

      // 绘制柱状图
      svg.selectAll(".bar")
        .data(this.filteredData)
        .join("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.date))
        .attr("y", d => y(d.aqi))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.aqi))
        .attr("fill", "steelblue");

      // 添加x轴
      svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-45)");

      // 添加y轴
      svg.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("AQI值");
    }
  }
};
</script>

<style scoped>
.chart-container {
  margin: 20px;
}

.date-selector {
  position: absolute;
  right: 20px;
  top: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 12px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1;
}

.date-selector label {
  margin: 0;
  color: #333;
  font-size: 14px;
  white-space: nowrap;
}

.date-selector input[type="date"] {
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 130px;
  height: 28px;
  font-size: 14px;
}

.tooltip {
  position: absolute;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 12px;
  pointer-events: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  font-size: 14px;
  line-height: 1.4;
  opacity: 0;
  transition: opacity 0.2s;
}

.chart-title {
  text-anchor: middle;
  font-size: 18px;
  font-weight: bold;
  fill: #333;
}

.axis-label {
  font-size: 12px;
  fill: #666;
}

.grid line {
  stroke: #eee;
  stroke-width: 0.5;
}

.bar {
  transition: all 0.3s ease;
}
</style>