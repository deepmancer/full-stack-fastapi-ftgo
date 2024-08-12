<template>
  <div class="customer-main-page" style="background-image: url('/images/UserMainPage-image.jpg');">
    <b-container>
      <div class="customer-main-page-content">
        <b-container>
          <b-row>
            <b-col>
              <b-button variant="primary" @click="navigateToEditUserInfo">
                ویرایش اطلاعات کاربر
              </b-button>
            </b-col>
            <b-button @click="logout">
              خروج
            </b-button>
          </b-row>
          <b-row>
            <b-col>
              <h2 class="mt-4">رستوران‌ها</h2>
              <b-card>
                <b-list-group>
                  <b-list-group-item
                    v-for="restaurant in restaurants"
                    :key="restaurant.id"
                    class="rtl-text restaurant-item"
                    @click="selectRestaurant(restaurant)"
                    style="cursor: pointer;"
                  >
                    <div class="d-flex justify-content-between align-items-center">
                      <div><strong>آدرس:</strong> {{ restaurant.address }}</div>
                      <div><strong>نام رستوران:</strong> {{ restaurant.name }}</div>
                    </div>
                  </b-list-group-item>
                </b-list-group>
              </b-card>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </b-container>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';
import axios from 'axios';
import Vue from "vue";

export default {
  data() {
    return {
      restaurants: [],
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
    navigateToEditUserInfo() {
      this.$router.push({ name: 'CustomerChangeInfo' });
    },
    async logout() {
      try {
        await Vue.axios.post(
          'http://localhost:8000/api/v1/profile/logout',
          {},
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
      } catch (error) {
        console.error('Error logout :', error);
      }
      this.$router.push('/');
    },
    async selectRestaurant(restaurant) {
      await this.updateRestaurantInfo(restaurant);
      this.$router.push({ name: 'MenuPage' });
    },
    async fetchRestaurants() {
      try {
        const response = await axios.get(
          'http://localhost:8000/api/v1/restaurant/get_all_restaurant_info',
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );
        this.restaurants = response.data.restaurants;
      } catch (error) {
        console.error('Error fetching menu:', error);
      }
    },
  },
  async created() {
    await this.fetchRestaurants();
  }
};
</script>

<style scoped>
.customer-main-page {
  background-size: cover;
  background-attachment: fixed;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.customer-main-page-content {
  flex-grow: 1;
  padding: 20px;
}

.user-id-box {
  margin-top: 20px;
  text-align: center;
}

.restaurant-logo {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  object-fit: cover;
}

.restaurant-info {
  display: flex;
  align-items: center;
}

.restaurant-item {
  margin-top: 20px;
}
</style>
