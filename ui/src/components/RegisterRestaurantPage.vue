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
              <div class="mt-3 l-map">
                <l-map
                  :zoom="13"
                  :center="[restaurantLat, restaurantLng]"
                  @update:center="updateLatLng"
                >
                  <l-tile-layer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  />
                  <l-marker
                    :lat-lng="[restaurantLat, restaurantLng]"
                    :icon="customIcon"
                    :draggable="true"
                    @update:lat-lng="updateLatLng"
                  />
                </l-map>
              </div>
              <b-input-group class="mt-3">
                <template #prepend>
                  <b-input-group-text>
                    <font-awesome-icon icon="fa-solid fa-id-card" />
                  </b-input-group-text>
                </template>
                <b-form-input placeholder="شناسه مجوز رستوران" v-model="restaurantLicenceId" required></b-form-input>
              </b-input-group>

              <div class="form-group form-button mt-5">
                <b-button variant="secondary" type="submit" :disabled="loading">
                  <b-spinner v-if="loading" small></b-spinner>
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
import {BVToastPlugin} from "bootstrap-vue";
import {mapActions, mapGetters} from 'vuex';
import {LMap, LMarker, LTileLayer} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon from "../assets/images/location-logo.png";

Vue.use(VueAxios, axios);
Vue.use(BVToastPlugin);

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  data() {
    return {
      restaurantName: '',
      postalCode: '',
      restaurantAddress: '',
      restaurantLat: '',
      restaurantLng: '',
      restaurantLicenceId: '',
      loading: false,
      customIcon: null,
    };
  },
  computed: {
    ...mapGetters(['getUserId', 'getToken']),
    userId() {
      return this.getUserId;
    },
    token() {
      return this.getToken;
    }
  },
  methods: {
    ...mapActions(['updateRestaurantInfo']),
    async registerRestaurant() {
      this.loading = true;
      try {
        const registerInfo = {
          name: this.restaurantName,
          postal_code: this.postalCode,
          address: this.restaurantAddress,
          address_lat: this.restaurantLat,
          address_lng: this.restaurantLng,
          restaurant_licence_id: this.restaurantLicenceId
        };
        await axios.post(
          'http://localhost:8000/api/v1/restaurant/register',
          registerInfo,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.$bvToast.toast('Restaurant registered successfully!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });

        // Fetch and store restaurant info
        await this.fetchAndStoreRestaurantInfo();

        this.$router.push({ name: 'SupplierMainPage' });
      } catch (error) {
        console.error('Error registering restaurant:', error);
        this.$bvToast.toast('Error registering restaurant. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      } finally {
        this.loading = false;
      }
    },
    async fetchAndStoreRestaurantInfo() {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/restaurant/get_supplier_restaurant_info', {
          headers: {
            Authorization: `Bearer ${this.token}`
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
    navigateBack() {
      this.$router.push({ name: 'SupplierMainPage' });
    },
    updateLatLng({ lat, lng }) {
      this.restaurantLat = lat;
      this.restaurantLng = lng;
    }
  },
  async mounted() {

    this.restaurantLat = 35.6892;
    this.restaurantLng = 51.3890;

    this.customIcon = L.icon({
      iconUrl: markerIcon,
      iconSize: [22, 32], // adjust size as needed
      iconAnchor: [32, 32], // point of the icon which will correspond to marker's location
      popupAnchor: [0, -32] // point from which the popup should open relative to the iconAnchor
    });
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

.l-map {
  height: 400px;
}
</style>