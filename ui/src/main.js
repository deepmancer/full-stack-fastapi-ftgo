import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'
import VueAxios from 'vue-axios'
import 'leaflet/dist/leaflet.css';

import {BootstrapVue, IconsPlugin, ToastPlugin} from "bootstrap-vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

/* import the fontawesome core */
import {library} from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

/* import specific icons */
import {
    faArrowRightFromBracket,
    faCircleInfo,
    faClose,
    faCreditCard,
    faDollarSign,
    faEllipsis,
    faEnvelope,
    faFileCirclePlus,
    faGear,
    faHeart,
    faIdCard,
    faLock,
    faMagnifyingGlass,
    faMinus,
    faMoneyCheck,
    faPenToSquare,
    faPhone,
    faPlus,
    faShare,
    faThumbsDown,
    faThumbsUp,
    faTimeline,
    faTrash,
    faUser,
    faUserMinus,
    faUserPlus,
    faUserTie
} from '@fortawesome/free-solid-svg-icons'

Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(ToastPlugin)

Vue.use(VueAxios, axios)

library.add(faUserTie);
library.add(faEnvelope);
library.add(faPhone);
library.add(faLock);
library.add(faUser);
library.add(faIdCard);
library.add(faArrowRightFromBracket);
library.add(faGear);
library.add(faMagnifyingGlass);
library.add(faCircleInfo);
library.add(faShare);
library.add(faPlus);
library.add(faMinus);
library.add(faDollarSign);
library.add(faClose);
library.add(faTrash);
library.add(faUserPlus);
library.add(faUserMinus);
library.add(faThumbsUp);
library.add(faThumbsDown);
library.add(faFileCirclePlus);
library.add(faCreditCard);
library.add(faPenToSquare);
library.add(faMoneyCheck);
library.add(faEllipsis);
library.add(faHeart);
library.add(faTimeline);

Vue.component('font-awesome-icon', FontAwesomeIcon)

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')