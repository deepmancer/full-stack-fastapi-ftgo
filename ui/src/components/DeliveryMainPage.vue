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
            <h3>شماره پلاک: {{ vehicle.plate_number }}</h3>
          </div>
          <b-button @click="logout">
              خروج
            </b-button>
        </div>

        <!-- Map Section -->
        <div class="mt-3 l-map" v-if="isActive">
          <l-map
            :zoom="11"
            :center="[driverLocation.latitude, driverLocation.longitude]"
            @update:center="updateLatLng"
          >
            <l-tile-layer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <l-marker
              :lat-lng="[driverLocation.latitude, driverLocation.longitude]"
              :icon="customIcon"
              :draggable="false"
              @update:lat-lng="updateLatLng"
            />

            <l-marker
              :lat-lng="[35.7892, 51.4890]"
              :icon="restaurantIcon"
              :draggable="false"
            />

            <l-marker
              :lat-lng="[35.6492, 51.4590]"
              :icon="destinationtIcon"
              :draggable="false"
            />
          </l-map>
        </div>

        <!-- Active/Inactive Button -->
        <div class="driver-controls">
          <b-button
            :variant="isActive ? 'secondary' : 'success'"
            @click="toggleActive"
          >
            {{ isActive ? "غیرفعال" : "فعال" }}
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
import {LMap, LMarker, LTileLayer} from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon from "../assets/images/location-logo.png";
import destinationMarkerIcon from "../assets/images/destination-icon.png";
import restauranMarkertIcon from "../assets/images/restaurant-icon.png";
import {mapGetters} from 'vuex';
import Vue from "vue";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  data() {
    return {
      isActive: false,
      driverLocation: {
        latitude: 35.6892,
        longitude: 51.3890,
      },
      customIcon: null,
      restaurantIcon: null,
      destinationtIcon: null,
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
    },
    activeStatus() {
      return this.getActiveStatus;
    }
  },
  methods: {
    navigateToRegisterVehicle() {
      this.$router.push({ name: 'RegisterVehiclePage' });
    },
    async toggleActive() {
      this.isActive = !this.isActive;
      await this.setDriverOnlineStatus();
    },
    navigateToEditDriverInfo() {
      this.$router.push({ name: "ChangeVehicleInfo" });
    },
    navigateToRestaurant(restaurantId) {
      this.$router.push({ name: "Restaurant", params: { id: restaurantId } });
    },
    updateLatLng({ lat, lng }) {
      this.newAddress.latitude = lat;
      this.newAddress.longitude = lng;
    },
    async fetchDriverOnlineStatus() {
      try {
        const response = await Vue.axios.get('http://localhost:8000/api/v1/status/get', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        });
        if (response.data) {
            this.isActive = response.data.is_online;
        }
      } catch (error) {
        this.updateRestaurantInfo(null);
        console.error('Failed to get driver online status:', error);
      }
    },
    async setDriverOnlineStatus() {
      const url = this.isActive
        ? 'http://localhost:8000/api/v1/status/online'
        : 'http://localhost:8000/api/v1/status/offline';

      try {
        await Vue.axios.post(url, {}, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        });
        await this.fetchDriverOnlineStatus();
      } catch (error) {
        console.error(`Failed to set driver status to ${this.isActive ? 'Online' : 'Offline'}:`, error);
      }
    },
    async submitLocation() {
      this.driverLocation.latitude = this.driverLocation.latitude + 0.005;
      this.driverLocation.longitude = this.driverLocation.longitude + 0.005;
      const locationInfo = {
          locations: [
            {
              latitude: this.driverLocation.latitude,
              longitude: this.driverLocation.longitude,
              timestamp: 1,
              accuracy: 2,
              speed: 5,
              bearing: 188,
              altitude: 10
            }
          ]
        };
        await Vue.axios.post(
          'http://localhost:8000/api/v1/location/submit',
          locationInfo,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
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
    async refreshData() {
      await this.fetchDriverOnlineStatus();
      if (this.isActive) {
        await this.submitLocation();
      }

    },
    startRefresh() {
      setInterval(() => {
        this.refreshData();
      }, 5000);
    }
  },
  async mounted() {
    await this.fetchDriverOnlineStatus();

    this.customIcon = L.icon({
      iconUrl: markerIcon,
      iconSize: [22, 32],
      iconAnchor: [32, 32],
      popupAnchor: [0, -32]
    });

    this.restaurantIcon = L.icon({
      iconUrl: restauranMarkertIcon,
      iconSize: [32, 32],
      iconAnchor: [32, 32],
      popupAnchor: [0, -32]
    });

    this.destinationtIcon = L.icon({
      iconUrl: destinationMarkerIcon,
      iconSize: [32, 32],
      iconAnchor: [32, 32],
      popupAnchor: [0, -32]
    });

    this.startRefresh(); // Start the data refresh interval
  }
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

.l-map {
  height: 700px;
}
</style>
