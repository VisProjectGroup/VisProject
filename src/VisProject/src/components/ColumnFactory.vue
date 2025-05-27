<template>
  <div style="display: flex; flex-direction: column; align-items: center;">
    <div style="font-size: 22px; font-weight: bold; margin-bottom: 16px;">
    {{ CityName }} 的能耗(吨标准煤)历史数据
    </div>
    <div ref="chartContainer" class="chart-container" style="width: 100%; height: 600px;"></div>

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

  },
  methods: {
    async fetchCityData() {
      try {
        const response = await fetch(`../assets/data/column/column_factory/energy_consumption/${this.CityName}.json`);
        if (!response.ok) throw new Error();
        const module = await import(`../assets/data/column/column_factory/energy_consumption/${this.CityName}.json`);
        this.data1 = module.default;
        this.drawChart();
      } catch {
        this.errorMessage = `无法加载 ${this.CityName} 的数据`;
      }
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
        .domain(this.data1.map(d => d.year))  // 使用实际存在的year字段
        .range([0, width])
        .padding(0.1);

      // 修正y轴定义
      const y = d3.scaleLinear()
        .domain([0, d3.max(this.data1, d => d.consumption)])  // 使用实际存在的consumption字段
        .nice()
        .range([height, 0]);

      // 绘制柱状图
      svg.selectAll(".bar")
        .data(this.data1)
        .join("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.year))
        .attr("y", d => y(d.consumption))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.consumption))
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
        .text("降水量(mm)");
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
  top: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.date-selector label {
  display: block;
  margin: 8px 0;
  color: #333;
  font-size: 14px;
}

.date-selector input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 160px;
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