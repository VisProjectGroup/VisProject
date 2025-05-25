<template>
  <div style="display: flex; flex-direction: column; align-items: center;">
    <div style="font-size: 22px; font-weight: bold; margin-bottom: 16px;">
      当前城市：{{ CityName }}
    </div>
    <div style="font-size: 22px; font-weight: bold; margin-bottom: 16px;">
      AQI - 风速 玫瑰图
    </div>
    <div style="width: 100%; display: flex; flex-direction: row; align-items: center; justify-content: center; margin-bottom: 20px;">
      <div class="year-btn-group-rect" style="display: flex;">
        <button
          v-for="(y, idx) in years"
          :key="y"
          :class="['year-btn-rect', { active: selectedYear === y }]"
          @click="selectedYear = y"
          style="border-radius: 0; margin: 0; border: 1px solid #4a90e2; border-right: none; padding: 8px 20px; background: white; color: #4a90e2; font-size: 16px;"
          :style="idx === years.length - 1 ? 'border-right:1px solid #4a90e2;' : ''"
        >
          {{ y }}
        </button>
      </div>
    </div>
    <div ref="chartContainer" class="chart-container" style="display: flex; justify-content: center;"></div>
    <div v-if="selectedMonth !== null" style="margin-top: 16px; font-size: 18px;">
      <b>{{ months[selectedMonth] }}</b> - 风速: {{ monthData.winditation.toFixed(2) }} km/h, AQI: {{ monthData.aqi.toFixed(2) }}
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import aqiUrl from "../assets/data/monthly_data/2015-2021_aqi_per_month.json";
import windUrl from "../assets/data/monthly_data/2015-2021_wind_speed_per_month.json";

export default {
  name: "Gradient-encoding",
  props: {
    CityName: {
      type: String,
      default: "杭州市",
    },
    CityCode: {
      type: String,
      default: "330100",
    },
    Year: {
      type: String,
      default: "2015",
    },
    width: {
      type: Number,
      default: 500,
    },
    height: {
      type: Number,
      default: 300,
    },
  },
  data() {
    return {
      years: ["2015", "2016", "2017", "2018", "2019", "2020", "2021"],
      selectedYear: this.Year,
      selectedMonth: null,
      monthData: {},
      months: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
      ],
      mergedData: [],
    };
  },
  mounted() {
    this.initializeChart();
  },
  watch: {
    selectedYear() {
      this.selectedMonth = null;
      this.initializeChart();
    },
    CityName() {
      this.selectedMonth = null;
      this.initializeChart();
    }
  },
  methods: {
    async initializeChart() {
      
      d3.select(this.$refs.chartContainer).selectAll("*").remove();

      const [windData, aqiData] = await Promise.all([
        Promise.resolve(windUrl),
        Promise.resolve(aqiUrl),
      ]);
      const city = this.CityName;
      const city_code = this.CityCode;
      const year = this.selectedYear;

      // const cityAQI = aqiData.find((d) => d.city_code === city_code);
      const cityAQI = aqiData.find((d) => d.city === city);
      const yearAQI = cityAQI?.years.find((y) => y.year === year);
      const aqiMonths = yearAQI ? yearAQI.months.map(Number) : Array(12).fill(0);
      
      // const cityWind = windData.find((d) => d.city_code === city_code);
      const cityWind = windData.find((d) => d.city === city);
      const yearWind = cityWind?.years.find((y) => y.year === year);
      const windMonths = yearWind ? yearWind.months.map(Number) : Array(12).fill(0);

      const aqi_scaling = 0.05;
      const aqiMax = d3.max(aqiMonths);
      const windMax = d3.max(windMonths);
      const radiusMax = Math.max(aqiMax, windMax / aqi_scaling) * 1.1;

      const mergedData = Array.from({ length: 12 }, (_, i) => ({
        month: i,
        winditation: windMonths[i],
        aqi: aqiMonths[i],
      }));
      this.mergedData = mergedData; // 保存数据用于点击时显示

      const width = 800;
      const height = 600;
      const margin = { top: 50, right: 50, bottom: 50, left: 50 };

      const svg = d3
        .select(this.$refs.chartContainer)
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      const chart = svg
        .append("g")
        .attr("transform", `translate(${width / 2},${height / 2})`);

      const angleScale = d3
        .scaleLinear()
        .domain([0, 12])
        .range([0, 2 * Math.PI]);

      const radiusScale = d3
        .scaleLinear()
        .domain([0, radiusMax])
        .range([0, Math.min(width, height) / 2 - Math.max(margin.top, margin.bottom)]);

      const winditationArea = d3
        .areaRadial()
        .angle((d) => angleScale(d.month))
        .innerRadius(0)
        .outerRadius((d) => radiusScale(d.winditation) / aqi_scaling)
        .curve(d3.curveLinearClosed);
      
      const aqiLine = d3
        .lineRadial()
        .angle((d) => angleScale(d.month))
        .radius((d) => radiusScale(d.aqi))
        .curve(d3.curveCardinalClosed);

      const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radiusScale.range()[1]);

      // AQI 区域
      chart
        .append("path")
        .datum(mergedData)
        .attr("d", aqiLine)
        .attr("fill", "#00D800")
        .attr("fill-opacity", 0.3)
        .attr("stroke", "#008800")
        .attr("stroke-width", 1.5);

      // 风速折线
      chart
        .append("path")
        .datum(mergedData)
        .attr("d", winditationArea)
        .attr("fill", "none")
        .attr("stroke", "#f39c12")
        .attr("stroke-width", 2);

      chart.selectAll(".month-hover")
        .data(mergedData)
        .join("path")
        .attr("class", "month-hover")
        .attr("d", (d, i) =>
          arc({
        startAngle: angleScale(i),
        endAngle: angleScale(i + 1),
          })
        )
        .attr("fill", "transparent")
        .attr("cursor", "pointer")
        .on("mouseover", (event, d) => {
          this.selectedMonth = d.month;
          this.monthData = d;
        })
        .on("mouseout", () => {
          this.selectedMonth = null;
          this.monthData = {};
        });

      const axis = chart
        .append("g")
        .attr("class", "axis");

      const months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
      ];

      axis
        .selectAll(".month-label")
        .data(months)
        .join("text")
        .attr("class", "month-label")
        .attr("text-anchor", (d, i) => (i < 3 || i > 9 ? "middle" : i < 6 ? "start" : "end"))
        .attr("x", (d, i) => Math.sin(angleScale(i)) * (radiusScale.range()[1] + 20))
        .attr("y", (d, i) => -Math.cos(angleScale(i)) * (radiusScale.range()[1] + 20))
        .text((d) => d);

      const maxRadius = radiusScale.range()[1];
      const gridRadii = [1, 2, 3].map(i => (i * maxRadius) / 3);

      axis
        .selectAll(".grid-circle")
        .data(gridRadii)
        .join("circle")
        .attr("class", "grid-circle")
        .attr("r", d => d)
        .attr("cx", 0)
        .attr("cy", 0)
        .attr("fill", "none")
        .attr("stroke", "#bbb")
        .attr("stroke-dasharray", "2,2");

      const legend = svg
        .append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${width - 150}, 20)`);

      // AQI 区域
      legend
        .append("rect")
        .attr("width", 20)
        .attr("height", 20)
        .attr("fill", "#00E400")
        .attr("opacity", 0.3);
      legend
        .append("text")
        .attr("x", 30)
        .attr("y", 15)
        .text("AQI");

      // 风速折线
      legend
        .append("path")
        .attr("d", d3.line()([[0, 40], [20, 40]]))
        .attr("stroke", "#4a90e2")
        .attr("stroke-width", 2);
      legend
        .append("text")
        .attr("x", 30)
        .attr("y", 45)
        .text("Wind-Speed");
    },
  },
};
</script>

<style>
.chart-container {
  margin: 20px;
}

.axis text {
  font-size: 16px;
  fill: #666;
}

.legend text {
  font-size: 14px;
  fill: #333;
}
</style>