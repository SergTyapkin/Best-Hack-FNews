<style lang="stylus" scoped>
@require '../styles/constants.styl'

borderColorInputs = textColor5
borderColorInputsFocus = textColor2


.gradient-bg
  position absolute
  inset 0
  background linear-gradient(30deg, #000, transparent)
  opacity 1
  transition all 0.3s ease
  z-index -1
.gradient-bg.closed
  opacity 0

.page
  text-align center

.top-string
  width 100%
  margin-top 50px
  .half
    width 50%
    display inline-block
    .title
      font-size 45px
    .svg-button
      position absolute
      left 70px
      top 9px
    .svg-button.closed
      left 0
      opacity 0
  .half.page-name
    position relative
  .half.balance
    padding-right 60px
    padding-left 70px


.columns-flex-container
  display flex
  flex-direction row
  text-align left

.info-column
  flex 1
  max-width 5000px
  transition all 0.2s ease-in-out
.info-column
  margin-right 40px
  margin-left 80px
  opacity 1
  .form
    all unset
  div > div.input-like
    display flex
    align-items center
    justify-content space-between
    > div
      flex 1
      display flex
      align-items center
      .symbol
        color #50E2C2
        font-size 30px
      .name
        margin-left 10px
        font-size 20px
        line-height 35px
    > div:last-child
      justify-content flex-end
    > .arrows
      flex-direction column
      svg
        display block
        stroke textColor1
        stroke-width 2px
        overflow visible
        transition all 0.1s ease-out
    > .arrows:not(.bottom)
      svg.bottom
        stroke textColor1
        stroke-width 1px
        width 20px
    > .arrows:not(.bottom):hover
      svg.bottom
        stroke-width 2px
        width 23px
    > .arrows.bottom
      svg.top
        stroke textColor1
        stroke-width 1px
        width 20px
    > .arrows.bottom:hover
      svg.top
        stroke-width 2px
        width 23px

  .exchange-input-group
    .exchange-result
      position absolute
      right 0
      top 0
    .exchange-result.minus
      color colorMinus
    .exchange-result.plus
      color colorPlus

  .submit-buttons
    justify-content flex-end
    .button
      padding 7px
      width 120px


.info-column.closed
  flex 0
  max-width 0
  margin 0
  opacity 0
.info-column:not(.closed) ~ .currencies-column
.edit-column:not(.closed) ~ .currencies-column
  .currencies-container
    .currency-plate
      width calc(50% - 15px)


.currencies-column
  margin-top 50px
  margin-left 70px
  margin-right 45px
  flex 1
.currencies-container
  display flex
  flex-wrap wrap
  .currency-plate
    width calc(25% - 15px)
    height 70px
    margin-right 15px
    margin-bottom 15px
    cursor pointer

.edit-column
  flex 1
  transition all 0.2s ease-in-out
  max-width 5000px
  .currencies-container
    margin-left 40px
    overflow-y scroll
    max-height 400px
    .currency-plate
      width calc(50% - 15px)
.edit-column.closed
  flex 0
  opacity 0
  max-width 0

.float-button
  .svg
    opacity 0.7
    transform scale(0.8)

.currencies-column
.edit-column
  .hint
    text-align center
    font-size 14px
    color textColor3
    margin-bottom 10px
</style>

<template>
  <BluredBG></BluredBG>

  <TopBar></TopBar>

  <div :class="'gradient-bg ' + (selectedCurrency ? '' : 'closed')"></div>

  <div class="page">
    <div class="top-string">
      <div class="half page-name">
        <img :class="'svg-button ' + (selectedCurrency || isEditorOpened ? '' : 'closed')" src="../res/arrow_left.svg" alt="<-" @click="closeCurrencyColumn">
        <div class="title">Обмен валют</div>
      </div>
      <span class="half balance">
        <Balance ref="balance"></Balance>
      </span>
    </div>

    <div class="columns-flex-container">
      <div :class="'info-column ' + (selectedCurrency ? '' : 'closed')">
        <form class="form" @submit.prevent="doExchange">
          <div class="fields-container">
            <div>
              <div class="input-like" ref="exchangeInfo">
                <div>
                  <span class="symbol">{{ selectedCurrency?.symbol }}</span>
                  <span class="name">{{ selectedCurrency?.name }}</span>
                </div>
                <div class="arrows bottom" @click="switchCurrencies" ref="arrows">
                  <svg class="top" width="38" height="11" viewBox="0 0 38 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0 6.4498H36M36 6.4498L31.6 1M36 6.4498L31.6 11.8996"/>
                  </svg>
                  <svg class="bottom" width="38" height="11" viewBox="0 0 38 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g transform="rotate(180 18 6)"><path d="M0 6.4498H36M36 6.4498L31.6 1M36 6.4498L31.6 11.8996"/></g>
                  </svg>
                </div>
                <div>
                  <span class="symbol">₽</span>
                  <span class="name">RUB</span>
                </div>
              </div>
            </div>

            <div class="exchange-input-group">
              <span class="error-text">{{ errors.exchangeValue }}</span>
              <input type="number" autocomplete="off" placeholder=" " v-model="exchangeValue" @input="updateExchangeResult">
              <label>Сумма</label>
              <div :class="'exchange-result ' + (exchangeResult !== '0₽' ? (isSell ? 'plus' : 'minus') : '')">{{ exchangeResult }}</div>
            </div>

            <div class="submit-buttons">
              <input type="submit" @click="doExchange" value="Обменять" class="button">
            </div>
          </div>
        </form>
      </div>


      <div :class="'edit-column ' + (isEditorOpened ? '' : 'closed')">
        <div class="hint">Нажмите на валюту, чтобы добавить её в отслеживаемые</div>
        <div class="currencies-container scrollable">
          <Currency v-for="(cur, idx) in allCurrencies" class="currency-plate" ref="currencies" @click="moveCurrencyToMy(idx)"
                    :name="cur.name" :value="cur.rate" :percents="cur.percents" :symbol="cur.symbol"></Currency>
        </div>
      </div>


      <div class="currencies-column">
        <div v-if="isEditorOpened" class="hint">Нажмите на валюту, чтобы убрать её из отслеживаемых</div>
        <div v-else class="hint">Нажмите на валюту, чтобы обменять рубли на неё, или наоборот</div>

        <div class="currencies-container">
          <Currency v-for="(cur, idx) in currencies" class="currency-plate" ref="currencies" @click="selectCurrency(idx)"
                    :name="cur.name" :value="cur.rate" :percents="cur.percents" :symbol="cur.symbol"
                    :show-notify="true" @notify="notify"></Currency>
        </div>
      </div>
    </div>
    <div class="float-button" @click="opedEditCurrencies">
      <img class="svg" src="../res/edit.svg" alt="plus">
      <div class="hover-text">Изменить валюты</div>
    </div>
  </div>
</template>


<script>
import BluredBG from "../components/BluredBG.vue";

import TopBar from "../components/TopBar.vue";
import Balance from "../components/Balance.vue";
import Currency from "../components/Currency.vue";
import {curNameToSymbol, currencies} from "../utils/utils";

export default {
  components: {TopBar, BluredBG, Balance, Currency},
  data() {
    return {
      currencies: [],
      allCurrencies: [],
      selectedCurrency: null,

      isEditorOpened: false,

      isSell: false,
      exchangeValue: '',
      exchangeResult: '',
      enabled: true,
      errors: {},
    }
  },

  async mounted() {
    this.currencies = await this.getCurrencies();
  },

  methods: {
    async __exchangeActions() {
      if (this.exchangeValue.length === 0) {
        this.errors.exchangeValue = 'Дай деняк';
        return;
      }

      let response;
      if (!this.isSell)
        response = await this.$store.state.api.doExchange({
          nameFrom: 'RUB',
          nameTo: this.selectedCurrency.name,
          valueTo: this.exchangeValue,
        });
      else
        response = await this.$store.state.api.doExchange({
          nameTo: 'RUB',
          nameFrom: this.selectedCurrency.name,
          valueFrom: this.exchangeValue,
        });

      if (response.ok_) {
        this.$store.state.popups.success('Успешный обмен');
        this.selectedCurrency = null;
        await this.$refs.balance.updateBalance();
        return;
      }

      if (response.status_ === 409) {
        this.$store.state.popups.error('Недостаточно средств');
        return;
      }

      this.$store.state.popups.error('Не удалось совершить обмен', 'Неизвестная ошибка');
    },

    async doExchange() {
      if (!this.enabled) {
        return;
      }
      this.enabled = false;

      await this.__exchangeActions();

      this.enabled = true;
    },

    async getCurrencies(isAll = false) {
      const currencies_ = await this.$store.state.api[isAll ? 'getAllCurrencies' : 'getWatchingCurrencies']();
      if (!currencies_.ok_) {
        this.$store.state.popups.error('Не удалось получить список валют');
        return [];
      }
      currencies_.currencies.forEach(cur => cur.symbol = curNameToSymbol(cur.name));


      Object.keys(currencies).forEach(key => {
        key = key.toUpperCase();
        const perc = localStorage.getItem(key);
        if (perc !== null) {
          const item = currencies_.currencies.find(el => el.name === key);
          if (Math.abs(item?.percents) >= Number(perc)) {
            localStorage.removeItem(key);
            this.$store.state.popups.alert(`Валюта ${key} превысила порог изменения в ${perc}%.`, 'Вы были подписаны на это уведомление', 10000);
          }
        }
      });

      return currencies_.currencies;
    },


    async logOut() {
      const response = await this.$store.state.api.signOut();
      if (!response.ok_) {
        this.$store.state.popups.error('Не получилось выйти из аккаунта', 'Неизвестная ошибка');
        return;
      }
      await this.$router.push('/');
    },

    selectCurrency(idx) {
      if (this.isEditorOpened) {
        const currency = this.currencies[idx];
        this.allCurrencies.push(currency);
        this.currencies.splice(idx, 1);

        this.$store.state.api.removeCurrency(currency.name);
        return;
      }


      if (this.selectedCurrency) {
        this.selectedCurrency.isSelected = false;
      }

      const cur = this.$refs.currencies[idx];
      cur.isSelected = true;
      this.selectedCurrency = cur;

      this.updateExchangeResult();
    },
    closeCurrencyColumn() {
      if (this.selectedCurrency) {
        this.selectedCurrency.isSelected = false;
        this.selectedCurrency = null;
      }
      this.isEditorOpened = false;
    },

    switchCurrencies() {
      if (!this.isSell) {
        this.$refs.arrows.classList.remove('bottom');
        this.isSell = true;
      } else {
        this.$refs.arrows.classList.add('bottom');
        this.isSell = false;
      }

      this.updateExchangeResult();
    },

    updateExchangeResult() {
      if (this.exchangeValue != this.exchangeValue / 1) {// not Number
        this.errors.exchangeValue = "Накорректный формат";
        return;
      }
      this.errors.exchangeValue = undefined;

      if (!this.exchangeValue) {
        this.exchangeResult = '0₽';
        return;
      }
      if (this.exchangeValue.toString().length > 10) {
        this.exchangeValue = Number(this.exchangeValue.toString().slice(0, 10));
      }

      if (this.isSell) {
        this.exchangeResult = '+ ' + (this.exchangeValue * this.selectedCurrency.value) + '₽';
        return;
      }
      this.exchangeResult = '- ' + (this.exchangeValue * this.selectedCurrency.value) + '₽';
    },

    async opedEditCurrencies() {
      if (this.selectedCurrency) {
        this.selectedCurrency.isSelected = false;
        this.selectedCurrency = undefined;
      }
      this.selectedCurrency = null;
      this.isEditorOpened = true;
      this.allCurrencies = await this.getCurrencies(true);
    },

    moveCurrencyToMy(idx) {
      const currency = this.allCurrencies[idx];
      this.currencies.push(currency);
      this.allCurrencies.splice(idx, 1);

      this.$store.state.api.addCurrency(currency.name);
    },

    async notify(name) {
      const percents = await this.$store.state.modal.prompt(`При изменении ${name} на сколько процентов прислать уведомление?`);
      if (!percents)
        return;
      this.$store.state.popups.success("Хорошо, мы вас уведомим!");
      localStorage.setItem(name, percents);
    }
  }
}
</script>
