<template>
    <div dir="rtl" class="verification-page">
        <section class="verification">
            <div class="container">
                <div class="verification-content">
                    <div class="auth-id-box">
                    <b-alert variant="info" show>
                        <strong>your auth_code is {{ authCode }}</strong>
                    </b-alert>
                    </div>
                    <div class="user-id-box">
                    <b-alert variant="info" show>
                        <strong>your user_id is {{ userId }}</strong>
                    </b-alert>
                    </div>
                    <div class="verification-form">
                        <h2 class="form-title">تایید حساب کاربری</h2>
                        <p>لطفا کد تاییدی که دریافت کرده‌اید را در کادر زیر وارد کنید:</p>
                        <b-input-group class="mt-3">
                            <template #prepend>
                                <b-input-group-text>
                                    <font-awesome-icon icon="fa-solid fa-key"/>
                                </b-input-group-text>
                            </template>
                            <b-form-input type="text" placeholder="کد تایید" v-model="authCodeInput"></b-form-input>
                        </b-input-group>
                        <div class="form-group form-button mt-5">
                            <b-button variant="secondary" @click="verify">
                                <b-spinner v-if="loading" label="Spinning"></b-spinner>
                                <span v-else>
                                    تایید
                                </span>
                            </b-button>
                        </div>
                        <p v-if="error" class="error">{{ error }}</p>
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
import { mapGetters } from 'vuex';


export default {
    computed: {
        ...mapGetters(['getUserId', 'getAuthCode']),
        userId() {
        return this.getUserId;
        },
        authCode() {
        return this.getAuthCode;
        }
    },
    data() {
        return {
            user_id : this.getUserId,
            authCodeInput: '',
            loading: false,
            error: ''
        };
    },
    // mounted() {
    //     // Retrieve the userId from local storage
    //     if (!user_id) {
    //         this.$router.push('/SignUp'); // Redirect to SignUp if userId is not found
    //     }
    // },
    methods: {
        verify() {
            this.loading = true;
            const api = "http://localhost:8000/api/v1/auth/verify";
            const data = {
                user_id: this.userId,
                auth_code: this.authCodeInput,
            };
            Vue.axios.post(api, data)
                .then(response => {
                    this.loading = false;
                    this.$router.push('/');
                    if (response.data.success) {
                        // Clear userId and authCode from local storage
                        localStorage.removeItem('userId');
                        localStorage.removeItem('authCode');
                        // Redirect to SignIn page
                        this.$router.push('/');
                    } else {
                        this.$router.push('/');
                        this.error = "کد تایید اشتباه است";
                    }
                })
                .catch(e => {
                    this.$router.push('/');
                    this.loading = false;
                    this.error = e.response.data.detail || "خطایی رخ داده است";
                });

        }
    }
}
</script>

<style scoped>
/* Your existing styles here */
</style>
