<template>
  <div class="complex">
    <iframe :src="src" ref="iframe" frameborder="0"></iframe>
  </div>
</template>

<script>
export default {
  name: "Complex",
  data(){
    return {
      src: '../../../static/complex.html'
    }
  }
}
</script>

<style scoped>
iframe {
  width: 100%;
  height: 94vh;
  margin: 0 auto;
  display: block;
}
</style>
