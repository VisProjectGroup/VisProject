<template>
  <div style="display: flex; flex-direction: column; align-items: center;">
    <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
      当前城市：{{ CityName }}
    </div>
    <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
      月度平行坐标分析
    </div>
    <div style="width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 12px;">
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <div class="year-btn-group-rect" style="display: flex;">
          <button
            v-for="y in years.slice(0, Math.ceil(years.length/2))"
            :key="y"
            :class="['year-btn-rect', { active: selectedYear === y }]"
            @click="selectedYear = y"
            style="border-radius: 0; margin: 0; border: 1px solid #4a90e2; border-right: none; padding: 4px 12px; background: white; color: #4a90e2; font-size: 14px; outline: none;"
            :style="y === years[Math.ceil(years.length/2)-1] ? 'border-right:1px solid #4a90e2;' : ''"
            tabindex="-1">
            {{ y }}
          </button>
        </div>
        <div class="year-btn-group-rect" style="display: flex;">
          <button
            v-for="y in years.slice(Math.ceil(years.length/2))"
            :key="y"
            :class="['year-btn-rect', { active: selectedYear === y }]"
            @click="selectedYear = y"
            style="border-radius: 0; margin: 0; border: 1px solid #4a90e2; border-right: none; padding: 4px 12px; background: white; color: #4a90e2; font-size: 14px; outline: none;"
            :style="y === years[years.length-1] ? 'border-right:1px solid #4a90e2;' : ''"
            tabindex="-1">
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
  name: "ParallelCoordinates",
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
      colorScale: null,
      brushedRegions: new Map(),
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

      return Array.from({length: 12}, (_, i) => ({
        month: i + 1,
        precipitation: precipitation[i] || 0,
        wind: wind[i] || 0,
        aqi: aqi[i] || 0
      })).filter(d => 
        !isNaN(d.precipitation) && 
        !isNaN(d.wind) && 
        !isNaN(d.aqi)
      );
    }
  },
  watch: {
    selectedYear() {
      this.brushedRegions.clear();
      this.dimensions.forEach(dim => {
        this.brushedRegions.delete(dim);
      });
      this.updateHighlight();
      this.renderChart();
    },
    CityCode() {
      this.brushedRegions.clear();
      this.dimensions.forEach(dim => {
        this.brushedRegions.delete(dim);
      });
      this.updateHighlight();
      this.renderChart();
    },
    CityName() {
      this.brushedRegions.clear();
      this.dimensions.forEach(dim => {
        this.brushedRegions.delete(dim);
      });
      this.updateHighlight();
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
        .attr("viewBox", `-21 0 ${width+60} ${height}`)
        .attr("preserveAspectRatio", "xMidYMid meet")

      // 每个维度坐标轴自定义
      const y = {};
      this.dimensions.forEach(dim => {
        if (dim === "month") {
          y[dim] = d3.scaleLinear()
          .domain([1, 12])
          .range([height/1.2, 0]);
        } else if (dim === "precipitation") {
          const max = d3.max(this.processedData, d => d[dim]);
          y[dim] = d3.scaleLinear()
          .domain([0, max])
          .range([height/1.2, 0]);
        } else {
          const extent = d3.extent(this.processedData, d => d[dim]);
          y[dim] = d3.scaleLinear()
          .domain(extent)
          .range([height/1.2, 0]);
        }
      });

      // x 比例尺
      const x = d3.scalePoint()
        .domain(this.dimensions)
        .range([0, width]);

      // 按照 AQI 设置颜色比例尺
      const color = d3.scaleLinear()
        .domain([0, 50, 100, 150, 200, 300, 500])
        .range(["#4ae24a", "#aee24a", "#ffe24a", "#ffc04a", "#ff7e4a", "#e24a4a", "#7e0023"]);

      // 绘制数据线
      svg.selectAll(".data-line")
        .data(this.processedData)
        .enter()
        .append("path")
        .attr("class", "data-line")
        .attr("d", d => d3.line()(this.dimensions.map(dim => [x(dim), y[dim](d[dim])])))
        .attr("stroke", d => color(d.aqi))
        .attr("stroke-width", 2.4)
        .attr("fill", "none")
        .attr("opacity", 0.7);

      // 绘制坐标轴
      this.dimensions.forEach(dim => {
        const axis = d3.axisLeft(y[dim]);
        svg.append("g")
          .attr("transform", `translate(${x(dim)},0)`)
          .call(axis)
          .append("text")
          .style("text-anchor", "middle")
          .attr("y", -16)
          .attr("fill", "#333")
          .style("font-size", "13px")
          .text(this.getAxisLabel(dim));
      });

      // 初始化刷选区域
      if (!this.brushedRegions) this.brushedRegions = new Map();

      // 添加刷选交互
      this.dimensions.forEach(dim => {
        const brush = d3.brushY()
          .extent([[-30, 0], [30, height]])
          .on("brush", (event) => this.handleBrush(event, dim, y))
          .on("end", (event) => this.handleBrushEnd(event, dim, y));

        const brushG = svg.append("g")
          .attr("class", `brush brush-${dim}`)
          .attr("transform", `translate(${x(dim)},0)`)
          .call(brush);

        // 单击任何地方取消所有刷选
        d3.select(this.$refs.chartContainer)
          .on("click", (event) => {
            if (event.target.tagName === "svg" || event.target.classList.contains("chart-container")) {
              this.brushedRegions.clear();
              this.dimensions.forEach(dim => {
            d3.select(`.brush-${dim}`).call(brush.move, null);
                });
                this.updateHighlight();
              }
          });

        // 如果有已刷选区域，恢复显示
        if (this.brushedRegions.has(dim)) {
          const [min, max] = this.brushedRegions.get(dim);
          d3.select(`.brush-${dim}`)
            .call(brush.move, [y[dim](max), y[dim](min)]);
        }
      });

      // 悬浮显示线条数据
      let tooltip = d3.select(this.$refs.chartContainer)
        .selectAll(".pc-tooltip")
        .data([null])
        .join("div")
        .attr("class", "pc-tooltip")
        .style("position", "fixed")
        .style("pointer-events", "none")
        .style("background", "rgba(255,255,255,0.95)")
        .style("border", "1px solid #aaa")
        .style("padding", "8px 12px")
        .style("border-radius", "4px")
        .style("font-size", "14px")
        .style("color", "#222")
        .style("box-shadow", "0 2px 8px rgba(0,0,0,0.15)")
        .style("display", "none")
        .style("z-index", 10);
      
      // 添加鼠标悬浮交互
      svg.selectAll(".data-line")
        .on("mouseover", function(event, d) {
          d3.select(this).attr("stroke-width", 4).attr("opacity", 1);
          tooltip
        .style("display", "block")
        .style("text-align", "left")
        .html(
            `<div><b>月份:</b> ${d.month} 月</div>
             <div><b>AQI:</b> ${d.aqi.toFixed(2)}</div>
             <div><b>降水量:</b> ${d.precipitation.toFixed(2)} mm</div>
             <div><b>风速:</b> ${d.wind.toFixed(2)} km/h</div>`
          );
        })
        .on("mousemove", function(event) {
          tooltip
          .style("left", (event.clientX + 20) + "px")
          .style("top", (event.clientY + 20) + "px");
        })
        .on("mouseleave", function() {
          d3.select(this).attr("stroke-width", 2).attr("opacity", 0.7);
          tooltip.style("display", "none");
        });
        },

    handleBrush(event, dim, yScales) {
      if (!event.selection) return;
      const [y0, y1] = event.selection.map(yScales[dim].invert);
      this.brushedRegions.set(dim, [Math.min(y0, y1), Math.max(y0, y1)]);
      this.updateHighlight();
    },

    handleBrushEnd(event, dim, yScales) {
      // 如果没有刷选，清除该维度的刷选
      if (!event.selection) {
        this.brushedRegions.delete(dim);
        this.updateHighlight();
      }
    },

    updateHighlight() {
      d3.selectAll(".data-line")
        .transition()
        .duration(200)
        .style("opacity", d =>
          Array.from(this.brushedRegions).every(([dim, [min, max]]) =>
           d[dim] >= min && d[dim] <= max
        ) ? 1 : 0.1
      );
    },

    getAxisLabel(dim) {
      const labels = {
        precipitation: "降水量 (mm)",
        wind: "风速 (km/h)",
        aqi: "AQI 指数",
        month: "月份"
      };
      return labels[dim];
    }
  }
};
</script>

<style scoped>
.chart-container {
  margin: 20px;
}

.data-line {
  fill: none;
  stroke-width: 1.5;
  transition: opacity 0.2s ease;
}

.year-btn-rect.active {
  background-color: #4a90e2 !important;
  color: white !important;
}

.axis text {
  font-size: 12px;
  fill: #666;
}
</style>
