<template>
    <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
            当前城市：{{ CityName }}
        </div>
        <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
            月度数据折线图与柱状图
        </div>
        <div style="width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 12px;">
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div class="year-btn-group-rect" style="display: flex;">
                    <button
                        v-for="y in years.slice(0, Math.ceil(years.length / 2))"
                        :key="y"
                        :class="['year-btn-rect', { active: selectedYear === y }]"
                        @click="selectedYear = y"
                        style="border-radius: 0; margin: 0; border: 1px solid #4a90e2; border-right: none; padding: 4px 12px; background: white; color: #4a90e2; font-size: 14px; outline: none;"
                        :style="y === years[Math.ceil(years.length / 2) - 1] ? 'border-right:1px solid #4a90e2;' : ''">
                        {{ y }}
                    </button>
                </div>
                <div class="year-btn-group-rect" style="display: flex;">
                    <button
                        v-for="y in years.slice(Math.ceil(years.length / 2))"
                        :key="y"
                        :class="['year-btn-rect', { active: selectedYear === y }]"
                        @click="selectedYear = y"
                        style="border-radius: 0; margin: 0; border: 1px solid #4a90e2; border-right: none; padding: 4px 12px; background: white; color: #4a90e2; font-size: 14px; outline: none;"
                        :style="y === years[years.length - 1] ? 'border-right:1px solid #4a90e2;' : ''">
                        {{ y }}
                    </button>
                </div>
            </div>
        </div>
        <div ref="chartContainer" class="chart-container" style="width: 100%; height: 600px; display: flex; justify-content: center;"></div>
    </div>
</template>

<script>
import * as d3 from "d3";
import precipData from "../assets/data/monthly_data/2015-2021_precipitation_per_month.json";
import aqiData from "../assets/data/monthly_data/2015-2021_aqi_per_month.json";
import windData from "../assets/data/monthly_data/2015-2021_wind_speed_per_month.json";

export default {
  name: "BarLineChart",
  props: {
    CityName: {
      type: String,
      default: "杭州市"
    },
    CityCode: {
      type: String,
      default: "330100"
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
  data() {
    return {
      years: ["2015", "2016", "2017", "2018", "2019", "2020", "2021"],
      selectedYear: "2015",
      dimensions: ["month", "aqi", "precipitation", "wind"],
    };
  },
  computed: {
    processedData() {
      const getMonthlyData = (dataset) => {
        const city = dataset.find(d => d.city === this.CityName);
        if (!city) return [];
        const yearData = city.years.find(y => y.year === this.selectedYear);
        return yearData ? yearData.months.map(Number) : [];
      };

      const precipitation = getMonthlyData(precipData);
      const aqi = getMonthlyData(aqiData);
      const wind = getMonthlyData(windData);

      return Array.from({ length: 12 }, (_, i) => ({
        month: i + 1,
        precipitation: precipitation[i] || 0,
        wind: wind[i] || 0,
        aqi: aqi[i] || 0,
      })).filter(d =>
        !isNaN(d.precipitation) &&
        !isNaN(d.wind) &&
        !isNaN(d.aqi)
      );
    }
  },
  watch: {
    selectedYear() {
      this.renderChart();
    },
    CityCode() {
      this.renderChart();
    },
    CityName() {
      this.renderChart();
    }
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      d3.select(this.$refs.chartContainer).selectAll("*").remove();

      if (this.processedData.length === 0) return;

      const container = this.$refs.chartContainer;
      const width = container.clientWidth;
      const height = container.clientHeight;

      const svg = d3
        .select(this.$refs.chartContainer)
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", `-30 -40 ${width + 70} ${height}`)
        .attr("preserveAspectRatio", "xMidYMid meet");

      // x 比例尺 - 月份
      const x = d3.scaleBand()
        .domain(this.processedData.map(d => d.month))
        .range([0, width])
        .padding(0.1);

      // y 比例尺 - 降水量
      const yLeft = d3.scaleLinear()
        .domain([0, d3.max(this.processedData, d => d.precipitation)])
        .range([height, 0]);

      // y 右侧比例尺 - 风速
      const yRight = d3.scaleLinear()
        .domain([0, d3.max(this.processedData, d => d.wind)])
        .range([height, 0]);

      // 绘制 AQI 数据柱状图
      const color = d3.scaleLinear()
        .domain([0, 50, 100, 150, 200, 300, 500])
        .range(["#4ae24a", "#aee24a", "#ffe24a", "#ffc04a", "#ff7e4a", "#e24a4a", "#7e0023"]);

      // AQI 的 y 比例尺
      const yAqi = d3.scaleLinear()
        .domain([0, d3.max(this.processedData, d => d.aqi)*1.05 + 5])
        .range([height, 0]);

      svg.selectAll(".bar")
        .data(this.processedData)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.month))
        .attr("y", d => yAqi(d.aqi))
        .attr("width", x.bandwidth())
        .attr("height", d => height - yAqi(d.aqi))
        .attr("fill", d => color(d.aqi));

      // 在柱状图上标注 AQI 值
      svg.selectAll(".aqi-text")
        .data(this.processedData)
        .enter()
        .append("text")
        .attr("x", d => x(d.month) + x.bandwidth() / 2)
        .attr("y", d => yAqi(d.aqi) - 5)
        .attr("text-anchor", "middle")
        .attr("fill", "black")
        .attr("font-size", "12px")
        .text(d => d.aqi);

    // 绘制降水折线图
    const precipLine = d3.line()
      .x(d => x(d.month) + x.bandwidth() / 2)
      .y(d => yLeft(d.value));

    svg.append("path")
      .datum(this.processedData.map(d => ({ month: d.month, value: d.precipitation })))
      .attr("fill", "none")
      .attr("stroke", "#1f77b4")
      .attr("stroke-width", 2.4)
      .attr("d", precipLine);

    // 降水折线图节点
    svg.selectAll(".precip-dot")
      .data(this.processedData)
      .enter()
      .append("circle")
      .attr("class", "precip-dot")
      .attr("cx", d => x(d.month) + x.bandwidth() / 2)
      .attr("cy", d => yLeft(d.precipitation))
      .attr("r", 3.5)
      .attr("fill", "#1f77b4")
      .attr("stroke", "#fff")
      .attr("stroke-width", 0);

    // 绘制风速折线图
    const windLine = d3.line()
      .x(d => x(d.month) + x.bandwidth() / 2)
      .y(d => yRight(d.value));

    svg.append("path")
      .datum(this.processedData.map(d => ({ month: d.month, value: d.wind })))
      .attr("fill", "none")
      .attr("stroke", "#2ca02c")
      .attr("stroke-width", 2.4)
      .attr("d", windLine);

    // 风速折线图节点
    svg.selectAll(".wind-dot")
      .data(this.processedData)
      .enter()
      .append("circle")
      .attr("class", "wind-dot")
      .attr("cx", d => x(d.month) + x.bandwidth() / 2)
      .attr("cy", d => yRight(d.wind))
      .attr("r", 3.5)
      .attr("fill", "#2ca02c")
      .attr("stroke", "#fff")
      .attr("stroke-width", 0);

    // 横轴：月份
    svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d => `${d}月`));
    
    // 左侧纵轴：降水量
    svg.append("g")
      .call(d3.axisLeft(yLeft));

    // 右侧纵轴：风速
    svg.append("g")
      .attr("transform", `translate(${width}, 0)`)
      .call(d3.axisRight(yRight));

    // 左侧纵轴标签
    svg.append("text")
      .attr("x", 50)
      .attr("y", -10)
      .attr("text-anchor", "end")
      .attr("font-size", 14)
      .text("降水 (mm)");

    // 右侧纵轴标签
    svg.append("text")
      .attr("x", width - 40)
      .attr("y", -10)
      .attr("text-anchor", "start")
      .attr("font-size", 14)
      .text("风速 (km/h)");
    
    // 图例
    const legend = svg.append("g")
    .attr("transform", `translate(${width - 60}, -90)`);

    // 降水图例
    legend.append("line")
      .attr("x1", 0)
      .attr("y1", 5)
      .attr("x2", 20)
      .attr("y2", 5)
      .attr("stroke", "#1f77b4")
      .attr("stroke-width", 3);

    legend.append("text")
    .attr("x", 25)
    .attr("y", 10)
    .attr("font-size", "12px")
    .attr("fill", "#000")
    .text("降水量 (mm)");

    // 风速图例
    legend.append("line")
      .attr("x1", 0)
      .attr("y1", 25)
      .attr("x2", 20)
      .attr("y2", 25)
      .attr("stroke", "#2ca02c")
      .attr("stroke-width", 3);

    legend.append("text")
    .attr("x", 25)
    .attr("y", 30)
    .attr("font-size", "12px")
    .attr("fill", "#000")
    .text("风速 (km/h)");

    // AQI 图例
    const aqiLegend = svg.append("g")
    .attr("transform", `translate(${width - 60}, -50)`);

    aqiLegend.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 20)
    .attr("height", 10)
    .attr("fill", "#ffe24a");

    aqiLegend.append("text")
    .attr("x", 25)
    .attr("y", 10)
    .attr("font-size", "12px")
    .attr("fill", "#000")
    .text("AQI");

    // 鼠标悬浮提示框
    const tooltip = d3.select(this.$refs.chartContainer)
      .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("background", "rgba(255,255,255,0.95)")
      .style("border", "1px solid #ccc")
      .style("padding", "8px 12px")
      .style("border-radius", "6px")
      .style("pointer-events", "none")
      .style("font-size", "14px")
      .style("color", "#333")
      .style("box-shadow", "0 2px 8px rgba(0,0,0,0.08)")
      .style("display", "none")
      .style("z-index", 10);

    // 响应区域
    svg.selectAll(".hover-area")
      .data(this.processedData)
      .enter()
      .append("rect")
      .attr("class", "hover-area")
      .attr("x", d => x(d.month))
      .attr("y", 0)
      .attr("width", x.bandwidth())
      .attr("height", height)
      .attr("fill", "transparent")
      .on("mousemove", (event, d) => {
        tooltip
          .style("display", "block")
          .style("left", (event.clientX-10) + "px")
          .style("top", (event.clientY) + "px")
          .style("text-align", "left")
          .html(
            `<b><center>${d.month}月</center></b>
            <b>AQI</b>: ${d.aqi.toFixed(2)}<br/>
            <b>降水</b>: ${d.precipitation.toFixed(2)} mm<br/>
            <b>风速</b>: ${d.wind.toFixed(2)} km/h`
          );
      })
      .on("mouseleave", () => {
        tooltip.style("display", "none");
      });
    }
  }
};
</script>

<style scoped>
.chart-container {
  margin: 20px;
}

.bar {
  transition: opacity 0.2s ease;
}

.year-btn-rect.active {
  background-color: #4a90e2 !important;
  color: white !
}

.axis text {
    font-size: 14px;
    font: #666;
}
</style>