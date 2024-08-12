<template>
  <div dir="rtl" class="change-restaurant-info-page">
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
          <b-list-group-item class="rtl-text">
            <strong>شماره پلاک:</strong> {{ plateNumber }}
          </b-list-group-item>
          <b-list-group-item class="rtl-text">
            <strong>شماره گواهینامه:</strong> {{ licenceNumber }}
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

        <div class="text-center mt-3">
          <b-button variant="danger" @click="confirmDeleteAccount">حذف حساب کاربری من</b-button>
        </div>
        <div class="text-center mt-3">
          <b-button variant="danger" @click="confirmDeleteVehicle">حذف وسیله نقلیه‌ی من</b-button>
        </div>
        <div class="text-center mt-3">
          <b-button @click="navigateBack">برگشت</b-button>
        </div>
      </b-card>

    </b-container>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import {BVToastPlugin} from "bootstrap-vue";
import {mapActions, mapGetters} from 'vuex';

Vue.use(VueAxios, axios);
Vue.use(BVToastPlugin);

export default {
  data() {
    return {
      userInfo: {},
      plateNumber: '',
      licenceNumber: '',
      loading: false,
    };
  },
  computed: {
    ...mapGetters(['getVehicleInfo', 'getUserId', 'getToken']),
    vehicle() {
      return this.getVehicleInfo;
    },
    userId() {
      return this.getUserId;
    },
    token() {
      return this.getToken;
    }
  },
  created() {
    this.fetchUserInfo();
  },
  methods: {
    ...mapActions(['updateVehicleInfo']),
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
        this.$router.push({ name: 'DeliveryMainPage' });
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
    async registerVehicle() {
      this.loading = true;
      try {
        const registerInfo = {
          plate_number: this.plateNumber,
          license_number: this.licenceNumber,
        };
        await axios.post(
          'http://localhost:8000/api/v1/vehicle/register',
          registerInfo,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.$bvToast.toast('Vehicle registered successfully!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });

        await this.fetchAndStoreVehicleInfo();

        this.$router.push({ name: 'DeliveryMainPage' });
      } catch (error) {
        console.error('Error registering vehicle:', error);
        this.$bvToast.toast('Error registering vehicle. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      } finally {
        this.loading = false;
      }
    },
    async fetchAndStoreVehicleInfo() {
        try {
            const response = await Vue.axios.get('http://localhost:8000/api/v1/vehicle/get_info', {
                headers: {
                    Authorization: `Bearer ${this.token}`
                }
            });
            if (response.data && response.data.vehicle_id) {
                this.updateVehicleInfo(response.data);
            } else {
                this.updateVehicleInfo(null);
            }
        } catch (error) {
            this.updateVehicleInfo(null);
            console.error('Failed to fetch vehicle info:', error);
        }
    },
    async confirmDeleteVehicle() {
      if (confirm('آیا از حذف وسیله نقلیه خود اطمینان دارید؟')) {
        this.deleteVehicle();
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
    async deleteVehicle() {
      try {
        await axios.delete('http://localhost:8000/api/v1/vehicle/delete', {
          data: {vehicle_id: this.vehicle.vehicle_id},
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.$bvToast.toast('وسیله نقلیه با موفقیت حذف شد!', {
          title: 'Success',
          variant: 'success',
          solid: true
        });
        await this.fetchAndStoreVehicleInfo();
        this.$router.push({ name: 'DeliveryMainPage' });
      } catch (error) {
        console.error('Error deleting vehicle:', error);
        this.$bvToast.toast('Error deleting vehicle. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true
        });
      }
    },
    navigateBack() {
      this.$router.push({ name: 'DeliveryMainPage' });
    },
  },
  async mounted() {
    await this.fetchAndStoreVehicleInfo();
    if (this.vehicle) {
      this.plateNumber = this.vehicle.plate_number;
      this.licenceNumber = this.vehicle.license_number;
    }
  },

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

.l-map {
  height: 400px;
}
</style>