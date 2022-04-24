<style lang="stylus" scoped>
  @require '../../styles/constants.styl'

  .addable-list
    padding 0
    margin 0 100px
    list-style none
    > li
      margin-top 10px
      margin-bottom 10px
      justify-content space-between
      align-items center

      :last-child
        margin-bottom 0
      :first-child
        margin-top 0
    > li:first-child
      > .move-buttons
        > .button:first-child
          opacity 0.2
          pointer-events none
    > li:last-child
      > .move-buttons
        > .button:last-child
          opacity 0.2
          pointer-events none

  .btn.delete
    display flex
    align-content center
    justify-content center
    background color3
    padding 8px
  .btn.delete:hover
    background color4
  .btn.thin
    padding-top 2px
    padding-bottom 2px

.form
  text-align left
  margin 10px 0
  max-width unset
  padding 20px 40px
.add-button
  display flex
  align-items center
  justify-content center
  border 1px solid white
  width fit-content
  margin 0 auto
  padding 7px
  padding-right 12px
  border-radius 30px
  opacity 0.7
  transition all 0.2s ease
  cursor pointer
  > img
    width 40px
    transition all 0.2s ease
.add-button:hover
  opacity 1
  > img
    transform scale(1.1)

</style>

<template>
  <ul class="addable-list" @input="">
    <li v-for="(item, idx) in modelValue" class="form">
      <ListItem v-model="modelValue[idx]" :idx="idx + 1" @deleteListItem="deleteItem"></ListItem>
    </li>
    <li>
      <div class="add-button" @click="addItem">
        <img src="../../res/plus.svg" alt="add">
        Добавить тему
      </div>
    </li>
  </ul>
</template>

<script>
  import ListItem from "./ListItem.vue";

  export default {
    components: {ListItem},
    props: {
      modelValue: [], // aka "items"
    },

    mounted() {
    },

    methods: {
      async addItem() {
        const topic = {name: "", keys: ""};

        const res = await this.$store.state.api.createTopic(topic.name, topic.keys);
        if (!res.ok_) {
          this.$store.state.popups.error("Не удалось создать тему");
          return;
        }
        topic.id = res.id;
        this.modelValue.push(topic);
        this.updateVModel();
      },

      async deleteItem(idx) {
        const topic = this.modelValue[idx];

        const res = await this.$store.state.api.deleteTopic(topic.id);
        if (!res.ok_) {
          this.$store.state.popups.error("Не удалось удалить тему");
          return;
        }
        this.modelValue.splice(idx - 1, 1);
        this.updateVModel();
      },

      updateVModel() {
        this.$emit('update:modelValue', this.modelValue);
      }
    }
  }
</script>
