<template>
  <div class="driver-main-page"> 
    <b-container>
      <div v-if="vehicle">
        <!-- Driver Profile Section -->
        <div class="driver-profile">
          <b-button variant="primary" @click="navigateToEditDriverInfo">
            ویرایش اطلاعات
          </b-button>
          <div>
            <h3>شماره پلاک {{ vehicle.plate_number }}</h3>
          </div>
        </div>

        <!-- Map Section -->


        <!-- Active/Inactive Button -->
        <div class="driver-controls">
          <b-button
            :variant="isActive ? 'success' : 'secondary'"
            @click="toggleActive"
          >
            {{ isActive ? "فعال" : "غیرفعال" }}
          </b-button>
        </div>
      </div>
      <div v-else class="no-vehivle">
        <p>لطفا ابتدا اطلاعات ماشین خود را ثبت کنید.</p>
        <b-button variant="primary" @click="navigateToRegisterVehicle">
          ثبت اطلاعات ماشین
        </b-button>
      </div>
    </b-container>
  </div>
</template>


<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      isActive: false,
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
  methods: {
    navigateToRegisterVehicle() {
      this.$router.push({ name: 'RegisterVehiclePage' });
    },
    toggleActive() {
      this.isActive = !this.isActive;
    },
    navigateToEditDriverInfo() {
      this.$router.push({ name: "ChangeVehicleInfo" });
    },
    navigateToRestaurant(restaurantId) {
      this.$router.push({ name: "Restaurant", params: { id: restaurantId } });
    },
  },
};
</script>

<style scoped>
.driver-main-page {
  background-image: url('/images/background.jpg');
  height: 100vh;
  background-size: cover;
  color: #1c3a58;
  padding: 20px;
}

.driver-profile {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.profile-info {
  display: flex;
  align-items: center;
}

.driver-avatar {
  width: 60px;
  height: 60px;
  margin-right: 15px;
  object-fit: cover;
  border-radius: 50%;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.driver-profile .b-button {
  height: fit-content;
}

.driver-map {
  margin-top: 30px;
}

.restaurant-logo {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  object-fit: cover;
  border-radius: 50%;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.restaurant-popup {
  display: flex;
  align-items: center;
  flex-direction: column;
  text-align: center;
}

.restaurant-popup strong {
  display: block;
  margin-bottom: 5px;
}

.driver-controls {
  position: fixed;
  bottom: 20px;
  width: 10%;
  text-align: center;
  padding: 10px;
}

.driver-controls .b-button {
  font-size: 1.5rem;
  padding: 15px 30px;
}
</style>
