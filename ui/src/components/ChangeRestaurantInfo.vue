<template>
  <div dir="rtl" class="change-restaurant-info-page">
    <section class="change-restaurant-info">
      <div class="container">
        <div class="change-restaurant-info-content">
          <div class="change-restaurant-info-form">
            <h2 class="form-title">اطلاعات رستوران</h2>
            <form class="register-form" id="register-form" @submit.prevent="updateRestaurant">
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

    <!-- Delete Restaurant Modal -->
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

    <!-- Delete Account Modal -->
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
Vue.use(VueAxios, axios);
import { BVToastPlugin } from "bootstrap-vue";
Vue.use(BVToastPlugin);
import { mapGetters, mapActions } from 'vuex';

export default {
  data() {
    return {
      restaurantName: '',
      postalCode: '',
      restaurantAddress: '',
      restaurantLat: '',
      restaurantLng: '',
      loading: false
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
        this.$router.push({ name: '/' });
      } catch (error) {
        console.error('Error deleting account:', error);
        this.$bvToast.toast('Error deleting account. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      }
    },
    showDeleteRestaurantModal() {
      this.$bvModal.show('delete-restaurant-modal');
    },
    showDeleteAccountModal() {
      this.$bvModal.show('delete-account-modal');
    },
    navigateBack() {
      this.$router.push({ name: 'SupplierMainPage' });
    },
    initializeForm() {
      this.restaurantName = this.restaurant.name || '';
      this.postalCode = this.restaurant.postal_code || '';
      this.restaurantAddress = this.restaurant.address || '';
      this.restaurantLat = this.restaurant.address_lat || '';
      this.restaurantLng = this.restaurant.address_lng || '';
    }
  },
  created() {
    this.initializeForm();
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
