<template>
  <div class="driver-main-page"> 
    <b-container>
      <!-- Driver Profile Section -->
      <div class="driver-profile">
        <b-button variant="primary" @click="navigateToEditDriverInfo">
          ویرایش اطلاعات
        </b-button>
        <b-button variant="primary" @click="navigateToDeliveryActiveOrder">
          مشاهده سفارش فعال
        </b-button>
        <div class="profile-info">
          <img
            src="/images/default-avatar.png"
            alt="Driver Avatar"
            class="driver-avatar"
          />
          <div>
            <h3>نام: {{ driver.name }}</h3>
            <p>شماره تماس: {{ driver.phone }}</p>
          </div>
        </div>
      </div>

      <!-- Map Section -->
      <div v-if="isActive" class="driver-map">
        <h2 class="mt-4 text-center">نقشه رستوران‌ها</h2>
        <!-- Leaflet Map -->
        <l-map
          style="height: 400px; width: 100%"
          :zoom="12"
          :center="[35.6892, 51.389]"
        >
          <l-tile-layer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
          ></l-tile-layer>

          <l-marker
            v-for="restaurant in restaurants"
            :key="restaurant.id"
            :lat-lng="[restaurant.lat, restaurant.lng]"
            @click="navigateToRestaurant(restaurant.id)"
          >
            <l-popup>
              <div class="restaurant-popup">
                <img
                  :src="restaurant.logo"
                  alt="Logo"
                  class="restaurant-logo"
                />
                <div><strong>نام:</strong> {{ restaurant.name }}</div>
                <div><strong>آدرس:</strong> {{ restaurant.address }}</div>
              </div>
            </l-popup>
          </l-marker>
        </l-map>
      </div>

      <!-- Active/Inactive Button -->
      <div class="driver-controls">
        <b-button
          :variant="isActive ? 'success' : 'secondary'"
          @click="toggleActive"
        >
          {{ isActive ? "فعال" : "غیرفعال" }}
        </b-button>
      </div>
    </b-container>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  data() {
    return {
      isActive: false,
      driver: {
        name: "علی احمدی",
        phone: "09123456789",
        avatar: "/images/default-avatar.png",
      },
      restaurants: [
        {
          id: 1,
          logo: "/images/McDonalds.png",
          name: "مک دونالد 1",
          address: "تهران، شریعتی، بالاتر از سه راه قلهک",
          lat: 35.7615,
          lng: 51.409,
          status: "نیازمند پیک",
        },
        {
          id: 2,
          logo: "/images/McDonalds.png",
          name: "مک دونالد 2",
          address: "تهران، شریعتی، بالاتر از سه راه قلهک",
          lat: 35.7128,
          lng: 51.388,
          status: "نیازمند پیک",
        },
        {
          id: 3,
          logo: "/images/McDonalds.png",
          name: "مک دونالد 3",
          address: "تهران، شریعتی، بالاتر از سه راه قلهک",
          lat: 35.6892,
          lng: 51.389,
          status: "نیازمند پیک",
        },
      ],
    };
  },
  methods: {
    toggleActive() {
      this.isActive = !this.isActive;
    },
    navigateToDeliveryActiveOrder() {
      this.$router.push({ name: "DeliveryActiveOrder" });
    },
    navigateToEditDriverInfo() {
      this.$router.push({ name: "DriverChangeInfo" });
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
