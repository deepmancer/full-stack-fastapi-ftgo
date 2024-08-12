<template>
  <div class="restaurant-main-page" style="background-image: url('/images/background.jpg');">
    <b-container>
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
            <b-button @click="logout">
              خروج
            </b-button>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <h2 class="mt-4">{{ editMode ? 'به‌روزرسانی محصول' : 'افزودن محصول جدید به منو' }}</h2>
            <b-card>
              <b-form @submit.prevent="editMode ? updateFood() : addFood()">
                <b-form-group>
                  <b-form-input v-model="newItem.name" placeholder="نام محصول" class="rtl-text" required></b-form-input>
                </b-form-group>
                <b-form-group>
                  <b-form-input v-model.number="newItem.price" placeholder="قیمت" class="rtl-text" required></b-form-input>
                </b-form-group>
                <b-form-group>
                  <b-form-input v-model.number="newItem.count" placeholder="تعداد موجود" class="rtl-text" required></b-form-input>
                </b-form-group>
                <b-form-group>
                  <b-form-input v-model="newItem.description" placeholder="توضیحات" class="rtl-text" required></b-form-input>
                </b-form-group>
                <b-button type="submit">{{ editMode ? 'به‌روزرسانی محصول' : 'افزودن محصول' }}</b-button>
                <b-button v-if="editMode" @click="cancelEdit" variant="secondary">لغو</b-button>
              </b-form>
            </b-card>

            <h2 class="mt-4">منو</h2>
            <b-card>
              <b-list-group>
                <b-list-group-item v-for="item in menu" :key="item.item_id" class="rtl-text">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <div><strong>نام محصول:</strong> {{ item.name }}</div>
                      <div><strong>قیمت:</strong> {{ item.price }}</div>
                      <div><strong>موجودی:</strong> {{ item.count }}</div>
                      <div><strong>توضیحات:</strong> {{ item.description }}</div>
                    </div>
                    <div v-if="!editMode">
                      <b-button variant="danger" @click="confirmDeleteItem(item.item_id)">
                        حذف محصول
                      </b-button>
                      <b-button variant="warning" @click="editItem(item)">
                        ویرایش محصول
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
import {mapGetters} from 'vuex';
import axios from 'axios';
import Vue from "vue";

export default {
  data() {
    return {
      menu: [],
      newItem: {
        restaurant_id: '',
        name: '',
        price: '',
        count: '',
        description: '',
      },
      editMode: false,
      currentItem: null,
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

        this.resetNewItem();

        await this.fetchMenu();
      } catch (error) {
        console.error('Error adding food:', error);
      }
    },
    async updateFood() {
      try {
        await axios.put(
          'http://localhost:8000/api/v1/menu/update',
          this.newItem,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );

        this.resetNewItem();
        this.editMode = false;
        this.currentItem = null;

        await this.fetchMenu();
      } catch (error) {
        console.error('Error updating food:', error);
      }
    },
    resetNewItem() {
      this.newItem = {
        restaurant_id: this.restaurant.id,
        name: '',
        price: '',
        count: '',
        description: '',
      };
    },
    async deleteItem(itemId) {
      try {
        await axios.delete('http://localhost:8000/api/v1/menu/delete', {
          data: {item_id: itemId },
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.fetchMenu();
      } catch (error) {
        console.error('Error deleting item:', error);
      }
    },
    async confirmDeleteItem(itemId) {
      if (confirm('آیا از حذف این محصول اطمینان دارید؟')) {
        this.deleteItem(itemId);
      }
    },
    editItem(item) {
      this.editMode = true;
      this.currentItem = item;
      this.newItem = { ...item };
    },
    cancelEdit() {
      this.editMode = false;
      this.currentItem = null;
      this.resetNewItem();
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
