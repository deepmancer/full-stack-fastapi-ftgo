<template>
  <div dir="rtl" class="change-restaurant-info-page">
    <section class="change-restaurant-info">
      <div class="container">
        <div class="change-restaurant-info-content">

          <div class="change-restaurant-info-form">
            <h2 class="form-title">اطلاعات رستوران</h2>
            <form class="register-form" id="register-form" @submit.prevent="registerRestaurant">
              <b-input-group class="mt-3">
                <template #prepend>
                  <b-input-group-text>
                    <font-awesome-icon icon="fa-solid fa-store" />
                  </b-input-group-text>
                </template>
                <b-form-input placeholder="نام رستوران" v-model="restaurantName" required></b-form-input>
              </b-input-group>
              <b-input-group class="mt-3">
                <template #prepend>
                  <b-input-group-text>
                    <font-awesome-icon icon="fa-solid fa-map-marker-alt" />
                  </b-input-group-text>
                </template>
                <b-form-input placeholder="کد پستی رستوران" v-model="postalCode" required></b-form-input>
              </b-input-group>
              <b-input-group class="mt-3">
                <template #prepend>
                  <b-input-group-text>
                    <font-awesome-icon icon="fa-solid fa-map-marker-alt" />
                  </b-input-group-text>
                </template>
                <b-form-input placeholder="آدرس رستوران" v-model="restaurantAddress" required></b-form-input>
              </b-input-group>
              <b-input-group class="mt-3">
                <template #prepend>
                  <b-input-group-text>
                    <font-awesome-icon icon="fa-solid fa-map-marker-alt" />
                  </b-input-group-text>
                </template>
                <b-form-input placeholder="عرض جغرافیایی رستوران" v-model="restaurantLat" required></b-form-input>
              </b-input-group>
              <b-input-group class="mt-3">
                <template #prepend>
                  <b-input-group-text>
                    <font-awesome-icon icon="fa-solid fa-map-marker-alt" />
                  </b-input-group-text>
                </template>
                <b-form-input placeholder="طول جغرافیایی رستوران" v-model="restaurantLng" required></b-form-input>
              </b-input-group>
              <b-input-group class="mt-3">
                <template #prepend>
                  <b-input-group-text>
                    <font-awesome-icon icon="fa-solid fa-id-card" />
                  </b-input-group-text>
                </template>
                <b-form-input placeholder="شناسه مجوز رستوران" v-model="restaurantLicenceId" required></b-form-input>
              </b-input-group>

              <div class="form-group form-button mt-5">
                <b-button variant="secondary" type="submit">
                  <b-spinner v-if="loading" label="Spinning"></b-spinner>
                  <span v-else>ثبت‌نام</span>
                </b-button>
              </div>
            </form>
            <div class="form-group form-button mt-3">
              <b-button variant="primary" @click="navigateBack">
                بازگشت
              </b-button>
            </div>
          </div>
          <div class="change-restaurant-info-image">
            <figure><img src="../../images/Restaurant-Register.png" alt="sign up image"></figure>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);
import { BVToastPlugin } from "bootstrap-vue";
Vue.use(BVToastPlugin);

export default {
  data() {
    return {
      restaurantName: '',
      postalCode: '',
      restaurantAddress: '',
      restaurantLat: '',
      restaurantLng: '',
      restaurantLicenceId: '',
      loading: false
    };
  },
  methods: {
    registerRestaurant() {
      this.loading = true;
      const api = "http://localhost:8000/api/v1/restaurants";
      const data = {
        name: this.restaurantName,
        postal_code: this.postalCode,
        address: this.restaurantAddress,
        lat: this.restaurantLat,
        lng: this.restaurantLng,
        licence_id: this.restaurantLicenceId,
      };

      Vue.axios.post(api, data)
        .then(response => {
          console.log(response);
          this.loading = false;
          this.$router.push({ name: 'SupplierMainPage' });
        }).catch((e) => {
          console.log(e);
          this.$bvToast.toast(e.response.data.message, {
            title: 'پیام خطا',
            autoHideDelay: 5000,
            appendToast: true
          });
          this.loading = false;
        });
    },
    navigateBack() {
      this.$router.push({ name: 'SupplierMainPage' });
    }
  }
}
</script>

<style scoped>
.change-restaurant-info-page {
  padding-top: 80px;
}

.change-restaurant-info-content {
  display: flex;
  display: -webkit-flex;
}

a:focus,
a:active,
a:hover {
  text-decoration: none;
  outline: none;
  transition: all 300ms ease 0s;
  -moz-transition: all 300ms ease 0s;
  -webkit-transition: all 300ms ease 0s;
  -o-transition: all 300ms ease 0s;
  -ms-transition: all 300ms ease 0s;
}

.input-group-text {
  border-top-left-radius: 0px !important;
  border-top-right-radius: 5px !important;
  border-bottom-right-radius: 5px !important;
  border-bottom-left-radius: 0px !important;
}

.form-control {
  border-top-left-radius: 5px !important;
  border-top-right-radius: 0px !important;
  border-bottom-right-radius: 0px !important;
  border-bottom-left-radius: 5px !important;
}

img {
  max-width: 100%;
  height: auto;
}

figure {
  margin: 0;
}

p {
  margin-bottom: 0px;
  font-size: 15px;
  color: #777;
}

h2 {
  line-height: 1.66;
  margin: 0;
  padding: 0;
  font-weight: bold;
  color: #222;
  font-family: Poppins;
  font-size: 36px;
}

body {
  font-size: 13px;
  line-height: 1.8;
  color: #222;
  background: #f8f8f8;
  font-weight: 400;
  font-family: Poppins;
}

.container {
  width: 900px;
  background: #fff;
  margin: 0 auto;
  box-shadow: 0px 15px 16.83px 0.17px rgba(0, 0, 0, 0.05);
  -moz-box-shadow: 0px 15px 16.83px 0.17px rgba(0, 0, 0, 0.05);
  -webkit-box-shadow: 0px 15px 16.83px 0.17px rgba(0, 0, 0, 0.05);
  -o-box-shadow: 0px 15px 16.83px 0.17px rgba(0, 0, 0, 0.05);
  -ms-box-shadow: 0px 15px 16.83px 0.17px rgba(0, 0, 0, 0.05);
  border-radius: 20px;
  -moz-border-radius: 20px;
  -webkit-border-radius: 20px;
  -o-border-radius: 20px;
  -ms-border-radius: 20px;
}

.change-restaurant-info {
  margin-bottom: 150px;
}

.change-restaurant-info-content {
  padding: 75px 0;
  display: flex;
  align-items: center;
}

.change-restaurant-info-image {
  width: 50%;
  text-align: center;
}

.change-restaurant-info-image img {
  max-width: 80%;
  height: auto;
}

.change-restaurant-info-form {
  width: 50%;
  padding-left: 34px;
}

.register-form {
  width: 100%;
}

.form-group {
  position: relative;
  margin-bottom: 25px;
  overflow: hidden;
}

.form-group:last-child {
  margin-bottom: 0px;
}
</style>
