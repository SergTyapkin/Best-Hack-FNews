<style lang="stylus" scoped>
@require '../styles/constants.styl'

photo-size = 180px
photo-column-width = 300px

borderColorInputs = textColor5

.profile-page
  position relative
  display flex
  padding-right 60px
  padding-bottom 20px

.page-name
  position absolute
  top -40px
  right 95px

.photo-column
  width photo-column-width
.info-column
  flex 1

.photo-column
  width photo-column-width
  .photo
    margin 0 auto
    opacity 0.6
    position relative
    width photo-size
    height photo-size
    display flex
    align-items center
    justify-content center
    img
      width 50%
  .photo::before
    content ""
    position absolute
    inset 0
    border-radius 50%
    border 1px solid white


.info-column
  .title
    margin-bottom 40px
  .inputs
    margin-left 30px
    font-size 14px
    max-width 500px
    > div
      display flex
      align-items center
      margin-bottom 20px
      label
        width 150px
      input
        all unset
        flex 1
        height 35px
        padding 5px 10px
        box-sizing border-box
        background mix(bgColor, transparent, 60%)
        border 1px solid borderColorInputs
        border-radius radiusS

    button
      all unset
      margin-top 20px
      float right
      width 120px
      background bgColor3
      padding 7px
      box-sizing border-box
      text-align center
      cursor pointer
      border-radius radiusS
</style>

<template>
  <BluredBG></BluredBG>

  <div class="profile-page">
    <div class="page-name">Your profile</div>

    <div class="photo-column">
      <div class="photo">
        <img src="../res/favicon.ico" alt="Photo">
      </div>
    </div>

    <div class="info-column">
      <div class="title">Personal information</div>
      <div class="inputs">
        <div><label>Username</label> <input v-model="user.username" type="text"/></div>
        <div><label>First name</label> <input v-model="user.firstName" type="text"/></div>
        <div><label>Last name</label> <input v-model="user.secondName" type="text"/></div>
        <div><label>Email</label> <input v-model="user.email" type="text"/></div>
        <div><label>Address</label> <input v-model="user.address" type="text"/></div>
        <div><label>Phone number</label> <input v-model="user.phone" type="text"/></div>
        <div><label>Date of birth</label> <input v-model="user.birthdate" type="text"/></div>
        <button @click="changeData">Submit</button>
      </div>
    </div>
  </div>
</template>


<script>
import BluredBG from "../components/BluredBG.vue";

import User from "../models/user";


export default {
  components: {BluredBG},
  data() {
    return {
      user: new User(),

      enabled: true,
      errors: {}
    }
  },

  mounted() {
    this.user.set(this.$store.state.user);
  },

  methods: {
    // TODO: Нормальная проверка всех полей
    async __signInAction() {
      if (this.username.length === 0) {
        this.errors.username = 'Логин не может быть пустым';
        return;
      }
      if (this.username.firstName === 0) {
        this.errors.firstName = 'Имя не может быть пустым';
        return;
      }
      if (this.email.length === 0) {
        this.errors.email = 'Email не может быть пустым';
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
    }
  }
}
</script>
