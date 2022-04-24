<style lang="stylus" scoped>
@require '../styles/constants.styl'

.title
  font-size 18px
  font-weight bold
  margin-bottom 8px
.meta-string
  font-size 12px
  color textColor5
  .date
    margin-right 5px
  .source
    margin-right 8px
  .tag
    color textColor1
    background #E3507A80
    padding 2px 4px
    border-radius 2px
    margin-right 5px
.description
  margin-top 16px
  color textColor2
  font-size 14px
</style>

<template>
  <div class="new" @click="openFull(data.title, data.description)">
    <div class="title">{{ data.title }}</div>
    <div class="meta-string">
      <span class="date">{{ data.date }}</span>
      <span class="source">{{ data.source }}</span>
      <span class="tag" v-for="tag in data.tags">{{ tag }}</span>
    </div>
    <div class="description">
      {{ data.description256 }}
    </div>
  </div>
</template>


<script>
export default {
  props: {
    data: {}
  },

  methods: {
    openFull(title, text) {
      this.$store.state.modal.alert(title, text);
    }
  }
}
</script>
