<style lang="stylus">
</style>

<template>
<!--  <Logo />-->

  <div class="signup">
    <div class="content">
      <div class="standalone-form">
        <div class="title">
          <div class="primary">Регистрация</div>
        </div>
        <div class="form" @keydown.enter.prevent="signUp">
          <form novalidate>
            <div class="form-group" :class="{ error: errors.username }" @input="errors.username = ''">
              <label>ЛОГИН*<span class="error-text">{{ errors.username }}</span></label>
              <input v-model="username" type="text" class="form-control" required autocomplete="on">
              <div class="muted">Минимум 3 символа, только буквы, цифры и _</div>
            </div>

            <div class="form-group" :class="{ error: errors.email }" @input="errors.email = ''">
              <label>EMAIL*<span class="error-text">{{ errors.email }}</span></label>
              <input v-model="email" type="email" class="form-control" placeholder="wolf@liokor.ru" autocomplete="on">
              <div class="muted">Используется для восстановления пароля, если не указан - восстановить пароль крайне сложно</div>
            </div>

            <div class="form-group" :class="{ error: errors.password }" @input="errors.password = ''">
              <label>ПАРОЛЬ*<span class="error-text">{{ errors.password }}</span></label>
              <input v-model="password" type="password" class="form-control" required autocomplete="off">
              <div class="muted">В пароле должно быть много всяких символов, но его надо не забыть</div>
            </div>

            <div class="form-group" :class="{ error: errors.passwordConfirm }" @input="errors.passwordConfirm = ''">
              <label>ПОДТВЕРЖДЕНИЕ ПАРОЛЯ*<span class="error-text">{{ errors.passwordConfirm }}</span></label>
              <input v-model="passwordConfirm" type="password" class="form-control" required autocomplete="off">
            </div>

            <div class="form-group" :class="{ error: errors.fullname }" @input="errors.fullname = ''">
              <label>ПОЛНОЕ ИМЯ<span class="error-text">{{ errors.fullname }}</span></label>
              <input v-model="fullname" type="text" class="form-control" placeholder="Иван Иванов" autocomplete="on">
            </div>

            <div class="form-group">
              <div class="btn" :class="{ 'btn-disabled': !enabled }" @click="signUp" >Создать</div>
              <div class="muted">Уже с нами? <router-link to="/signin" class="router-link">Войти</router-link></div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Logo from './Logo.vue'

  export default {
    components: { Logo },

    data() {
      return {
        username: "",
        email: "",
        password: "",
        passwordConfirm: "",
        fullname: "",

        enabled: true,

        errors: {}
      }
    },

    methods: {
      async __signUpAction() {
        if (this.username.length === 0) {
          this.errors.username = 'Логин не может быть пустым'
          return
        }
        if (this.password.length === 0) {
          this.errors.password = 'Пароль не может быть пустым'
          return
        }

        if (this.password !== this.passwordConfirm) {
          this.errors.password = 'Пароли не совпадают'
          this.errors.passwordConfirm = 'Пароли не совпадают'
          return;
        }

        const response = await this.$store.state.api.signUp(this.username, this.email, this.password, this.fullname);
        if (response.ok_) {
          this.$store.state.popups.success("Добро пожаловать!", `Пользователь ${this.username} успешно создан!`);
          await this.$store.dispatch('GET_USER');
          await this.$router.push('/profile');
          return;
        }

        const status = response.status_

        if (status === 409) {
          this.errors.username = 'Такой логин уже занят('
          this.errors.email = 'Или EMail уже занят... Мы точно не знаем)'
        } else {
          this.$store.state.popups.error("Не удалось создать пользователя", 'Произошла неизвестная ошибка!');
        }
      },

      async signUp() {
        if (!this.enabled) {
          return
        }
        this.enabled = false;

        this.errors = {}
        await this.__signUpAction();

        this.enabled = true;
      }
    }
  }
</script>
