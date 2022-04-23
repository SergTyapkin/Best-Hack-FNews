<style lang="stylus" scoped>
  @require '../styles/constants.styl'

  radius = radiusL
  borderColor = mix(textColorBlue, transparent)
  //width = 170px
  //height = 70px
  imageSize = 30px
  bg = mix(bgColor, transparent, 60%)
  bgSelected = linear-gradient(135deg, #40DDFF 0%, #14BAE3 19.24%, #13B1E6 68.64%, #11AADF 81.77%, #0B98C5 100%);

  colorIncrease = colorPlus
  colorDecrease = #E3507A
  colorIncreaseSelected = mix(colorIncrease, white, 30%)
  colorDecreaseSelected = mix(colorDecrease, white, 30%)

  .currency:not(.plain)
    margin-right 15px
    border 1px solid borderColor
    border-radius radius
    background bg
    transition background 0.2s ease
  .currency:not(.plain)hover
    background mix(bg, white, 80%)
  .currency.selected
    background bgSelected

  .currency
    display flex
    .img-col
      width 50px
      display flex
      align-items center
      justify-content center
      color #50E2C2
      font-size 30px
    .img-col.many-symbols
      font-size 15px

    .info-col
      flex 1
      display flex
      flex-direction column
      margin-left 10px
      margin-right 20px
      .value-row
        margin-top 15px
        .value
          font-size 15px
        .name
          padding-top 8px
          font-size 11px
          color textColor1
          opacity 0.7
          float right
      .perc-row
        margin-top 3px
        font-size 10px
        svg
          margin-top 3px
          width 7px
          display inline-block
          float right
        .perc
          line-height 20px
          margin-left 5px
          float right
        .graph
          float right
          height 40px
          margin-top -15px
      .perc-row.increase
        svg
          fill colorIncrease
        color colorIncrease
      .perc-row.decrease
        svg
          fill colorDecrease
        color colorDecrease

  .currency.selected
    .info-col
      .perc-row.increase
        svg
          fill colorIncreaseSelected
        color colorIncreaseSelected
      .perc-row.decrease
        svg
          fill colorDecreaseSelected
        color colorDecreaseSelected


</style>

<template>
  <div :class="'currency ' + (isSelected ? 'selected' : '') + (plainRender ? 'plain' : '')">
    <div :class="'img-col ' + (symbol.length > 1 ? 'many-symbols' : '')">
      {{ symbol }}
    </div>

    <div class="info-col">
      <div class="value-row">
        <span class="value">{{ value }}</span>
        <span class="name">{{ name }}</span>
      </div>
      <div :class="'perc-row ' + (isIncrease ? 'increase' : 'decrease')">
        <span class="perc">{{ isIncrease ? '+' : '-'}}{{ percentsAbs }}%</span>
        <svg v-if="isIncrease" viewBox="0 0 7 6" fill="white" xmlns="http://www.w3.org/2000/svg"><path d="M4.12165 3.81177L3.29433 4.63909C2.98972 4.9437 2.49585 4.9437 2.19124 4.63909C1.88663 4.33448 1.88663 3.84061 2.19124 3.536L3.01855 2.70868L0.840088 0.530212H6.30011V5.99024L4.12165 3.81177Z"/></svg>
        <svg v-else viewBox="0 0 7 6" fill="white" xmlns="http://www.w3.org/2000/svg"><path d="M3.95307 2.70861L3.12575 1.8813C2.82114 1.57669 2.32727 1.57669 2.02266 1.8813C1.71805 2.18591 1.71805 2.67978 2.02266 2.98439L2.84998 3.81171L0.671509 5.99017H6.13153V0.530148L3.95307 2.70861Z" fill="#E3507A"/></svg>

        <img class="graph" v-if="isIncrease" src="../res/graph_to_up.svg" alt="">
        <img class="graph" v-else src="../res/graph_to_down.svg" alt="">
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        isIncrease: this.percents >= 0,
        percentsAbs: Math.abs(this.percents),
        isSelected: this.isSelectedProp,
      };
    },

    props: {
      value: Number,
      name: String,
      percents: Number,
      symbol: String,
      isSelectedProp: {
        type: Boolean,
        default: false
      },
      plainRender: {
        type: Boolean,
        default: false
      },
    }
  }
</script>
