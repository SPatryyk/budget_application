import {createRouter, createWebHistory} from 'vue-router'
import Login from './components/Login/Login.vue'
import Router from './components/RouterView/Router.vue'
import Landing from './components/RouterView/Landing/Landing.vue'
import Wallets from './components/RouterView/Wallets/Wallets.vue'
import Goals from './components/RouterView/Goals/Goals.vue'

const routes = [
    {
        path: '/login',
        name: 'login',
        component: Login,
    }, 
    {
        path: '/',
        name: 'main',
        component: Router,
        children: [
            {
                path: 'landing',
                name: 'landing',
                component: Landing,
            }, {
                path: 'wallets',
                name: 'wallets',
                component: Wallets,
            },  {
                path: 'goals',
                name: 'goals',
                component: Goals,
            }, 
        ]
    }, 
]

const router = createRouter({
    routes,
    history: createWebHistory()
})

export default router