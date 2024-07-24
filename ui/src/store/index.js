import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userId: null,
        authCode: null,
    },
    mutations: {
        setUserId(state, userId) {
            state.userId = userId;
        },
        setAuthCode(state, authCode) {
            state.authCode = authCode;
        }
    },
    actions: {
        updateUserId({ commit }, userId) {
            commit('setUserId', userId);
        },
        updateAuthCode({ commit }, authCode) {
            commit('setAuthCode', authCode);
        }
    },
    getters: {
        getUserId: state => state.userId,
        getAuthCode: state => state.authCode,

    }
});