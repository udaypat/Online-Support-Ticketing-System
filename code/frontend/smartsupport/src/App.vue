<template>
  <div id="app">
    <router-view :key="$route.params[$route.meta.watchParam]" />
  </div>
</template>


<script>
export default {
  name: "App",
};
</script>
