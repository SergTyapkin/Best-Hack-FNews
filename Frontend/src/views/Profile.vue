<style lang="stylus">
  size = 96px
  .profile
    .avatar
      position relative
      width size
      margin 0 auto
      margin-bottom 5px
      .cover
        position absolute
        top 0
        width size
        height size
        line-height size
        border-radius (size / 2 - 1) // to fix avatar outside of div
        margin 0 auto
        color textColor1
        background-color clBackground
        opacity 0
        cursor pointer
        transition all 0.2s ease
      .cover:hover
        opacity 0.9
      img
        border-radius size
        width size
        height size
</style>

<template>
  <Logo />
  <div class="profile">
      <div class="standalone-form profile">
          <router-link to="/" class="back-btn">
              <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/></svg>
          </router-link>

          <div class="title">
              <div class="avatar">
                  <img v-if="avatarUrl" :src="avatarUrl" alt="">
                  <img v-else src="../images/cat_loading.gif" alt="">
                  <div class="cover">
                      Изменить
                  </div>
              </div>
              <div class="primary">{{ username }}</div>
          </div>
          <div class="form">
              <form novalidate>
                  <input name="avatarDataURL" type="hidden">

                  <div class="form-group">
                    <label>ЛОГИН<span class="error-text"></span></label>
                    <input name="username" type="text" class="form-control" :value="username" autocomplete="off" readonly>
                  </div>

                  <div class="form-group" :class="{ error: errorsInfo.fullname }" @input="errorsInfo.fullname = ''" @keydown.enter.prevent="updateUserInfo">
                      <label>ПОЛНОЕ ИМЯ<span class="error-text">{{ errorsInfo.fullname }}</span></label>
                      <input name="fullname" type="text" class="form-control" v-model="fullname" autocomplete="off">
                  </div>

                  <div class="form-group" :class="{ error: errorsInfo.email }" @input="errorsInfo.email = ''" @keydown.enter.prevent="updateUserInfo">
                      <label>EMAIL<span class="error-text">{{ errorsInfo.email }}</span></label>
                      <input name="reserveEmail" type="email" class="form-control" v-model="email" autocomplete="off">
                      <!-- <div class="muted">Необходимо будет подтвердить на старом и новом ящиках</div> -->
                  </div>

                  <div class="form-group">
                    <div class="btn" :class="{ 'btn-disabled': !enabledInfo}" @click="updateUserInfo">Сохранить</div>
                  </div>

                  <div class="roll-closed" ref="changePasswordFields" @keydown.enter.prevent="changePassword">
                    <div class="form-group" :class="{ error: errorsPassword.oldPassword }" @input="errorsPassword.oldPassword = ''">
                      <label>СТАРЫЙ ПАРОЛЬ<span class="error-text">{{ errorsPassword.oldPassword }}</span></label>
                      <input name="oldPassword" type="password" class="form-control" v-model="oldPassword" autocomplete="off">
                      <div class="muted">Если вы не задавали пароль - оставьте поле пустым</div>
                    </div>
                    <div class="form-group" :class="{ error: errorsPassword.newPassword }" @input="errorsPassword.newPassword = ''; errorsPassword.confirmPassword = ''">
                      <label>НОВЫЙ ПАРОЛЬ<span class="error-text">{{ errorsPassword.newPassword }}</span></label>
                      <input name="newPassword" type="password" class="form-control" v-model="newPassword" autocomplete="off">
                    </div>
                    <div class="form-group" :class="{ error: errorsPassword.confirmPassword }" @input="errorsPassword.newPassword = ''; errorsPassword.confirmPassword = ''">
                      <label>ПОДТВЕРЖДЕНИЕ<span class="error-text">{{ errorsPassword.confirmPassword }}</span></label>
                      <input name="newPassword" type="password" class="form-control" v-model="confirmPassword" autocomplete="off">
                    </div>
                  </div>

                  <div class="form-group">
                      <div class="btn" :class="{ 'btn-disabled': !enabledPassword}" @click="changePassword">Сменить пароль</div>
                  </div>

                  <div class="form-group">
                      <div @click="signOut" class="btn btn-danger">Выйти</div>
                  </div>
              </form>
          </div>
      </div>
  </div>
</template>


<script>
  import Logo from './Logo.vue'
  import {closeRoll, isClosedRoll, openRoll} from "../utils/show-hide";

  export default {
    components: { Logo },

    data() {
      return {
        username: this.$store.state.user.username,
        email: this.$store.state.user.email,
        avatarUrl: this.$store.state.user.avatarUrl,
        fullname: this.$store.state.user.fullname,

        oldPassword: '',
        newPassword: '',
        confirmPassword: '',

        errorsInfo: {},
        enabledInfo: true,

        errorsPassword: {},
        enabledPassword: true,
      }
    },

    methods: {
      async __updateUserInfoAction() {
        const response = await this.$store.state.api.updateUser({
          email: this.email,
          fullname: this.fullname,
        })

        if (response.ok_) {
          this.$store.state.popups.success("Данные успешно изменены")
          // todo: update data without getting user
          await this.$store.dispatch('GET_USER')
          return
        }

        const status = response.status_;
        if (status === 400) {
          this.errorsInfo.fullname = 'Некорректное полное имя!'
          this.errorsInfo.email = 'Или некорректный email... Мы точно не знаем)'
        } else {
          this.$store.state.popups.error('Не удалось изменить данные', 'Произошла непредвиденная ошибка!')
        }
      },


      async updateUserInfo() {
        if (!this.enabledInfo) {
          return
        }
        this.enabledInfo = false

        this.errorsInfo = {}
        await this.__updateUserInfoAction()

        this.enabledInfo = true
      },


      async signOut() {
        const response = await this.$store.state.api.signOut()
        if (!response.ok_) {
          this.$store.state.popups.error("Не удалось выйти из аккаунта", 'Произошла непредвиденная ошибка')
          return
        }

        await this.$store.dispatch('DELETE_USER')
        await this.$router.push('/signin')
        this.$store.state.popups.success('Вы успешно вышли из аккаунта')
      },


      async __changePasswordAction() {
        if (this.newPassword.length === 0) {
          this.errorsPassword.newPassword = 'Пароль не может быть пустым'
          return
        }
        if (this.newPassword !== this.confirmPassword) {
          const error = 'Пароли не совпадают'
          this.errorsPassword.newPassword = error
          this.errorsPassword.confirmPassword = error
          return
        }

        const response = await this.$store.state.api.updatePassword(this.oldPassword, this.newPassword);
        if (response.ok_) {
          this.oldPassword = ''
          this.newPassword = ''
          this.confirmPassword = ''
          this.$store.state.popups.success("Пароль успешно изменен")
          closeRoll(this.$refs.changePasswordFields)
          return
        }

        const status = response.status_
        if (status === 400) {
          this.errorsPassword.oldPassword = 'Неверный старый пароль'
        } else {
          this.$store.state.popups.error('Не удалось изменить пароль', 'Произошла непредвиденная ошибка')
        }
      },


      async changePassword() {
        if (isClosedRoll(this.$refs.changePasswordFields)) {
          openRoll(this.$refs.changePasswordFields);
          return;
        }

        if (!this.enabledPassword) {
          return
        }
        this.enabledPassword = false

        this.errorsPassword = {}
        await this.__changePasswordAction()

        this.enabledPassword = true
      }
    },
  }
</script>
