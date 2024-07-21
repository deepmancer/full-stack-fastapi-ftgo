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
        ...mapActions(['updateUserId']),
        signin() {
            this.loading = true;
            let api = "http://localhost:5020/user/profile/login";
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
                    this.phone = '';
                    this.password = '';
                    this.loading = false;
                    this.$router.push('/CustomerMainPage');
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
.login-button,
.login-button:hover {
    color: white !important;
}

.signup-page {
    padding-top: 80px;
}

.signup-content {
    display: flex;
    display: -webkit-flex;
}

a {
    color: black !important;
}

a:hover {
    color: black !important;
    text-decoration: none !important;
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

.signup {
    margin-bottom: 150px;
}

.signup-content {
    padding: 75px 0;
}

.signup-image {
    margin: 0 55px;
}

.form-title {
    margin-bottom: 33px;
}

.signup-image {
    margin-top: 45px;
}

figure {
    margin-bottom: 50px;
    text-align: center;
}

#signin {
    margin-top: 16px;
}

.signup-image-link {
    font-size: 14px;
    color: #222;
    display: block;
    text-align: center;
}

.signup-form {
    margin-left: 75px;
    margin-right: 75px;
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
</style>
