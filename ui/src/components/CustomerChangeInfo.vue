<template>
  <div class="customer-change-info">
    <b-container>
      <h2>اطلاعات کاربری</h2>
      <b-card>

        <b-list-group flush>
          <b-list-group-item class="rtl-text">
            <strong>کدملی:</strong> {{ userInfo.national_id }}
          </b-list-group-item>
          <b-list-group-item class="rtl-text">
            <strong>تلفن:</strong> {{ userInfo.phone_number }}
          </b-list-group-item>
        </b-list-group>

        <form class="register-form" id="register-form" @submit.prevent="updateUser">
          <b-input-group class="mt-3 rtl-text">
            <strong>نام:</strong>
            <b-form-input class="rtl-text" placeholder="نام" v-model="userInfo.first_name" required></b-form-input>
          </b-input-group>
          <b-input-group class="mt-3 rtl-text">
            <strong>نام خانوادگی:</strong>
            <b-form-input class="rtl-text" placeholder="نام خانوادگی" v-model="userInfo.last_name" required></b-form-input>
          </b-input-group>
          <div class="form-group form-button mt-5">
            <b-button variant="secondary" type="submit" :disabled="loading">
              <b-spinner v-if="loading" small></b-spinner>
              <span v-else>به‌روزرسانی</span>
            </b-button>
          </div>
        </form>

        <div class="text-right mt-3">
          <b-button variant="danger" @click="confirmDeleteAccount">حذف حساب کاربری من</b-button>
        </div>
        <div class="text-right mt-3">
          <b-button @click="backToUserPage">برگشت</b-button>
        </div>
      </b-card>

      <h2 class="mt-4">آدرس‌ها</h2>
      <b-card>
        <b-list-group>
          <b-list-group-item v-for="address in addresses" :key="address.address_id" class="rtl-text">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div><strong>آدرس 1:</strong> {{ address.address_line_1 }}</div>
                <div><strong>آدرس 2:</strong> {{ address.address_line_2 }}</div>
                <div><strong>شهر:</strong> {{ address.city }}</div>
                <div><strong>کد پستی:</strong> {{ address.postal_code }}</div>
                <div><strong>کشور:</strong> {{ address.country }}</div>
                <div><strong>پیش‌فرض:</strong> {{ address.is_default ? "بله" : "خیر" }}</div>
              </div>
              <div>
                <b-button variant="secondary" @click="setPreferredAddress(address.address_id)">
                  تنظیم به عنوان آدرس پیش‌فرض
                </b-button>
                <b-button variant="danger" @click="confirmDeleteAddress(address.address_id)">
                  حذف آدرس
                </b-button>
              </div>
            </div>
          </b-list-group-item>
        </b-list-group>
      </b-card>

      <h2 class="mt-4">افزودن آدرس جدید</h2>
      <b-card>
        <b-form @submit.prevent="addAddress">
          <b-form-group>
            <b-form-input v-model="newAddress.address_line_1" placeholder="آدرس خط 1" class="rtl-text"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.address_line_2" placeholder="آدرس خط 2" class="rtl-text"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.city" placeholder="شهر" class="rtl-text"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.postal_code" placeholder="کد پستی" class="rtl-text"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.country" placeholder="کشور" class="rtl-text"></b-form-input>
          </b-form-group>
          <div class="mt-3 l-map">
              <l-map
                :zoom="13"
                :center="[newAddress.latitude, newAddress.longitude]"
                @update:center="updateLatLng"
              >
                <l-tile-layer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <l-marker
                  :lat-lng="[newAddress.latitude, newAddress.longitude]"
                  :icon="customIcon"
                  :draggable="true"
                  @update:lat-lng="updateLatLng"
                />
              </l-map>
            </div>
          <b-button type="submit">افزودن آدرس</b-button>
        </b-form>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';
import {mapGetters} from 'vuex';

import {LMap, LMarker, LTileLayer} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon from "../assets/images/location-logo.png";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  name: 'CustomerChangeInfoComp',
  data() {
    return {
      userInfo: {},
      addresses: [],
      newAddress: {
        latitude: 0,
        longitude: 0,
        address_line_1: '',
        address_line_2: '',
        city: '',
        postal_code: '',
        country: ''
      },
      loading: false,
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
  created() {
    this.fetchUserInfo();
    this.fetchAddresses();
  },
  methods: {
    async updateUser() {
      this.loading = true;
      try {
        await axios.put(
          'http://localhost:8000/api/v1/profile/update',
          { first_name: this.userInfo.first_name, last_name: this.userInfo.last_name },
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.$bvToast.toast('اطلاعات کاربر با موفقیت به‌روزرسانی شد!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });

        await this.fetchUserInfo();
        this.$router.push({ name: 'CustomerMainPage' });
      } catch (error) {
        console.error('Error updating restaurant:', error);
        this.$bvToast.toast('Error updating user. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      } finally {
        this.loading = false;
      }
    },
    async fetchUserInfo() {
      try {
        const response = await axios.get(
          'http://localhost:8000/api/v1/profile/user_info',
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.userInfo = response.data;
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    },
    async fetchAddresses() {
      try {
        const response = await axios.get(
          'http://localhost:8000/api/v1/address/get_all_info',
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.addresses = response.data.addresses;
      } catch (error) {
        console.error('Error fetching addresses:', error);
      }
    },
    async addAddress() {
      try {
        await axios.post(
          'http://localhost:8000/api/v1/address/add',
          this.newAddress,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.newAddress = {
          latitude: 35.6892,
          longitude: 51.3890,
          address_line_1: '',
          address_line_2: '',
          city: '',
          postal_code: '',
          country: ''
        };
        this.fetchAddresses();
      } catch (error) {
        console.error('Error adding address:', error);
      }
    },
    async deleteAddress(addressId) {
      try {
        await axios.delete('http://localhost:8000/api/v1/address/delete', {
          data: {address_id: addressId },
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.fetchAddresses();
      } catch (error) {
        console.error('Error deleting address:', error);
      }
    },
    async setPreferredAddress(addressId) {
      try {
        await axios.post('http://localhost:8000/api/v1/address/set-preferred', {
          address_id: addressId
        }, {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.fetchAddresses();
      } catch (error) {
        console.error('Error setting preferred address:', error);
      }
    },
    async confirmDeleteAddress(addressId) {
      if (confirm('آیا از حذف این آدرس اطمینان دارید؟')) {
        this.deleteAddress(addressId);
      }
    },
    async confirmDeleteAccount() {
      if (confirm('آیا از حذف حساب کاربری خود اطمینان دارید؟')) {
        this.deleteAccount();
        this.$router.push('/');
      }
    },
    async deleteAccount() {
      try {
        await axios.delete('http://localhost:8000/api/v1/profile/delete', {
          data: { user_id: this.userId },
          headers: { Authorization: `Bearer ${this.token}` }
        });
      } catch (error) {
        console.error('Error deleting user account:', error);
      }
    },
    backToUserPage() {
      this.$router.push('/CustomerMainPage');
    },
    updateLatLng({ lat, lng }) {
      this.newAddress.latitude = lat;
      this.newAddress.longitude = lng;
    }
  },
  async mounted() {

    this.newAddress.latitude = 35.6892;
    this.newAddress.longitude = 51.3890;

    this.customIcon = L.icon({
      iconUrl: markerIcon,
      iconSize: [22, 32],
      iconAnchor: [32, 32],
      popupAnchor: [0, -32]
    });
  }
};
</script>

<style scoped>
.customer-change-info {
  padding: 20px;
}
.user-id-box {
  margin-top: 20px;
  text-align: center;
}
.rtl-text {
  direction: rtl;
}
.l-map {
  height: 400px;
}
</style>
