<template>
  <div class="change-user-info">
    <b-container>
      <h2>اطلاعات کاربری</h2>
      <b-card>
        <b-list-group flush>
          <b-list-group-item>
            <strong>نام کاربری:</strong> {{ userInfo.username }}
          </b-list-group-item>
          <b-list-group-item>
            <strong>نام:</strong> {{ userInfo.firstName }}
          </b-list-group-item>
          <b-list-group-item>
            <strong>نام خانوادگی:</strong> {{ userInfo.lastName }}
          </b-list-group-item>
          <b-list-group-item>
            <strong>ایمیل:</strong> {{ userInfo.email }}
          </b-list-group-item>
        </b-list-group>
        <div class="text-right mt-3">
          <b-button variant="danger" @click="deleteAccount">حذف حساب کاربری من</b-button>
        </div>
      </b-card>

      <h2 class="mt-4">آدرس‌ها</h2>
      <b-card>
        <b-list-group>
          <b-list-group-item v-for="address in addresses" :key="address.addressId">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div><strong>آدرس 1:</strong> {{ address.addressLine1 }}</div>
                <div><strong>آدرس 2:</strong> {{ address.addressLine2 }}</div>
                <div><strong>شهر:</strong> {{ address.city }}</div>
                <div><strong>کد پستی:</strong> {{ address.postalCode }}</div>
                <div><strong>کشور:</strong> {{ address.country }}</div>
              </div>
              <div>
                <b-button variant="secondary" @click="setPreferredAddress(address.addressId)">
                  تنظیم به عنوان آدرس پیش‌فرض
                </b-button>
                <b-button variant="danger" @click="deleteAddress(address.addressId)">
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
            <b-form-input v-model="newAddress.addressLine1" placeholder="آدرس 1"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.addressLine2" placeholder="آدرس 2"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.city" placeholder="شهر"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.postalCode" placeholder="کد پستی"></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-input v-model="newAddress.country" placeholder="کشور"></b-form-input>
          </b-form-group>
          <b-button type="submit">افزودن آدرس</b-button>
        </b-form>
      </b-card>
    </b-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInfo: {
        username: '',
        firstName: '',
        lastName: '',
        email: ''
      },
      addresses: [],
      newAddress: {
        addressLine1: '',
        addressLine2: '',
        city: '',
        postalCode: '',
        country: ''
      }
    };
  },
  created() {
    // Fetch user info and addresses from API
    this.fetchUserInfo();
    this.fetchAddresses();
  },
  methods: {
    async fetchUserInfo() {
      try {
        // Replace with actual API call to fetch user info
        const response = await fetch('/api/user/info');
        const data = await response.json();
        this.userInfo = data; // Assuming data structure matches this.userInfo
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    },
    async fetchAddresses() {
      try {
        // Replace with actual API call to fetch addresses
        const response = await fetch('/api/user/addresses');
        const data = await response.json();
        this.addresses = data.addresses; // Assuming data structure matches this.addresses
      } catch (error) {
        console.error('Error fetching addresses:', error);
      }
    },
    async addAddress() {
      try {
        // Replace with actual API call to add address
        const response = await fetch('/api/user/address/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newAddress)
        });
        const data = await response.json();
        console.log('Address added:', data);
        // Clear new address form fields
        this.newAddress = {
          addressLine1: '',
          addressLine2: '',
          city: '',
          postalCode: '',
          country: ''
        };
        // Refresh addresses
        this.fetchAddresses();
      } catch (error) {
        console.error('Error adding address:', error);
      }
    },
    async deleteAddress(addressId) {
      try {
        // Replace with actual API call to delete address
        const response = await fetch(`/api/user/address/delete/${addressId}`, {
          method: 'DELETE'
        });
        const data = await response.json();
        console.log('Address deleted:', data);
        // Refresh addresses
        this.fetchAddresses();
      } catch (error) {
        console.error('Error deleting address:', error);
      }
    },
    async setPreferredAddress(addressId) {
      try {
        // Replace with actual API call to set preferred address
        const response = await fetch('/api/user/address/set-preferred', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ address_id: addressId })
        });
        const data = await response.json();
        console.log('Preferred address set:', data);
        // Refresh addresses
        this.fetchAddresses();
      } catch (error) {
        console.error('Error setting preferred address:', error);
      }
    },
    async deleteAccount() {
      try {
        // Replace with actual API call to delete user account
        const response = await fetch('/api/user/delete', {
          method: 'DELETE'
        });
        const data = await response.json();
        console.log('User account deleted:', data);
        // Optionally, redirect to a logout or home page
      } catch (error) {
        console.error('Error deleting user account:', error);
      }
    }
  }
};
</script>

<style scoped>
.change-user-info {
  padding: 20px;
}

.b-card {
  margin-top: 20px;
}
</style>
