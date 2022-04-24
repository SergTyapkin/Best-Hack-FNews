<style lang="stylus" scoped>
  @require '../../styles/constants.styl'

  cross-size = 20px
  cross-lines-width = 14%
  cross-color = colorMinus
  .cross {
    width cross-size
    height cross-size
    transform: rotate(45deg);
    position: relative;
    display: inline-block;
    transition all 0.3s ease
    border-radius 50%
  }
  .cross:hover
    transform: rotate(135deg) scale(1.1);
  .cross:hover::before,
  .cross:hover:after
    background cross-color

  .cross::before, .cross:after {
    content: "";
    position: absolute;
    z-index: -1;
    background: cross-color;
  }
  .cross::before {
    top: 0;
    left: 50%;
    width: cross-lines-width;
    margin-left (- cross-lines-width / 2)
    height: 100%;
  }
  .cross:after {
    top: 50%;
    left: 0;
    height: cross-lines-width;
    margin-top (- cross-lines-width / 2)
    width: 100%;
  }

  .btn.delete
    display flex
    align-content center
    justify-content center
    background color3
    padding 8px
  .btn.delete:hover
    background color4

  .top-row
    display flex

  input
    flex 1
    width 100%
    padding 10px
    box-sizing border-box
    float left
  .radio
    margin-left 20px
    margin-right 5px
  .button
    opacity 1
    transition all 0.3s ease
    overflow hidden
    height 40px
    box-sizing border-box
    float right
    display flex
    align-content center
    justify-content center
    .arrow.right
      margin-left 5px
  div:last-child
    width 20%
    margin-left 20px
  div:not(:last-child)
    margin-right 20px
  div.closed
    opacity 0
    width 0
    padding-left 0
    padding-right 0
    margin-left 0
    margin-right 0
    pointer-events none
  .orderid
    display flex
    align-items center
    margin-right 5px
    color textColor1
    font-size 20px
  .move-buttons
    .button
      padding 0 15px

  .form
    .top-row
      position relative
      input
        font-size 20px
      .author
        color textColor5
        font-size 14px
        position absolute
        right 0
        top 0
    textarea
      all unset
      width 100%
      padding 10px
      font-size 14px
      height 80px
</style>

<template>
  <div class="top-row">
<!--    <span class="orderid">{{ idx }}</span>-->
    <div class="btn delete" @click="$emit('deleteListItem', idx)"><span class="cross"></span></div>
    <input type="text" placeholder="Название топика" ref="input1" :value="modelValue.name" @input="updateVModel" @change="updateOnServer" :disabled="modelValue.readonly">
    <span class="author">{{ modelValue.author }}</span>
  </div>
  <textarea placeholder="Ключевые слова (через запятую)" ref="input2" :value="modelValue.keys" @input="updateVModel" @change="updateOnServer" :disabled="modelValue.readonly"
            @keydown.tab="addItemIfLast" class="scrollable"></textarea>
</template>

<script>
  export default {
    props: {
      idx: Number,
      modelValue: {name: '', keys: ''}, // aka "item"
      readonly: Boolean
    },

    methods: {
      updateVModel() {
        this.$emit('update:modelValue', {name: this.$refs.input1.value, keys: this.$refs.input2.value});
      },
      addItemIfLast(e) {
        if (!e.target.parentElement.nextElementSibling)
          this.$parent.addItem();
      },

      async updateOnServer() {
        const item = this.modelValue;
        const res = await this.$store.state.api.updateTopic(item.id, item.name, item.keys);
        if (res.ok_) {
          return;
        }
        this.$store.state.popups.error("Ошибка при обновлении. Изменения не сохранены");
      }
    }
  }
</script>
