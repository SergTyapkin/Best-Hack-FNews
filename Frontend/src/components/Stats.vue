<style lang="stylus" scoped>
@require '../styles/constants.styl'

.stats
  padding 0
  overflow-y scroll
  .title
    font-weight bold
    font-size 16px
    margin-top 15px
    margin-left 15px
</style>

<template>
  <div class="plate stats scrollable">
    <div class="title">Котировки</div>
    <div v-for="cur in currencies" class="currency">
      <Currency :symbol="cur.symbol" :percents="cur.percents" :value="cur.rate" :name="cur.name" :plainRender="true"></Currency>
    </div>
  </div>
</template>


<script>
import {curNameToSymbol} from "../utils/utils";
import Currency from "./Currency.vue";

export default {
  components: {Currency},

  props: {
    data: {}
  },

  data() {
    return {
      currencies: [],
    }
  },

  async mounted() {
    await this.updateCurrencies();
  },

  methods: {
    async getCurrencies() {
      const currencies = await this.$store.state.api.getCurrencies();
      if (!currencies.ok_) {
        this.$store.state.popups.error('Не удалось получить список валют');
        return [];
      }
      return currencies.currencies;
    },

    async updateCurrencies() {
      this.currencies = await this.getCurrencies();
      this.currencies.forEach(cur => cur.symbol = curNameToSymbol(cur.name));
    }
  }
}
</script>
