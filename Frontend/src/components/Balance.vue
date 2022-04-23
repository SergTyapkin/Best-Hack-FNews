<style lang="stylus" scoped>
@require '../styles/constants.styl'

.balance-plate
  padding 10px 20px
  border-radius radiusM
  .currencies
    margin-top 16px
    margin-bottom 10px
    display flex
    .currency
      padding 0 20px
      .symbol
        margin-left 8px
        color textColor2
    .currency:not(:last-child)
      border-right 1px solid textColor5
    .currency:first-child
      padding-left 0
    .currency:last-child
      padding-right 0
</style>

<template>
  <div class="plate balance-plate">
    <div class="title">Баланс счёта</div>
    <div class="currencies">
      <div class="currency" v-for="cur in currencies">
        <span>{{ cur.value }}</span>
        <span class="symbol">{{ cur.symbol }}</span>
      </div>
    </div>
  </div>
</template>


<script>
import {curNameToSymbol} from "../utils/utils";

export default {
  data() {
    return {
      currencies: [],
    }
  },

  async mounted() {
    await this.updateBalance();
  },

  methods: {
    async getBalance() {
      const balance = await this.$store.state.api.getUserBalance();
      if (!balance.ok_) {
        this.$store.state.popups.error('Не удалось получить баланс');
        return [];
      }
      return balance.currencies;
    },

    async updateBalance() {
      this.currencies = await this.getBalance();
      this.currencies.forEach(cur => cur.symbol = curNameToSymbol(cur.name));
    }
  }
}
</script>
