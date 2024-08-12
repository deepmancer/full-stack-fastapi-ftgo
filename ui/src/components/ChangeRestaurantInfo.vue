<template>
  <div dir="rtl" class="change-restaurant-info-page">
    <section class="change-restaurant-info">
      <div class="container">
        <div class="change-restaurant-info-content">
          <div class="change-restaurant-info-form">
            <h2 class="form-title">اطلاعات رستوران</h2>
            <form class="register-form" id="register-form" @submit.prevent="updateRestaurant">
              <b-input-group class="mt-3">
                <strong>نام رستوران:</strong>
                <b-form-input placeholder="نام رستوران" v-model="restaurantName" required></b-form-input>
              </b-input-group>
              <b-input-group class="mt-3">
                <strong>کد پستی رستوران:</strong>
                <b-form-input placeholder="کد پستی رستوران" v-model="postalCode" required></b-form-input>
              </b-input-group>
              <b-input-group class="mt-3">
                <strong>آدرس رستوران:</strong>
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
              <div class="form-group form-button mt-5">
                <b-button variant="secondary" type="submit" :disabled="loading">
                  <b-spinner v-if="loading" small></b-spinner>
                  <span v-else>به‌روزرسانی</span>
                </b-button>
              </div>
            </form>
            <div class="form-group form-button mt-3">
              <b-button variant="primary" @click="navigateBack">
                بازگشت
              </b-button>
            </div>
            <div class="form-group form-button mt-3">
              <b-button variant="danger" @click="showDeleteRestaurantModal">
                حذف رستوران
              </b-button>
            </div>
            <div class="form-group form-button mt-3">
              <b-button variant="danger" @click="showDeleteAccountModal">
                حذف حساب کاربری
              </b-button>
            </div>
          </div>
          <div class="change-restaurant-info-image">
            <figure><img src="../../images/Restaurant-Register.png" alt="sign up image"></figure>
          </div>
        </div>
      </div>
    </section>

    <b-modal
      id="delete-restaurant-modal"
      title="حذف رستوران"
      @ok="deleteRestaurant"
      ok-variant="danger"
      ok-title="حذف"
      cancel-title="لغو"
    >
      <p>آیا از حذف رستوران اطمینان دارید؟</p>
    </b-modal>

    <b-modal
      id="delete-account-modal"
      title="حذف حساب کاربری"
      @ok="deleteAccount"
      ok-variant="danger"
      ok-title="حذف"
      cancel-title="لغو"
    >
      <p>آیا از حذف حساب کاربری و رستوران خود، اطمینان دارید؟</p>
    </b-modal>
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
      restaurantLat: 35.6892, // default to Tehran
      restaurantLng: 51.3890, // default to Tehran
      loading: false,
      customIcon: null
    };
  },
  computed: {
    ...mapGetters(['getUserId', 'getToken', 'getRestaurantInfo']),
    userId() {
      return this.getUserId;
    },
    token() {
      return this.getToken;
    },
    restaurant() {
      return this.getRestaurantInfo;
    }
  },
  methods: {
    ...mapActions(['updateRestaurantInfo']),
    async updateRestaurant() {
      this.loading = true;
      try {
        const updateInfo = {
          restaurant_id: this.restaurant.id,
          name: this.restaurantName,
          postal_code: this.postalCode,
          address: this.restaurantAddress,
          address_lat: this.restaurantLat,
          address_lng: this.restaurantLng,
        };
        await axios.put(
          'http://localhost:8000/api/v1/restaurant/update',
          updateInfo,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.$bvToast.toast('اطلاعات رستوران با موفقیت به‌روزرسانی شد!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });

        await this.fetchAndStoreRestaurantInfo();
        this.$router.push({ name: 'SupplierMainPage' });
      } catch (error) {
        console.error('Error updating restaurant:', error);
        this.$bvToast.toast('Error updating restaurant. Please try again.', {
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
        const response = await Vue.axios.get('http://localhost:8000/api/v1/restaurant/get_supplier_restaurant_info', {
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
    async deleteRestaurant() {
      try {
        await axios.delete('http://localhost:8000/api/v1/restaurant/delete', {
          data: {restaurant_id: this.restaurant.id},
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.$bvToast.toast('رستوران با موفقیت حذف شد!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });
        await this.fetchAndStoreRestaurantInfo();
        this.$router.push({ name: 'SupplierMainPage' });
      } catch (error) {
        console.error('Error deleting restaurant:', error);
        this.$bvToast.toast('Error deleting restaurant. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      }
    },
    async deleteAccount() {
      try {
        await this.deleteRestaurant();
        await this.fetchAndStoreRestaurantInfo();
        await axios.delete('http://localhost:8000/api/v1/profile/delete', {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.$bvToast.toast('حساب کاربری با موفقیت حذف شد!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });
        this.$store.dispatch('logout');
        this.$router.push({ name: 'LandingPage' });
      } catch (error) {
        console.error('Error deleting account:', error);
        this.$bvToast.toast('Error deleting account. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      }
    },
    navigateBack() {
      this.$router.go(-1);
    },
    showDeleteRestaurantModal() {
      this.$bvModal.show('delete-restaurant-modal');
    },
    showDeleteAccountModal() {
      this.$bvModal.show('delete-account-modal');
    },
    updateLatLng({ lat, lng }) {
      this.restaurantLat = lat;
      this.restaurantLng = lng;
    }
  },
  async mounted() {
    await this.fetchAndStoreRestaurantInfo();
    if (this.restaurant) {
      this.restaurantName = this.restaurant.name;
      this.postalCode = this.restaurant.postal_code;
      this.restaurantAddress = this.restaurant.address;
      this.restaurantLat = this.restaurant.address_lat;
      this.restaurantLng = this.restaurant.address_lng;
    }

    // Create custom icon
    this.customIcon = L.icon({
      iconUrl: markerIcon,
      iconSize: [22, 32], // adjust size as needed
      iconAnchor: [32, 32], // point of the icon which will correspond to marker's location
      popupAnchor: [0, -32] // point from which the popup should open relative to the iconAnchor
    });
  }
};
</script>


<style scoped>
.change-restaurant-info-page {
  background: #f8f9fa;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.change-restaurant-info .container {
  max-width: 900px;
}
.change-restaurant-info-content {
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
  justify-content: space-between;
}
.change-restaurant-info-form {
  width: 50%;
}
.change-restaurant-info-image {
  width: 50%;
}
.change-restaurant-info-image figure {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
}
.change-restaurant-info-image img {
  max-width: 100%;
  height: auto;
}
.l-map {
  height: 400px;
}
</style>
