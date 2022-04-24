<style lang="stylus" scoped>
@require '../styles/constants.styl'

.page-name
  font-size 40px
  margin 30px 0 40px 80px

.svg-button
  width 40px

.submit-buttons
  justify-content flex-end
  padding-bottom 100px
  margin-right 100px
  .button
    margin 0
</style>

<template>
  <BluredBG></BluredBG>

  <TopBar></TopBar>

  <div class="page">
    <div class="page-name">
      <router-link to="/"><img class="svg-button" src="../res/arrow_left.svg" alt="setup"></router-link>
      Настройка предпочтений
    </div>

    <AddableList :model-value="topics"></AddableList>

    <div class="submit-buttons">
<!--      <button class="button" @click="sendList">Сохранить</button>-->
    </div>
  </div>
</template>


<script>
import BluredBG from "../components/BluredBG.vue";

import TopBar from "../components/TopBar.vue";
import Balance from "../components/Balance.vue";
import New from "../components/New.vue";
import Stats from "../components/Stats.vue";
import AddableList from "../components/AddableList/AddableList.vue";

export default {
  components: {AddableList, TopBar, BluredBG, Balance, New, Stats},
  data() {
    return {
      topics: [],
    }
  },

  async mounted() {
    this.topics = await this.getTopics();
    this.topics.forEach(topic => topic.readonly = topic.author !== this.$store.state.user.username);
    console.log(this.topics)
  },

  methods: {
    async getTopics() {
      const list = await this.$store.state.api.getTopics();
      if (!list.ok_) {
        this.$store.state.popups.error('Не удалось получить темы');
        return [];
      }
      return list.topics;
    },

    async sendList() {
      const res = await this.$store.state.api.put();
      if (!res.ok_) {
        this.$store.state.popups.error('Не удалось сохранить');
        return;
      }
    }
  }
}
</script>
