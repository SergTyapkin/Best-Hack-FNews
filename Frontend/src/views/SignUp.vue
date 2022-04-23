<template>
  <BluredBg></BluredBg>

  <form class="form centered-horizontal" novalidate @submit.prevent="signUp">
    <img class="logo" src="../res/logo.svg" alt="FNews" />

    <div class="info-container">
      <div class="title">Создать аккаунт</div>
    </div>

    <div class="fields-container">
      <div>
        <span class="error-text">{{ errors.username }}</span>
        <input type="text" autocomplete="on" placeholder=" " v-model="user.username">
        <label>Логин</label>
      </div>
      <div>
        <span class="error-text">{{ errors.name }}</span>
        <input type="text" autocomplete="on" placeholder=" " v-model="user.name">
        <label>Ваше имя</label>
      </div>
      <div>
        <span class="error-text">{{ errors.email }}</span>
        <input type="email" autocomplete="on" placeholder=" " v-model="user.email">
        <label>Email</label>
      </div>
      <div>
        <span class="error-text">{{ errors.password }}</span>
        <input type="password" autocomplete="on" placeholder=" " v-model="user.password">
        <label>Пароль</label>
      </div>
      <div>
        <span class="error-text">{{ errors.passwordConfirm }}</span>
        <input type="password" autocomplete="on" placeholder=" " v-model="passwordConfirm">
        <label>Подтверждение пароля</label>
      </div>
    </div>

    <div class="submit-container">
      <input type="submit" value="Создать аккаунт">
      <div class="text info">Уже есть аккаунт? <router-link to="/signin">Нажмите, чтобы войти.</router-link></div>
    </div>
  </form>
</template>


<script>
import BluredBg from '../components/BluredBG.vue'
import User from "../models/user";

export default {
  components: {BluredBg},

  data() {
    return {
      user: new User(),
      passwordConfirm: '',

      enabled: true,
      errors: {}
    }
  },

  methods: {
    async __signUpAction() {
      if (this.user.username.length === 0) {
        this.errors.username = 'Логин не может быть пустым';
        return;
      }
      if (this.user.firstName.length === 0) {
        this.errors.firstName = 'Имя не может быть пустым';
        return;
      }
      if (this.user.password.length === 0) {
        this.errors.password = 'Пароль не может быть пустым';
        return;
      }
      if (this.user.password !== this.passwordConfirm) {
        this.errors.password = 'Пароли не совпадают';
        this.errors.passwordConfirm = 'Пароли не совпадают';
        return;
      }

      const userInfo = await this.$store.state.api.signUp(this.user.toNetwork());
      if (userInfo.ok_) {
        this.$store.state.popups.success("Добро пожаловать!", `Пользователь ${this.username} успешно создан!`);
        await this.$store.dispatch('GET_USER');
        await this.$router.push('/profile');
        return;
      }

      if (userInfo.status_ === 409) {
        this.errors.username = 'Такой логин уже занят(';
        this.errors.email = 'Или EMail уже занят... Мы точно не знаем)';
        return;
      }
      this.$store.state.popups.error("Не удалось создать пользователя", 'Произошла неизвестная ошибка!');
    },

    async signUp() {
      if (!this.enabled) {
        return;
      }
      this.enabled = false;

      this.errors = {};
      await this.__signUpAction();

      this.enabled = true;
    },
  }
}
</script>
