<template>
    <Navbar/>
    <FormView/>
    <RouterView v-slot="{ Component }">
        <transition name="default-transition">
            <component :is="Component" />
        </transition>
    </RouterView>
    <Footer/>
</template>
<script>
import { RouterView } from 'vue-router';
import Navbar from './_Handlers/Navbar.vue';
import Footer from './_Handlers/Footer.vue';
import FormView from './Forms/_Init.vue';
export default {
    components: {Navbar, FormView, Footer}
}
</script>
<style scoped>
    .default-transition-enter-active,
    .default-transition-leave-active {
    transition: all .3s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .default-transition-enter-from {
    }
    .default-transition-leave-to {
        transform: translateY(10%);
        opacity: 0;
    }
</style>