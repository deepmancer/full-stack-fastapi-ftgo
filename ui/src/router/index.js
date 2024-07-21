import Vue from 'vue'
import VueRouter from 'vue-router'
import SignUp from '../views/SignUp.vue'
import SignIn from '../views/SignIn.vue'
import CustomerMainPage from '../views/CustomerMainPage.vue'
import CustomerChangeInfo from '../views/CustomerChangeInfo.vue'
import DeliveryMainPage from '../views/DeliveryMainPage.vue'
import SupplierMainPage from '../views/SupplierMainPage.vue'


Vue.use(VueRouter)

const routes = [{
        path: '/CustomerMainPage',
        name: 'CustomerMainPage',
        component: CustomerMainPage
    },
    {
        path: '/DeliveryMain',
        name: 'DeliveryMainPage',
        component: DeliveryMainPage
    },
    {
        path: '/SupplierMain',
        name: 'SupplierMainPage',
        component: SupplierMainPage
    },{
        path: '/CustomerChangeInfo',
        name: 'CustomerChangeInfo',
        component: CustomerChangeInfo
    },
    {
        path: '/SignUp',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/',
        name: 'SignIn',
        component: SignIn
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router