<style lang="stylus" scoped>
@require '../styles/constants.styl'

height = 20%

.toolbar
  height height
  display flex
  align-items center
  justify-content space-between

  .logo
    width 200px
    height 80px

  .right-container
    display flex
    margin-right 80px
    .icon
      opacity 0.6
      position relative
      width 50px
      margin-left 30px
      height 50px
      display flex
      align-items center
      justify-content center
      transition opacity 0.2s ease
      img
        width 20px
    .icon::before
      content ""
      position absolute
      inset 0
      border-radius 50%
      border 2px solid white
      cursor pointer
    .icon:hover
      opacity 1


  .abs-container
    position relative
    input
      all unset
      height 45px
      width 330px
      padding 10px 40px 10px 14px
      box-sizing border-box
      border 1px solid textColor5
      border-radius radiusM
      color textColor1
      font-size 16px
    input + .search
      position absolute
      right 0
      margin 10px
      width 25px
      opacity 0.6
</style>

<template>
  <div class="toolbar">
    <img class="logo" src="../res/logo.svg" alt="Logo" />
    <div class="right-container">
      <div class="abs-container">
        <input v-model="searchText" type="search" placeholder="поиск" />
        <img class="search" src="../res/search.svg" alt="" />
      </div>

      <router-link to="#" class="icon"><img src="../res/bell.svg" alt="" /></router-link>
      <router-link to="/profile" class="icon"><img src="../res/profile.svg" alt="" /></router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchText: '',
    };
  },
};
</script>
