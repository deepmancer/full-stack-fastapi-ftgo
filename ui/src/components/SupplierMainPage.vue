<template>
  <div class="restaurant-main-page" style="background-image: url('/images/background.jpg');">
    <b-container>
    <div class="user-id-box">
        <b-alert variant="info" show>
          <strong>your user_id is {{ userId }}</strong>
        </b-alert>
        <b-alert variant="info" show>
          <strong>your token is {{ token }}</strong>
        </b-alert>
      </div>
      <div v-if="restaurant">
        <div class="restaurant-header">
          <h1>{{ restaurant.name }}</h1>
        </div>
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
                @click="openFoodModal(food)"
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
                    <div>{{ food.name }}</div>
                    <div><strong>قیمت :</strong> {{ food.price }} تومان</div>
                  </div>
                  <b-icon icon="chevron-right"></b-icon>
                </div>
              </b-list-group-item>
            </b-list-group>
          </b-col>
        </b-row>
      </div>
      <div v-else class="no-restaurant">
        <p>هیچ رستورانی یافت نشد</p>
        <b-button variant="primary" @click="navigateToRegisterRestaurant">
          ثبت رستوران
        </b-button>
      </div>
    </b-container>

    <b-modal
      v-if="selectedFood"
      @hide="clearSelectedFood"
      id="food-modal"
      title="جزئیات غذا"
      size="lg"
      ok-title="ذخیره"
      ok-variant="success"
      cancel-title="لغو"
      cancel-variant="danger"
      @ok="updateFood"
    >
      <div class="d-block">
        <img :src="selectedFood.logo" alt="Logo" class="restaurant-logo mb-3" />
        <b-form @submit.prevent="updateFood">
          <b-form-group label="نام" label-for="food-name">
            <b-form-input id="food-name" v-model="selectedFood.name" required></b-form-input>
          </b-form-group>
          <b-form-group label="قیمت" label-for="food-price">
            <b-form-input id="food-price" v-model="selectedFood.price" required></b-form-input>
          </b-form-group>
          <b-form-group label="وضعیت" label-for="food-status">
            <b-form-select id="food-status" v-model="selectedFood.status" :options="statusOptions" required></b-form-select>
          </b-form-group>
        </b-form>
      </div>

      <template #modal-footer="{ ok, cancel }">
        <b-button variant="danger" @click="cancel">لغو</b-button>
        <b-button variant="success" @click="ok">ذخیره</b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      menu: [],
      selectedFood: null,
      statusOptions: [
        { value: 'موجود', text: 'موجود' },
        { value: 'ناموجود', text: 'ناموجود' }
      ]
    };
  },
  computed: {
    ...mapGetters(['getRestaurantInfo', 'getUserId', 'getToken']),
    restaurant() {
      return this.getRestaurantInfo;
    },
    userId() {
      return this.getUserId;
    },
    token() {
      return this.getToken;
    }
  },
  methods: {
    async fetchMenu() {
      if (this.restaurant) {
        const response = await this.$axios.get('/resturant/menu');
        this.menu = response.data;
      }
    },
    navigateToEditSupplierInfo() {
      this.$router.push({ name: 'ChangeRestaurantInfo' });
    },
    navigateToSupplierOrdersHistory() {
      this.$router.push({ name: 'SupplierOrdersHistory' });
    },
    navigateToSupplierActiveOrders() {
      this.$router.push({ name: 'SupplierActiveOrders' });
    },
    navigateToRegisterRestaurant() {
      this.$router.push({ name: 'RegisterRestaurantPage' });
    },
    openFoodModal(food) {
      this.selectedFood = { ...food };
      this.$bvModal.show('food-modal');
    },
    clearSelectedFood() {
      this.selectedFood = null;
    },
    async updateFood() {
      try {
        await this.$axios.put(`/resturant/menu/${this.selectedFood.id}`, this.selectedFood);
        this.$bvModal.hide('food-modal');
        this.fetchMenu(); // refresh menu list
      } catch (error) {
        console.error(error);
      }
    }
  },
  async created() {
    await this.fetchMenu();
  }
};
</script>

<style scoped>
.restaurant-main-page {
  height: 100vh;
  padding: 20px;
  background-size: cover;
  background-attachment: fixed;
}

.restaurant-header {
  text-align: center;
  margin-bottom: 20px;
}

.no-restaurant {
  text-align: center;
  margin-top: 50px;
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
