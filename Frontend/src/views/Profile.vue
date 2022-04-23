<style lang="stylus" scoped>
@require '../styles/constants.styl'

photo-size = 180px
photo-column-width = 300px

borderColorInputs = textColor5
borderColorInputsFocus = textColor2

.profile-page
  text-align center

.page-name
  font-size 28px
  margin-bottom 60px

.plate
  padding 20px 20px
  background mix(bgColor, transparent, 60%)
  border 1px solid borderColorInputs
  border-radius radiusS


.columns-flex-container
  display flex
  flex-direction row
  text-align left

.photo-column
  width photo-column-width
.history-column
.info-column
  flex 1

.info-column
  margin-right 40px
  margin-left 80px
  .inputs
    font-size 18px
    max-width 500px
    > div
      display flex
      align-items center
      margin-bottom 25px
      label
        width 130px
      input
        outline none
        flex 1
        height 35px
        color textColor1
        padding 5px 10px
      input:focus
        border-color borderColorInputsFocus

    .buttons
      display flex
      justify-content space-between
      button
        all unset
        margin-top 20px
        float right
        width 120px
        background bgColor3
        padding 7px
        text-align center
        cursor pointer
        border-radius radiusS
      button:first-child
        background bgColor2

.history-column
  margin-left 40px
  margin-right 100px
  font-size 15px
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
  .history-plate
    margin-top 10px
    padding 30px
    border-radius radiusL
    .title
      text-align center
      margin-bottom 20px
    .operation
      font-size 16px
      padding 10px 20px
      display flex
      align-items center
    .operation:not(:last-child)
      border-bottom solid 1px textColor4
    .operation
      .left
        .date
          color textColor3
          font-size 14px
          line-height 20px
      .right
        flex 1
        text-align right
        height fit-content
      .right.plus
        color #50E3C2
      .right.minus
        color #FF3F3F
</style>

<template>
  <BluredBG></BluredBG>

  <TopBar></TopBar>

  <div class="profile-page">
    <div class="page-name">Личный кабинет</div>

    <div class="columns-flex-container">
      <div class="info-column">
        <div class="inputs">
          <div><label>Логин</label> <input v-model="user.username" type="text" class="plate"/></div>
          <div><label>Имя</label> <input v-model="user.name" type="text" class="plate"/></div>
          <div><label>Email</label> <input v-model="user.email" type="email" class="plate"/></div>
          <div><label>Пароль</label> <input v-model="user.password" type="password" class="plate"/></div>
          <div class="buttons">
            <button @click="logOut">Выйти</button>
            <button @click="changeData">Изменить</button>
          </div>
        </div>
      </div>

      <div class="history-column">
        <Balance></Balance>

        <div class="plate history-plate">
          <div class="title">Последние операции</div>
          <div class="operation" v-for="operation in operations">
            <div class="left">
              <div class="action">{{operation.action === 'topup' ? 'Покупка' : 'Продажа'}}</div>
              <div class="date">{{operation.date}}</div>
            </div>
            <div :class="'right ' + (operation.action === 'topup' ? 'plus' : 'minus')">
              {{operation.message}}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import BluredBG from "../components/BluredBG.vue";

import User from "../models/user";
import TopBar from "../components/TopBar.vue";
import Balance from "../components/Balance.vue";

export default {
  components: {TopBar, BluredBG, Balance},
  data() {
    return {
      user: new User(),
      operations: [],

      enabled: true,
      errors: {},
    }
  },

  async mounted() {
    this.user.set(this.$store.state.user);
    this.operations = await this.getHistory();
  },

  methods: {
    async __signInAction() {
      if (this.user.username.length === 0) {
        this.errors.username = 'Логин не может быть пустым';
        return;
      }
      if (this.user.name.length === 0) {
        this.errors.name = 'Имя не может быть пустым';
        return;
      }
      if (this.user.email.length === 0) {
        this.errors.email = 'Email не может быть пустым';
        return;
      }
      if (this.user.password.length === 0) {
        this.errors.password = 'Введите пароль';
        return;
      }

      const response = await this.$store.state.api.updateUser(this.user.toNetwork());
      if (response.ok_) {
        await this.$store.dispatch('GET_USER');
        this.$store.state.popups.success('Данные обновлены');
        return;
      }

      if (response.status_ === 409) {
        this.errors.email = 'Такой email уже занят';
      } else {
        this.$store.state.popups.error("Не удалось обновить данные", 'Произошла неизвестная ошибка!');
      }
    },

    async changeData() {
      if (!this.enabled) {
        return;
      }
      this.enabled = false;

      await this.__signInAction();

      this.enabled = true;
    },

    async getHistory() {
      const operations = await this.$store.state.api.getHistory();
      if (!operations.ok_) {
        this.$store.state.popups.error('Не удалось получить историю действий');
        return [];
      }
      return operations.actions;
    },

    async logOut() {
      const response = await this.$store.state.api.signOut();
      if (!response.ok_) {
        this.$store.state.popups.error('Не получилось выйти из аккаунта', 'Неизвестная ошибка');
        return;
      }
      await this.$router.push('/');
    }
  }
}
</script>
