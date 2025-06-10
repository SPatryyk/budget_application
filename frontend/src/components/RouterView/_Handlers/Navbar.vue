<template>
    <div class="navbar">
        <div class="header" @click="switchRoute('/landing')">
            <div class="h-1">Home</div>
            <div class="h-2">Budget</div>
        </div>
        <div class="nav-links-list">
            <div class="nav-link" @click="switchRoute('/wallets')" :class="{active: $route.path.includes('/wallets')}">Wallets</div>
            <div class="nav-link" @click="switchRoute('/goals')" :class="{active: $route.path.includes('/goals')}">Goals</div>
        </div>
        <div class="line"></div>
        <div class="user-data">
            <div class="col">
                <div class="username">{{ this.user.username }}</div>
                <div class="class" @click="Logout">Logout</div>
            </div>
            <div class="icon">
                <i class="fas fa-user"></i>
            </div>
        </div>
    </div>
</template>
<script>
import { useUserStorage } from '../../../storage/user';

export default {
    data() {
        return({
            user: useUserStorage()
        })
    },
    methods: {
        switchRoute(path) {
            this.$router.push(path)
        },
        Logout() {
            localStorage.removeItem('access')
            this.$router.push('/login')
        }
    }
}
</script>
<style scoped>
    .navbar {
        width: 100%;
        display: flex;
        align-items: center;
    }

    .navbar .user-data {
        display: flex;
        gap: .5vw;
        align-items: center;
    }

    .navbar .user-data .col {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        color: #1a1a1a;
    }

    .navbar .user-data .col .username {
        font-size: .8vw;
        font-weight: 600;
    }

    .navbar .user-data .col .class {
        font-size: .65vw;
        font-weight: 500;
        opacity: .3;
    }

    .navbar .user-data .icon {
        width: 3vw;
        height: 3vw;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.05);
        font-size: 1vw;
        color: #1a1a1a;
        border-radius: 50%;
    }

    .navbar .nav-links-list {
        display: flex;
        margin-left: auto;
        gap: .5vw;
    }

    .navbar .nav-links-list .nav-link {
        font-size: .9vw;
        text-transform: uppercase;
        font-weight: 700;
        color: #1a1a1a;
        opacity: .3;
        transition: opacity .125s ease-in-out;
    }

    .navbar .nav-links-list .nav-link:hover, .navbar .nav-links-list .nav-link.active {
        opacity: 1;
    }

    .navbar .line {
        margin: 0 1vw;
        width: .2vw;
        align-self: stretch;
        background-color: black;
        opacity: .1;
    }

    .navbar .header {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        text-transform: uppercase;
        position: relative;
        z-index: 9999999999999999999999;
    }

    .navbar .header .h-1 {
        font-size: calc(4vw * .3);
        height: calc(2.5vw * .3);
    }

    .navbar .header .h-2 {
        font-size: calc(7vw * .3);
        font-weight: 700;
    }
</style>