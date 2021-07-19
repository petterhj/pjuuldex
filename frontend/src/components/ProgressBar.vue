<template>
  <div class="progress-bar">
    <div
      :style="'width: '+progressPercent+'%'"
      class="progress"
    >
    </div>
    <div class="label">
      {{ collectedCount }}/{{ cardCount }} ({{progressPercent}} %)
    </div>
  </div>
</template>

<script>
export default {
  props: {
    cardCount: {
      type: Number,
      required: true
    },
    collectedCount: {
      type: Number,
      required: true
    }
  },
  computed: {
    progressPercent() {
      return Math.round((this.collectedCount / this.cardCount) * 100)
    }
  }
}
</script>

<style scoped>
.progress-bar {
  margin-top: 5px;
  position: relative;
  height: 1.25rem;
  background: #000;
  border-radius: 6px;
}
.progress-bar > div.progress {
  height: inherit;
  background: #0dd157;
  border-radius: inherit;
}
.progress-bar > div.label {
  position: absolute;
  top: 0;
  left: 0.5rem;
  color: white;
  font-size: 0.7rem;
}
</style>