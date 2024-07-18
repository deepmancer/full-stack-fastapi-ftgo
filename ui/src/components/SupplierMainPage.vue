<template>
  <div class="restaurant-main-page" style="background-image: url('/images/background.jpg');">
    <b-container>
      <div class="restaurant-main-page">
        <b-container>
          <b-row>
            <b-col>
              <b-button variant="primary" @click="navigateToEditSupplierInfo">
                ویرایش اطلاعات
              </b-button>
            </b-col>
            <b-col>
              <b-button variant="primary" @click="navigateToSupplierActiveOrders">
                سفارشات درحال پردازش
              </b-button>
            </b-col>
            <b-col>
              <b-button variant="primary" @click="navigateToSupplierOrdersHistory">
                تاریخچه سفارشات
              </b-button>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <h2 class="mt-4">منو</h2>
              <b-list-group>
                <b-list-group-item
                  v-for="food in menu"
                  :key="food.id"
                  @click="navigateToFood(food.id)"
                  class="d-flex align-items-center restaurant-item"
                >
                  <div class="restaurant-info d-flex align-items-center justify-content-between w-100">
                    <div class="d-flex align-items-center">
                      <img :src="food.logo" alt="Logo" class="restaurant-logo" />
                      <div>
                        <div><strong>امتیاز:</strong> {{ food.score }}</div>
                        <div><strong>وضعیت:</strong> {{ food.status }}</div>
                      </div>
                    </div>
                    <div>
                      <div> {{ food.name }}</div>
                      <div><strong>قیمت :</strong> {{ food.price }} تومان</div>
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
export default {
  data() {
    return {
      menu: [
      {
          id: 1,
          logo: '/images/McDonalds.png',
          name: 'کباب',
          price: '200,000',
          score: 4.5,
          status: 'موجود'
        },
        {
          id: 2,
          logo: '/images/McDonalds.png',
          name: 'کباب',
          price: '200,000',
          score: 4.2,
          status: 'موجود'
        },
        {
          id: 3,
          logo: '/images/McDonalds.png',
          name: 'کباب',
          price: '200,000',
          score: 4.0,
          status: 'موجود'
        },
        {
          id: 4,
          logo: '/images/McDonalds.png',
          name: 'کباب',
          price: '200,000',
          score: 3.8,
          status: 'موجود'
        },
        {
          id: 5,
          logo: '/images/McDonalds.png',
          name: 'کباب',
          price: '200,000',
          score: 3.5,
          status: 'موجود'
        },
      ]
    };
  },
  methods: {
    async fetchMenu() {
      const response = await this.$axios.get('/resturant/menu');
      this.menu = response.data;
    },
    navigateToEditSupplierInfo() {
      this.$router.push({ name: 'EditSupplierInfo' });
    },
    navigateToSupplierOrdersHistory() {
      this.$router.push({ name: 'SupplierOrdersHistory' });
    },
    navigateToSupplierActiveOrders() {
      this.$router.push({ name: 'SupplierActiveOrders' });
    },
    navigateToFood(foodId) {
      this.$router.push({ name: 'FoodDetail', params: { id: foodId } });
    }
  }
};
</script>

<style scoped>
.restaurant-main-page {
  padding: 20px;
  background-size: cover;
  background-attachment: fixed;
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
</style>
