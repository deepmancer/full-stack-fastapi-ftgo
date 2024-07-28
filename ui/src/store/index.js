import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userId: null,
        authCode: null,
        token: null,
    },
    mutations: {
        setUserId(state, userId) {
            state.userId = userId;
        },
        setAuthCode(state, authCode) {
            state.authCode = authCode;
        },
        setToken(state, token) {
            state.token = token;
        },
    },
    actions: {
        updateUserId({ commit }, userId) {
            commit('setUserId', userId);
        },
        updateAuthCode({ commit }, authCode) {
            commit('setAuthCode', authCode);
        },
        updateToken({ commit }, token) {
            commit('setToken', token);
        },
    },
    getters: {
        getUserId: state => state.userId,
        getAuthCode: state => state.authCode,
        getToken: state => state.token,
    }
});