<template>
  <div class="customer-main-page" style="background-image: url('/images/UserMainPage-image.jpg');">
    <b-container>
      <div class="user-id-box">
        <b-alert variant="info" show>
          <strong>your user_id is {{ userId }}</strong>
        </b-alert>
        <b-alert variant="info" show>
          <strong>your token is {{ token }}</strong>
        </b-alert>
      </div>
      <div class="customer-main-page">
        <b-container>
          <b-row>
            <b-col>
              <b-button variant="primary" @click="navigateToEditUserInfo">
                ویرایش اطلاعات کاربر
              </b-button>
            </b-col>
            <b-col>
              <b-button variant="primary" @click="navigateToShoppingCart">
                سبد خرید
              </b-button>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <h2 class="mt-4">رستوران‌ها</h2>
              <b-list-group>
                <b-list-group-item
                  v-for="restaurant in restaurants"
                  :key="restaurant.id"
                  @click="navigateToRestaurant(restaurant.id)"
                  class="d-flex align-items-center restaurant-item"
                >
                  <div class="restaurant-info d-flex align-items-center justify-content-between w-100">
                    <div class="d-flex align-items-center">
                      <img :src="restaurant.logo" alt="Logo" class="restaurant-logo" />
                      <div>
                        <div><strong>امتیاز:</strong> {{ restaurant.score }}</div>
                        <div><strong>وضعیت:</strong> {{ restaurant.status }}</div>
                      </div>
                    </div>
                    <div>
                      <div><strong>نام:</strong> {{ restaurant.name }}</div>
                      <div><strong>آدرس:</strong> {{ restaurant.address }}</div>
                    </div>
                    <b-icon icon="chevron-right"></b-icon>
                  </div>
                </b-list-group-item>
              </b-list-group>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </b-container>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      restaurants: [
        { id: 1, logo: '/images/McDonalds.png', name: 'مک دونالد 1', address: 'تهران، شریعتی، بالاتر از سه راه قلهک', score: 4.5, status: 'باز' },
        { id: 2, logo: '/images/McDonalds.png', name: 'مک دونالد 2', address: 'تهران، شریعتی، بالاتر از سه راه قلهک', score: 4.2, status: 'باز' },
        { id: 3, logo: '/images/McDonalds.png', name: 'مک دونالد 3', address: 'تهران، شریعتی، بالاتر از سه راه قلهک', score: 3.5, status: 'بسته' },
        { id: 4, logo: '/images/McDonalds.png', name: 'مک دونالد 4', address: 'تهران، شریعتی، بالاتر از سه راه قلهک', score: 2.5, status: 'باز' },
        { id: 5, logo: '/images/McDonalds.png', name: 'مک دونالد 5', address: 'تهران، شریعتی، بالاتر از سه راه قلهک', score: 1.5, status: 'باز' },
        { id: 6, logo: '/images/McDonalds.png', name: 'مک دونالد 6', address: 'تهران، شریعتی، بالاتر از سه راه قلهک', score: 1.5, status: 'باز' },
        { id: 7, logo: '/images/McDonalds.png', name: 'مک دونالد 7', address: 'تهران، شریعتی، بالاتر از سه راه قلهک', score: 3.9, status: 'بسته' },
      ]
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
    navigateToEditUserInfo() {
      this.$router.push({ name: 'CustomerChangeInfo' });
    },
    navigateToShoppingCart() {
      this.$router.push({ name: 'ShoppingCart' });
    },
    navigateToRestaurant(restaurantId) {
      this.$router.push({ name: 'Restaurant', params: { id: restaurantId } });
    }
  }
};
</script>

<style scoped>
.customer-main-page {
  padding: 20px;
  background-size: cover;
  background-attachment: fixed;
}

.user-id-box {
  margin-top: 20px;
  text-align: center;
}

.restaurant-logo {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  object-fit: cover; /* Ensures the image covers the container without distortion */
}

.restaurant-info {
  display: flex;
  align-items: center;
}
</style>
