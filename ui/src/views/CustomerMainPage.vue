<template>
    <div class="home">
      <user-comp />
    </div>
  </template>
  
  <script>
  import UserComp from '../components/CustomerMainPage.vue'

  export default {
    name: 'Home',
    components: {
        UserComp
    }
  }
  </script>
  