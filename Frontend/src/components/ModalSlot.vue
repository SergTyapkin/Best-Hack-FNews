<style lang="stylus" scoped>
  @require '../styles/constants.styl'
  @require '../styles/forms.styl'

  close-btn-size = 25px

  .modal
    position fixed
    top 0
    left 0
    width 100%
    height 100vh
    z-index 999
    display flex
    justify-content center
    align-items center

    .modal-background
      position fixed
      left 0
      top 0
      width 100%
      height 100vh

      background-color #00000080
      z-index -1
    .close-btn
      position absolute
      color textColor2
      right 20px
      top 10px
      width close-btn-size
      height close-btn-size
      transition all 0.3s ease
      cursor pointer
    .close-btn:hover
      color textColor1

    .plate
      position relative
      width 600px
      margin 0 60px
</style>
<template>
  <div class="modal" v-show="show" @keydown.esc="exit(false)">
    <div class="modal-background">
    </div>

    <div class="plate">
      <span class="close-btn" @click="exit(false)">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16"><path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/></svg>
      </span>

      <slot></slot>

    </div>
  </div>
</template>
<script>
  export default {
    props: {
      show: {
        type: Boolean,
        default: false,
      }
    },
    data() {
      return {
        show: this.showProp,
      }
    },

    methods: {
      exit() {
        this.show = false;
      }
    }
  }
</script>
