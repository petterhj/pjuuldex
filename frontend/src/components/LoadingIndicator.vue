<template>
  <div class="loading-bar"></div>
</template>

<style scoped>
@keyframes progress-animation {
  0% {
    background-position: 100%;
  }
  100% {
    background-position: 0;
  }
}
.loading-bar {
  position: absolute;
  top: 0px;
  height: 5px;
  width: 100%;
  background: linear-gradient(90deg, rgba(15,121,9,1) 0%, rgba(15,121,9,1) 35%, rgba(0,255,46,1) 50%, rgba(15,121,9,1) 65%, rgba(15,121,9,1) 100%);
  background-size: 300% 100%;
  -webkit-animation: progress-animation 2s linear infinite;
          animation: progress-animation 2s linear infinite;
}
</style>