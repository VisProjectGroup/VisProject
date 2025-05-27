<template>
  <div style="display: flex; flex-direction: column; align-items: center;">
    <div style="font-size: 22px; font-weight: bold; margin-bottom: 16px;">
      当前城市：{{ CityName }}
    </div>
    <div style="font-size: 22px; font-weight: bold; margin-bottom: 16px;">
      年度平行坐标分析
    </div>
    <div ref="chartContainer" class="chart-container" style="width: 100%; height: 600px;"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import energyData from "../assets/data/yearly_data/2015-2021_energy_consumption_per_year.json"
import precipData from "../assets/data/yearly_data/2015-2021_precipitation_per_year.json";
import aqiData from "../assets/data/yearly_data/2015-2021_aqi_per_year.json";
import windData from "../assets/data/yearly_data/2015-2021_wind_speed_per_year.json";

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
      dimensions: ["years", "aqi", "precipitation", "wind", "industry"],
      colorScale: null,
    };
  },
  computed: {
    processedData() {

      const getYearlyValue = (dataset) => {
      const city = dataset.find(d => d.city === this.CityName);
      if (!city || !city.years) return [];

        return this.years.map(y => city.years[y] !== undefined ? Number(city.years[y]) : null);
      };

      const industry = getYearlyValue(energyData);
      const precipitation = getYearlyValue(precipData);
      const aqi = getYearlyValue(aqiData);
      const wind = getYearlyValue(windData);

      return Array.from({length: this.years.length}, (_, i) => ({
        years: Number(this.years[i]),
        industry: industry[i] || 0,
        precipitation: precipitation[i] || 0,
        wind: wind[i] || 0,
        aqi: aqi[i] || 0
      })).filter(d =>
        !isNaN(d.industry) &&
        !isNaN(d.precipitation) &&
        !isNaN(d.wind) &&
        !isNaN(d.aqi)
      );
    }
    },
  watch: {
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

      const margin = { top: 50, right: 40, bottom: 10, left: 40 };
      const width = this.width - margin.left - margin.right;
      const height = this.height - margin.top - margin.bottom;

      const svg = d3.select(this.$refs.chartContainer)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      // 为每个维度设置单独的数据范围
      const y = {};
      this.dimensions.forEach(dim => {
        if (dim === "years") {
          y[dim] = d3.scaleLinear()
            .domain([2015, 2021])
            .range([height, 0]);
        } else {
          const extent = d3.extent(this.processedData, d => d[dim]);
          y[dim] = d3.scaleLinear()
          .domain(extent)
          .range([height, 0]);
        }
      });

      // 构建 x 比例尺
      const x = d3.scalePoint()
        .domain(this.dimensions)
        .range([0, width]);

      // 按 AQI 指数设置颜色比例尺
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
        .attr("stroke-width", 2)
        .attr("fill", "none")
        .attr("opacity", 0.7);

      // 绘制坐标轴
      this.dimensions.forEach(dim => {
        const axis = d3.axisLeft(y[dim])
          .tickFormat(d3.format("d"));
        svg.append("g")
          .attr("transform", `translate(${x(dim)},0)`)
          .call(axis)
          .append("text")
          .style("text-anchor", "middle")
          .attr("y", -16)
          .attr("fill", "#333")
          .text(this.getAxisLabel(dim))
          .style("font-size", "15px");
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
          `<div><b>年份:</b> ${d.years}</div>
           <div><b>AQI:</b> ${d.aqi.toFixed(2)}</div>
           <div><b>降水量:</b> ${d.precipitation.toFixed(2)} mm</div>
           <div><b>风速:</b> ${d.wind.toFixed(2)} km/h</div>
           <div><b>能源消耗:</b> ${d.industry.toFixed(2)} kwh</div>`
        );
        })
        .on("mousemove", function(event) {
          tooltip
        .style("left", (event.clientX + 20) + "px")
        .style("top", (event.clientY + 20) + "px");
        })
        .on("mouseleave", function() {
          d3.select(this).attr("stroke-width", 2.4).attr("opacity", 0.7);
          tooltip.style("display", "none");
        });
      },

      handleBrush(event, dim, yScales) {
        if (!event.selection) return;
        const [y0, y1] = event.selection.map(yScales[dim].invert);
        this.brushedRegions.set(dim, [Math.min(y0, y1), Math.max(y0, y1)]);
        this.updateHighlight();
      },

      handleBrushEnd(event, dim) {
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
        industry: "能源消耗 (kwh)",
        precipitation: "降水量 (mm)",
        wind: "风速 (km/h)",
        aqi: "AQI 指数",
        years: "年份"
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

.axis text {
  font-size: 12px;
  fill: #666;
}
</style>
