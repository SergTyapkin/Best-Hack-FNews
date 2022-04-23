<style lang="stylus">
logo-size = 140px

.form
  .logo
    width logo-size
    margin-bottom 20px
</style>

<template>
  <BluredBg></BluredBg>

  <form class="form centered-horizontal" novalidate @submit.prevent="signIn">
    <img class="logo" src="../res/logo.svg" alt="BH Exchange" />

    <div class="info-container">
      <div class="title">Вход</div>
    </div>

    <div class="fields-container">
      <div>
        <span class="error-text">{{ errors.username }}</span>
        <input type="text" autocomplete="on" placeholder=" " v-model="username">
        <label>Логин</label>
      </div>
      <div>
        <span class="error-text">{{ errors.password }}</span>
        <input type="password" autocomplete="on" placeholder=" " v-model="password">
        <label>Пароль</label>
      </div>
    </div>

    <div class="submit-container">
      <input type="submit" value="Войти">
      <div class="text info">Ещё нет аккаунта?<router-link to="/signup"> Нажмите, чтобы создать.</router-link></div>
    </div>
  </form>
</template>


<script>
import BluredBg from '../components/BluredBG.vue'

export default {
  components: {BluredBg},

  data() {
    return {
      username: '',
      password: '',

      enabled: true,
      errors: {}
    }
  },

  methods: {
    async __signInAction() {
      if (this.username.length === 0) {
        this.errors.username = 'Логин не может быть пустым';
        return;
      }
      if (this.password.length === 0) {
        this.errors.password = 'Пароль не может быть пустым';
        return;
      }

      const response = await this.$store.state.api.signIn(this.username, this.password);
      if (response.ok_) {
        await this.$store.dispatch('GET_USER');
        await this.$router.push('/profile');
        this.$store.state.popups.success('Успешный вход!');
        return;
      }

      if (response.status_ === 403) {
        const error = 'Неверный логин или пароль';
        this.errors.username = error;
        this.errors.password = error;
      } else {
        this.$store.state.popups.error("Не удалось создать пользователя", 'Произошла неизвестная ошибка!');
      }
    },

    async signIn() {
      if (!this.enabled) {
        return;
      }
      this.enabled = false;

      this.errors = {};
      await this.__signInAction();

      this.enabled = true;
    },
  }
}
</script>
