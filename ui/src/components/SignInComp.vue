<template>
    <div dir="rtl" class="signup-page">
        <section class="signup">
            <div class="container">
                <div class="signup-content">
                    <div class="signup-form">
                        <h2 class="form-title">ورود</h2>
                        <form class="register-form" id="register-form">
                            <b-input-group class="mt-3">
                                <template #prepend>
                                    <b-input-group-text>
                                        <font-awesome-icon icon="fa-solid fa-phone"/>
                                    </b-input-group-text>
                                </template>
                                <b-form-input placeholder="تلفن همراه" required v-model="phone"></b-form-input>
                            </b-input-group>
                            <b-input-group class="mt-3">
                                <template #prepend>
                                    <b-input-group-text>
                                        <font-awesome-icon icon="fa-solid fa-lock"/>
                                    </b-input-group-text>
                                </template>
                                <b-form-input type="password" placeholder="رمزعبور" required v-model="password"></b-form-input>
                            </b-input-group>
                            <b-input-group class="mt-3">
                                <b-form-select placeholder="نقش" v-model="userRole" :options="userRoles" class="w-100"></b-form-select>
                            </b-input-group>
                            <div class="form-group form-button mt-5">
                                <b-button variant="secondary" @click="signin">
                                    <b-spinner v-if="loading" label="Spinning"></b-spinner>
                                    <span v-else>
                                        ورود
                                    </span>
                                </b-button>
                            </div>
                        </form>
                    </div>
                    <div class="signup-image">
                        <figure><img src="../../images/signin-image.jpg" alt="sign up image"></figure>
                        <router-link class="signup-image-link" to="/SignUp">من که حساب کاربری ندارم :(</router-link>
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
import {BVToastPlugin} from "bootstrap-vue";
import {mapActions} from 'vuex';

Vue.use(VueAxios, axios);
Vue.use(BVToastPlugin);


export default {
  data() {
    return {
      phone: "",
      password: "",
      userRole: 'customer',
      userRoles: [
        {value: 'customer', text: 'مشتری'},
        {value: 'driver', text: 'پیک'},
        {value: 'restaurant_admin', text: 'رستوران'}
      ],
      loading: false,
      userId: null,
    }
  },
  methods: {
    ...mapActions(['updateUserId', 'updateToken', 'updateRestaurantInfo', 'updateVehicleInfo']),
    async signin() {
      this.loading = true;
      let api = "http://localhost:8000/api/v1/auth/login";
      const data = {
        role: this.userRole,
        phone_number: this.phone,
        password: this.password,
      };
      let response = null;
      try {
        response = await Vue.axios.post(api, data);
        localStorage.removeItem('token');
        localStorage.setItem('token', response.data.user_id);
        this.updateUserId(response.data.user_id);
        this.updateToken(response.data.token);
        this.phone = '';
        this.password = '';
        this.loading = false;

        if (this.userRole === 'restaurant_admin') {
          await this.fetchAndStoreRestaurantInfo(response.data.token);
        }

        if (this.userRole === 'driver') {
          await this.fetchAndStoreVehicleInfo(response.data.token);
        }

        switch (this.userRole) {
          case 'customer':
            this.$router.push('/CustomerMainPage');
            break;
          case 'driver':
            this.$router.push('/DeliveryMainPage');
            break;
          case 'restaurant_admin':
            this.$router.push('/SupplierMainPage');
            break;
          default:
            this.$router.push('/');
        }
      } catch (e) {
        if (e.response) {
          this.$bvToast.toast(e.response.data.detail.detail, {
            title: 'Error',
            variant: 'danger',
            solid: true,
            autoHideDelay: 5000,
          });

        } else {
          this.$bvToast.toast('مشکلی در ورود پیش آمد، لطفا مجددا تلاش کنید.', {
            title: 'Error',
            variant: 'danger',
            solid: true,
            autoHideDelay: 5000,
          });
        }
        this.phone = '';
        this.password = '';
        this.loading = false;
      }
    },
    async fetchAndStoreRestaurantInfo(token) {
      try {
        const response = await Vue.axios.get('http://localhost:8000/api/v1/restaurant/get_supplier_restaurant_info', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        if (response.data && response.data.id) {
          this.updateRestaurantInfo(response.data);
        } else {
          this.updateRestaurantInfo(null);
        }
      } catch (error) {
        this.updateRestaurantInfo(null);
        console.error('Failed to fetch restaurant info:', error);
      }
    },
    async fetchAndStoreVehicleInfo(token) {
      try {
        const response = await Vue.axios.get('http://localhost:8000/api/v1/vehicle/get_info', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        if (response.data && response.data.vehicle_id) {
          this.updateVehicleInfo(response.data);
        } else {
          this.updateVehicleInfo(null);
        }
      } catch (error) {
        this.updateVehicleInfo(null);
        console.error('Failed to fetch restaurant info:', error);
      }
    },
  }
}
</script>

<style scoped>
/* Your existing styles here */
</style>
