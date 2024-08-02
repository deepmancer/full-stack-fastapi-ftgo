// store/index.js

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userId: null,
        token: null,
        authCode: null,
        restaurantInfo: null,
        vehicleInfo: null,
    },
    mutations: {
        setUserId(state, userId) {
            state.userId = userId;
        },
        setToken(state, token) {
            state.token = token;
        },
        setRestaurantInfo(state, restaurantInfo) {
            state.restaurantInfo = restaurantInfo;
        },
        setVehicleInfo(state, vehicleInfo) {
            state.vehicleInfo = vehicleInfo;
        },
        setAuthCode(state, authCode) {
            state.authCode = authCode;
        },
    },
    actions: {
        updateUserId({ commit }, userId) {
            commit('setUserId', userId);
        },
        updateToken({ commit }, token) {
            commit('setToken', token);
        },
        updateRestaurantInfo({ commit }, restaurantInfo) {
            commit('setRestaurantInfo', restaurantInfo);
        },
        updateVehicleInfo({ commit }, vehicleInfo) {
            commit('setVehicleInfo', vehicleInfo);
        },
        updateAuthCode({ commit }, restaurantInfo) {
            commit('setAuthCode', restaurantInfo);
        }
    },
    getters: {
        getUserId: state => state.userId,
        getToken: state => state.token,
        getRestaurantInfo: state => state.restaurantInfo,
        getVehicleInfo: state => state.vehicleInfo,
        getAuthCode: state => state.authCode,
    }
});