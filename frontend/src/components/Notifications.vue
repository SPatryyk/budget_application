<template>
    <div class="notifications-content" :class="{invert: $route.path.includes('/login')}">
        <transition-group
            @enter="onEnter"
            @leave="onLeave"
            :css="false"
        >
            <div class="notification" v-for="(notify, key) in notification.list" :key="key">
                <div class="row">
                    <div class="icon">
                        <i :class="notify.icon"></i>
                    </div>
                    <div class="header">{{ notify.header }}</div>
                </div>
                <div class="text">{{ notify.text }}</div>
            </div>
        </transition-group>
    </div>
</template>
<script>
import { useNotificationStorage } from '../storage/notifications';
import anime from 'animejs'
export default {
    data() {
        return({
            notification: useNotificationStorage()
        })
    },
    methods: {
        onEnter(el, complete) {
            anime({
                targets: el,
                right: ['-10vw', '0vw'],
                paddingTop: ['0vw', '1vw'],
                paddingBottom: ['0vw', '1vw'],
                marginTop: ['0vw', '.5vw'],
                maxHeight: ['0vw', '6vw'],
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                complete: complete
            })
        }, onLeave(el, complete) {
            anime({
                targets: el,
                right: ['0vw', '-10vw'],
                paddingTop: ['1vw', '0vw'],
                paddingBottom: ['1vw', '0vw'],
                marginTop: ['.5vw', '0vw'],
                maxHeight: ['6vw', '0vw'],
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                complete: complete
            })
        }
    }
}
</script>
<style scoped>
    .notifications-content {
        position: absolute;
        right: 5vw;
        bottom: 5vw;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        z-index: 999999999999999999999;
    }

    .notifications-content.invert .notification {
        color: white;
    }

    .notification {
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        padding: 1vw 1.25vw;
        background-color: rgba(0, 0, 0, 0.03);
        color: #1a1a1a;
        max-width: 18vw;
        min-width: 15vw;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }

    .notification .row {
        display: flex;
        gap: .25vw;
        align-items: center;
    }

    .notification .row .icon {
        font-size: .8vw;
    }

    .notification .row .header {
        font-size: .8vw;
        font-weight: 600;
    }

    .notification .text {
        font-size: .65vw;
        opacity: .6;
    }
</style>