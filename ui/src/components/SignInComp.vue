<template>
    <div dir="rtl" class="signup-page">
        <section class="signup">
            <div class="container">
                <div class="signup-content">
                    <div class="signup-form">
                        <h2 class="form-title">ورود</h2>
                        <form class="register-form" id="register-form">
                            <b-input-group class="mt-3">
                                <template #prepend>
                                    <b-input-group-text>
                                        <font-awesome-icon icon="fa-solid fa-phone"/>
                                    </b-input-group-text>
                                </template>
                                <b-form-input placeholder="تلفن همراه" v-model="phone"></b-form-input>
                            </b-input-group>
                            <b-input-group class="mt-3">
                                <template #prepend>
                                    <b-input-group-text>
                                        <font-awesome-icon icon="fa-solid fa-lock"/>
                                    </b-input-group-text>
                                </template>
                                <b-form-input type="password" placeholder="رمزعبور" v-model="password"></b-form-input>
                            </b-input-group>
                            <b-input-group class="mt-3">
                                <b-form-select placeholder="نقش" v-model="userRole" :options="userRoles" class="w-100"></b-form-select>
                            </b-input-group>
                            <div v-if="showVerificationCode" class="mt-3">
                                <b-input-group>
                                    <template #prepend>
                                        <b-input-group-text>
                                            <font-awesome-icon icon="fa-solid fa-key"/>
                                        </b-input-group-text>
                                    </template>
                                    <b-form-input type="text" placeholder="کد تایید" v-model="verificationCode"></b-form-input>
                                </b-input-group>
                                <b-button variant="secondary" class="mt-3" @click="verifyAccount">تایید</b-button>
                            </div>
                            <div class="form-group form-button mt-5">
                                <b-button variant="secondary" @click="signin">
                                    <b-spinner v-if="loading" label="Spinning"></b-spinner>
                                    <span v-else>
                                        ورود
                                    </span>
                                </b-button>
                            </div>
                        </form>
                    </div>
                    <div class="signup-image">
                        <figure><img src="../../images/signin-image.jpg" alt="sign up image"></figure>
                        <router-link class="signup-image-link" to="/SignUp">من که حساب کاربری ندارم :(</router-link>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);
import { BVToastPlugin } from "bootstrap-vue";
Vue.use(BVToastPlugin);
import { mapActions } from 'vuex';

export default {
    data() {
        return {
            phone: "",
            password: "",
            userRole: 'customer',
            userRoles: [
                { value: 'customer', text: 'مشتری' },
                { value: 'courier', text: 'پیک' },
                { value: 'restaurant', text: 'رستوران' }
            ],
            loading: false,
            showVerificationCode: false,
            verificationCode: '',
            userId: null,
        }
    },
    methods: {
        ...mapActions(['updateUserId', 'updateToken']),
        signin() {
            this.loading = true;
            let api = "http://localhost:8000/api/v1/auth/login";
            const data = {
                phone_number: this.phone,
                role: this.userRole,
                password: this.password,
            };
            Vue.axios.post(api, data)
                .then(response => {
                    localStorage.removeItem('token');
                    localStorage.setItem('token', response.data.user_id);
                    this.updateUserId(response.data.user_id);  // Store the user ID in Vuex
                    this.updateToken(response.data.auth_code);  // Store the user ID in Vuex
                    this.phone = '';
                    this.password = '';
                    this.loading = false;

                    // Redirect based on user role
                    switch (this.userRole) {
                        case 'customer':
                            this.$router.push('/CustomerMainPage');
                            break;
                        case 'courier':
                            this.$router.push('/DeliveryMainPage');
                            break;
                        case 'restaurant':
                            this.$router.push('/SupplierMainPage');
                            break;
                        default:
                            this.$router.push('/');
                    }
                })
                .catch(e => {
                    if (e.response && e.response.data.detail === "Account not verified") {
                        this.showVerificationCode = true;
                        this.userId = e.response.data.user_id; // Store the user ID for verification
                    } else {
                        console.log(e.response.data.detail);
                        this.$bvToast.toast(e.response.data.detail[0].msg, { title: 'پیام خطا', autoHideDelay: 5000, appendToast: true });
                        this.phone = '';
                        this.password = '';
                        this.loading = false;
                    }
                });
        },
        verifyAccount() {
            let api = "http://localhost:5020/user/profile/verify";
            const data = {
                user_id: this.userId,
                auth_code: this.verificationCode,
            };
            Vue.axios.post(api, data)
                .then(response => {
                    if (response.data.success) {
                        // Retry login after successful verification
                        this.signin();
                    } else {
                        this.$bvToast.toast("Verification failed. Please try again.", { title: 'Verification Error', autoHideDelay: 5000, appendToast: true });
                    }
                })
                .catch(e => {
                    console.log(e.response.data.detail);
                    this.$bvToast.toast(e.response.data.detail[0].msg, { title: 'Verification Error', autoHideDelay: 5000, appendToast: true });
                });
        }
    }
}
</script>

<style scoped>
/* Your existing styles here */
</style>
