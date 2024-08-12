<template>
  <div class="menu-page" style="background-image: url('/images/background.jpg');">
    <b-container>
      <b-row>
        <b-col>
          <div class="text-right mt-3">
            <b-button @click="backToUserPage">برگشت</b-button>
          </div>
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
                  <div class="item-controls">
                    <b-button @click="decreaseItemCart(item.item_id)" :disabled="!cart.items[item.item_id]">
                      <font-awesome-icon icon="fa-minus" />
                    </b-button>
                    <span class="item-count">{{ cart.items[item.item_id] || 0 }}</span>
                    <b-button @click="increaseItemCart(item.item_id, item.count)">
                      <font-awesome-icon icon="fa-plus" />
                    </b-button>
                  </div>
                </div>
              </b-list-group-item>
            </b-list-group>
          </b-card>
        </b-col>
      </b-row>
      <b-row class="mt-4">
        <b-col>
          <div class="order-summary">
            <h4>خلاصه سفارش</h4>
            <div>قیمت کل: {{ totalPrice }} تومان</div>
            <b-button v-if="totalPrice > 0" variant="success" @click="submitOrder">
              ثبت سفارش
            </b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';
import axios from 'axios';
import {library} from '@fortawesome/fontawesome-svg-core';
import {faMinus, faPlus} from '@fortawesome/free-solid-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

library.add(faPlus, faMinus);

export default {
  components: {
    FontAwesomeIcon
  },
  data() {
    return {
      menu: [],
      cart: {
        restaurant_id: '',
        items: {}
      },
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
    },
    totalPrice() {
      return Object.entries(this.cart.items).reduce((total, [itemId, count]) => {
        const item = this.menu.find(item => item.item_id === itemId);
        return total + (item ? item.price * count : 0);
      }, 0);
    }
  },
  methods: {
    ...mapActions(['updateRestaurantInfo']),
    backToUserPage() {
      this.updateRestaurantInfo(null);
      this.$router.push('/CustomerMainPage');
    },
    async fetchMenu() {
      if (this.restaurant) {
        try {
          const response = await axios.post(
            'http://localhost:8000/api/v1/menu/get_all_menu_item',
            { restaurant_id: this.restaurant.id },
            {
              headers: { Authorization: `Bearer ${this.token}` },
            }
          );
          this.menu = response.data.menu;
          this.cart.restaurant_id = this.restaurant.id;
        } catch (error) {
          console.error('Error fetching menu:', error);
        }
      }
    },
    increaseItemCart(itemId, maxCount) {
      if (!this.cart.items[itemId]) {
        this.$set(this.cart.items, itemId, 0);
      }
      if (this.cart.items[itemId] < maxCount) {
        this.cart.items[itemId]++;
      }
    },
    decreaseItemCart(itemId) {
      if (this.cart.items[itemId] > 0) {
        this.cart.items[itemId]--;
      }
    },
    async submitOrder() {
      try {
        const orderData = {
          restaurant_id: this.cart.restaurant_id,
          items: this.cart.items
        };
        await axios.post(
          'http://localhost:8000/api/v1/order/create',
          orderData,
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );
        this.$bvToast.toast('سفارش شما با موفقیت ثبت شد!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });
      } catch (error) {
        console.error('Error submitting order:', error);
        this.$bvToast.toast('خطا در ثبت سفارش. لطفاً دوباره امتحان کنید.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      }
    },
  },
  async created() {
    await this.fetchMenu();
  }
};
</script>

<style scoped>
.menu-page {
  height: 100vh;
  padding: 20px;
  background-size: cover;
  background-attachment: fixed;
}

.text-right {
  text-align: right;
}

.item-controls {
  display: flex;
  align-items: center;
}

.item-count {
  margin: 0 10px;
}

.order-summary {
  text-align: right;
}

.rtl-text {
  direction: rtl;
}
</style>
