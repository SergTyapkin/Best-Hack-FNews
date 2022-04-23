<style lang="stylus" scoped>
@require '../styles/constants.styl'

new-margin = 35px
stats-width = 200px

.page-name
  font-size 45px
  margin 30px 0 40px 80px

.bg
  position absolute
  inset 0
  background #000
  opacity 0.6
  z-index -1

.columns-flex-container
  display flex
  flex-direction row
  text-align left

.news-flex-container
  display flex
  flex-wrap wrap
  padding 80px
  padding-top 0
  .new
    min-width 150px
    max-width 'calc(50% - %s)' % (new-margin * 2)
    margin new-margin
  .new:nth-child(6n+1)
  .new:nth-child(6n+2)
  .new:nth-child(6n+5)
    max-width 'calc(33% - %s)' % (new-margin * 2)
  .new:nth-child(6n)
    max-width 'calc(100% - %s)' % (new-margin * 2)
  .new.first-string
    max-width 'calc(50% - %s - %s)' % ((new-margin * 2) (stats-width / 2))
  .stats
    width stats-width
    height 300px
</style>

<template>
  <BluredBG></BluredBG>

  <TopBar></TopBar>

  <div class="bg"></div>

  <div class="page">
    <div class="page-name">Новости</div>

    <div class="news-flex-container">
      <New v-for="curNew in news.slice(0, 2)" :data="curNew" class="new first-string"></New>
      <Stats class="stats"></Stats>
      <New v-for="curNew in news.slice(2, news.length)" :data="curNew" class="new"></New>
    </div>
  </div>
</template>


<script>
import BluredBG from "../components/BluredBG.vue";

import TopBar from "../components/TopBar.vue";
import Balance from "../components/Balance.vue";
import New from "../components/New.vue";
import Stats from "../components/Stats.vue";

export default {
  components: {TopBar, BluredBG, Balance, New, Stats},
  data() {
    return {
      news: [],
    }
  },

  async mounted() {
    this.news = await this.getNews();
  },

  methods: {
    async getNews() {
      const news = await this.$store.state.api.getNews();
      if (!news.ok_) {
        this.$store.state.popups.error('Не удалось получить новости');
        return [];
      }
      return news.news;
    },
  }
}
</script>
