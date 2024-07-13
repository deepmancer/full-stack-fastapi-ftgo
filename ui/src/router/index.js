import Vue from 'vue'
import VueRouter from 'vue-router'
import SignUp from '../views/SignUp.vue'
import SignIn from '../views/SignIn.vue'
import CustomerMainPage from '../views/CustomerMainPage.vue'


Vue.use(VueRouter)

const routes = [{
        path: '/',
        name: 'CustomerMainPage',
        component: CustomerMainPage
    },
    {
        path: '/SignUp',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/SignIn',
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