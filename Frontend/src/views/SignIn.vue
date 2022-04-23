<style lang="stylus">
</style>

<template>
  <Logo />

  <div class="auth">
    <div class="content">
      <div class="standalone-form">
        <div class="title">
          <div class="primary">Вход</div>
          <div class="secondary">Рады видеть вас снова!</div>
        </div>
        <div class="form" @keydown.enter.prevent="signIn">
          <form novalidate>
            <div class="form-group" :class="{ error: errors.username }" @input="errors.username = ''">
              <label>ЛОГИН<span class="error-text">{{ errors.username }}</span></label>
              <input v-model="username" type="text" class="form-control" required autocomplete="on">
            </div>
            <div class="form-group" :class="{ error: errors.password }" @input="errors.password = ''">
              <label>ПАРОЛЬ<span class="error-text">{{ errors.password }}</span></label>
              <input v-model="password" type="password" class="form-control" required autocomplete="on">
              <!-- <div class="muted"><linkButton href="#">Забыли пароль?</linkButton> -->
            </div>
            <div class="form-group">
              <div class="btn" :class="{ 'btn-disabled': !enabled }" @click="signIn">Войти</div>
              <div class="muted">Нужен аккаунт? <router-link to="/signup" class="router-link">Создать</router-link></div>
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
        password: "",

        enabled: true,

        errors: {}
      }
    },

    methods: {
      async __signInAction() {
        if (this.username.length === 0) {
          this.errors.username = 'Логин не может быть пустым!'
          return;
        } else if (this.password.length === 0) {
          this.errors.password = 'Пароль не может быть пустым!'
          return
        }

        const response = await this.$store.state.api.signIn(this.username, this.password);
        if (response.ok_) {
          await this.$store.dispatch('GET_USER')
          await this.$router.push('/profile')
          this.$store.state.popups.success('Успешный вход!')
          return
        }

        const status = response.status_;
        if (status === 403) {
          const error = 'Неверный логин или пароль'
          this.errors.username = error
          this.errors.password = error
        } else {
          this.$store.state.popups.error('Не удалось войти!', 'Произошла непредвиденная ошибка!')
        }
      },

      async signIn() {
        if (!this.enabled) {
          return;
        }
        this.enabled = false;

        this.errors = {}
        await this.__signInAction();

        this.enabled = true;
      }
    }
  }
</script>
