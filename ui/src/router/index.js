import Vue from 'vue'
import VueRouter from 'vue-router'
import SignUp from '../views/SignUp.vue'
import SignIn from '../views/SignIn.vue'
import CustomerMainPage from '../views/CustomerMainPage.vue'
import CustomerChangeInfo from '../views/CustomerChangeInfo.vue'
import DeliveryMainPage from '../views/DeliveryMainPage.vue'
import SupplierMainPage from '../views/SupplierMainPage.vue'
import VerifyAccountPage from '../views/VerifyAccountPage.vue'
import ChangeRestaurantInfo from '../views/ChangeRestaurantInfo.vue'
import RegisterRestaurantPage from '../views/RegisterRestaurantPage.vue'


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
        path: '/SupplierMainPage',
        name: 'SupplierMainPage',
        component: SupplierMainPage
    },
    {
        path: '/RegisterRestaurantPage',
        name: 'RegisterRestaurantPage',
        component: RegisterRestaurantPage
    },
    {
        path: '/CustomerChangeInfo',
        name: 'CustomerChangeInfo',
        component: CustomerChangeInfo
    },
    {
        path: '/ChangeRestaurantInfo',
        name: 'ChangeRestaurantInfo',
        component: ChangeRestaurantInfo
    },
    {
        path: '/SignUp',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/VerifyAccount',
        name: 'VerifyAccount',
        component: VerifyAccountPage
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