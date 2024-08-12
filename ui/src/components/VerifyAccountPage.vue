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
import {BVToastPlugin} from "bootstrap-vue";
import {mapGetters} from 'vuex';

Vue.use(VueAxios, axios);
Vue.use(BVToastPlugin);


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
                        localStorage.removeItem('userId');
                        localStorage.removeItem('authCode');

                        this.$router.push('/');
                    } else {
                         this.$bvToast.toast('کد تایید اشتباه است.', {
                            title: 'Error',
                            variant: 'danger',
                            solid: true,
                            autoHideDelay: 5000,
                        });
                    }
                })
                .catch(e => {
                    if (e.response.data.detail.detail) {
                        this.$bvToast.toast(e.response.data.detail.detail, {
                            title: 'Error',
                            variant: 'danger',
                            solid: true,
                            autoHideDelay: 5000,
                        });

                    } else {
                        this.$bvToast.toast('مشکلی در تایید حساب کاربری پیش آمد، لطفا مقادیر ورودی را چک کنید و مجددا تلاش کنید.', {
                            title: 'Error',
                            variant: 'danger',
                            solid: true,
                            autoHideDelay: 5000,
                        });
                    }
                    this.loading = false;
                });

        }
    }
}
</script>

<style scoped>
/* Your existing styles here */
</style>
