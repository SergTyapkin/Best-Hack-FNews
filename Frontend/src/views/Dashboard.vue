<style lang="stylus" scoped>
@require '../styles/constants.styl'

photo-size = 180px
photo-column-width = 300px

borderColorInputs = textColor5

chart-bg = mix(black, transparent, 60%)

.dashboard-page
  display flex
  flex-direction column
  padding-right 80px
  padding-bottom 20px
  margin-left 80px
  box-sizing border-box


.top-string
  width 100%
  display flex
  .title
    font-size 45px
  .stocks-row
    margin-left 30px
    overflow-x hidden


.stocks-row
  .title
    font-size 12px
    color textColor2
    line-height 40px
  .stocks
    display flex
    overflow-x scroll

.graphs-row
  flex 1
  margin-top 30px
  height 400px
  .graph-container
    height 400px

.currency
  cursor pointer

.bg
  overflow visible

.chart
  position relative
.chart::after
.chart::before
  content ""
  position absolute
  width 100px
  top 0
  bottom 0
  background chart-bg
.chart::before
  right 100%
.chart::after
  left 100%
</style>

<style lang="stylus">
.fusioncharts-container // hide white background
  svg
    background-color unset !important

.fusioncharts-container svg > g:nth-of-type(2) // hide FusionCharts logo
  display none
  overflow hidden

.fusioncharts-container // graph's grid
  .raphael-group-25-axisReferenceVisualsBottom
    > path
      stroke-linecap round
</style>

<template>
  <TopBar></TopBar>

  <div class="dashboard-page">
    <BluredBG class="bg"></BluredBG>

    <div class="top-string">
      <div class="title">Графики</div>
      <div class="stocks-row">
        <div class="stocks scrollable">
          <Currency v-for="(cur, idx) in currencies" ref="currencies" @click="selectCurrency(idx)"
                    :symbol="cur.symbol"
                    :percents="cur.percents"
                    :value="cur.rate"
                    :name="cur.name"
          ></Currency>
        </div>
      </div>
    </div>

    <div class="graphs-row">
      <div class="graph-container">
        <fusioncharts class="chart"
            type="line"
            width="100%"
            :height="height"
            dataformat="json"
            :dataSource="dataSource"
            :onInitialized="(e) => {this.chart = e.sender}"
        ></fusioncharts>
      </div>
    </div>
  </div>
</template>


<script>
import Currency from "../components/Currency.vue";
import BluredBG from "../components/BluredBG.vue";
import TopBar from "../components/TopBar.vue";
import {curNameToSymbol} from "../utils/utils";
import {nextTick} from "vue";


export default {
  components: {BluredBG, Currency, TopBar},

  data() {
    return {
      selectedStockIdx: 0,

      currencies: [],
      selectedCurrency: null,

      updatingInterval: null,

      height: window.innerHeight / 5 * 4 - 112 - 50, // fixme: убрать эту дичь и сделать 100%
      dataSource: {
        "chart": {
          "theme": "my"
        },
        "data": [
          {},
        ],
      }
    }
  },

  async mounted() {
    console.log(this.height)
    this.currencies = await this.getCurrencies();
    this.currencies.forEach(cur => cur.symbol = curNameToSymbol(cur.name));

    if (this.currencies.length) {
      await nextTick();
      await this.selectCurrency(0);
    }

    this.updatingInterval = setInterval(() => {
      if (!this.chart)
        return;
      this.addPointToChart(20000);
    }, 1500);
  },

  unmounted() {
    clearInterval(this.updatingInterval);
  },

  methods: {
    async getCurrencies() {
      const currencies = await this.$store.state.api.getWatchingCurrencies();
      if (!currencies.ok_) {
        this.$store.state.popups.error('Не удалось получить список валют');
        return [];
      }
      return currencies.currencies;
    },

    async getStats(name) {
      const stats = await this.$store.state.api.getLineStats(name, '1h', new Date(Date.now() - 86400000));
      if (!stats.ok_) {
        this.$store.state.popups.error('Не удалось получить графики');
        return [];
      }

      return stats.data;
    },

    formatTime(date) {
      const h = date.getHours();
      const m = date.getMinutes();
      const s = date.getSeconds();
      return h % 12 + ':' + m + (h > 12 ? 'PM' : 'AM');
    },

    addPointToChart(value) {
      const arr = this.dataSource.data;

      if (arr.length > 11) {
        arr.splice(0, 1);
      }
      arr.push({
        label: this.formatTime(new Date()),
        value: value + (Math.random() - 0.5) * 5000
      });
    },

    setChartData(valueArray) {
      this.dataSource.data = [];
      valueArray.forEach((el) => {
        this.dataSource.data.push({
          label: el.date,
          value: el.value
        });
      });
    },

    async selectCurrency(idx) {
      if (this.selectedCurrency) {
        if (this.$refs.currencies[idx] === this.selectedCurrency)
          return;
        this.selectedCurrency.isSelected = false;
      }

      const cur = this.$refs.currencies[idx];
      cur.isSelected = true;
      this.selectedCurrency = cur;

      const data = await this.getStats(cur.name);
      this.setChartData(data);
    },
  }
}
</script>
