<style lang="stylus" scoped>
@require '../styles/constants.styl'


div.balance-plate
  text-align left
  background mix(bgColor, transparent, 60%)
  border 1px solid textColor5
  font-size 15px
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
        font-weight lighter
    .currency:not(:last-child)
      border-right 1px solid textColor5
    .currency:first-child
      padding-left 0
    .currency:last-child
      padding-right 0

  .add-button
    color textColor4
    cursor pointer
    float right
    transition all 0.2s ease
  .right
    color textColor4
    float right
    margin 0 5px
  .add-button:hover
    color textColor2


.modal
  .form
    margin 0
    max-width unset
    background none
    border none
    font-size 20px
    input[type=number]
      all unset
      width calc(100% - 100px)
      text-align left
    input[type=submit]
      width 100%
      padding 10px

    .symbol
      color #50E2C2
      font-size 30px
    .name
      margin-left 10px
      line-height 35px
</style>

<template>
  <div class="plate balance-plate">
    <div class="title">
      Баланс счёта
      <span class="add-button" @click="startDialog(false)">вывести</span>
      <span class="right"> / </span>
      <span class="add-button" @click="startDialog(true)">пополнить</span>
    </div>

    <div class="currencies">
      <div class="currency" v-for="cur in currencies">
        <span>{{ cur.amount }}</span>
        <span class="symbol">{{ cur.symbol }}</span>
      </div>
    </div>
  </div>

  <ModalSlot ref="modal">
    <form class="form" @submit.prevent="doAction">
      <div class="input-like" ref="exchangeInfo">
        <input type="number" autocomplete="off" placeholder=" " v-model="value">
        <span>
          <span class="symbol">₽</span>
          <span class="name">RUB</span>
        </span>
      </div>

      <div class="submit-buttons">
        <input type="submit" :value="isTopUp ? 'Пополнить' : 'Вывести'" class="button">
      </div>
    </form>
  </ModalSlot>
</template>


<script>
import {curNameToSymbol} from "../utils/utils";
import ModalSlot from "./ModalSlot.vue";

export default {
  components: {ModalSlot},
  data() {
    return {
      isTopUp: null,
      currencies: [],
      value: 0,
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
    },

    startDialog(isTopUp) {
      this.isTopUp = isTopUp;
      this.$refs.modal.show = true;
    },
    async doAction() {
      let res;
      if (this.isTopUp)
        res = await this.$store.state.api.topup(this.value);
      else
        res = await this.$store.state.api.withdraw(this.value);

      if (res.ok_) {
        this.$store.state.popups.success("Успешная операция", (this.isTopUp ? "зачислено " : "выведено ") + this.value + "₽");
        this.value = 0;
        this.$refs.modal.show = false;
        return;
      }

      if (res.status_ === 409) {
        this.$store.state.popups.error("Недостаточно средств");
        return;
      }
      this.$store.state.popups.error("Не удалось выполнить операцию", "Неизвестная ошибка");
    }
  }
}
</script>
