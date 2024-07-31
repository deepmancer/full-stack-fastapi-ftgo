<template>
  <div class="restaurant-main-page" style="background-image: url('/images/background.jpg');">
    <b-container>
      <div class="user-id-box">
        <b-alert variant="info" show>
          <strong>your user_id is {{ userId }}</strong>
        </b-alert>
        <b-alert variant="info" show>
          <strong>your restaurant is {{ restaurant.id }}</strong>
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
            <h2 class="mt-4">افزودن محصول جدید به منو</h2>
            <b-card>
              <b-form @submit.prevent="addFood">
                <b-form-group>
                  <b-form-input v-model="newItem.name" placeholder="نام محصول" class="rtl-text"></b-form-input>
                </b-form-group>
                <b-form-group>
                  <b-form-input v-model.number="newItem.price" placeholder="قیمت" class="rtl-text"></b-form-input>
                </b-form-group>
                <b-form-group>
                  <b-form-input v-model.number="newItem.count" placeholder="تعداد موجود" class="rtl-text"></b-form-input>
                </b-form-group>
                <b-form-group>
                  <b-form-input v-model="newItem.description" placeholder="توضیحات" class="rtl-text"></b-form-input>
                </b-form-group>
                <b-button type="submit">افزودن محصول</b-button>
              </b-form>
            </b-card>

            <h2 class="mt-4">منو</h2>
            <b-card>
            <b-list-group>
              <b-list-group-item v-for="item in menu" :key="item.item_id" class="rtl-text">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <div><strong>آیدی غذا:</strong> {{ item.item_id }}</div>
                    <div><strong>آیدی رستوران:</strong> {{ item.restaurant_id }}</div>
                    <div><strong>نام محصول:</strong> {{ item.name }}</div>
                    <div><strong>قیمت:</strong> {{ item.price }}</div>
                    <div><strong>موجودی:</strong> {{ item.count }}</div>
                    <div><strong>توضیحات:</strong> {{ item.description }}</div>
                  </div>
                  <div>
                    <b-button variant="danger" @click="confirmDeleteItem(item.item_id)">
                      حذف محصول
                    </b-button>
                  </div>
                </div>
              </b-list-group-item>
            </b-list-group>
          </b-card>

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
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      menu: [],
      selectedFood: null,
      isEditing: false,
      newItem: {
        restaurant_id: '',
        name: '',
        price: '',
        count: '',
        description: '',
      }
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
    async fetchMenu() {
      if (this.restaurant) {
        try {
          const response = await axios.post(
            'http://localhost:8000/api/v1/menu/get_all_menu_item',
            {restaurant_id: this.restaurant.id},
            {
              headers: { Authorization: `Bearer ${this.token}` },
            }
          );
          this.menu = response.data.menu;
        } catch (error) {
          console.error('Error fetching menu:', error);
        }
      }
    },
    async addFood() {
      try {
        this.newItem.restaurant_id = this.restaurant.id;

        await axios.post(
          'http://localhost:8000/api/v1/menu/add',
          this.newItem,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );

        this.newItem = {
          restaurant_id: this.restaurant.id,
          name: '',
          price: '',
          count: '',
          description: '',
        };

        await this.fetchMenu();
      } catch (error) {
        console.error('Error adding food:', error);
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

.restaurant-info {
  display: flex;
  align-items: center;
}
.rtl-text {
  direction: rtl;
}
</style>
