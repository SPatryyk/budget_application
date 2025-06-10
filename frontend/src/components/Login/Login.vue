<template>
    <div class="login-content">
        <div class="form" ref="login-form">
            <div class="header">{{ isLogin ? 'Login' : 'Register'}}</div>
            <input type="text" id="email" placeholder="Email">
            <transition-group
                 @enter="onInputEnter"
                 @leave="onInputLeave"
                 :css="false"   
                >
                <input v-if="!isLogin" type="text" id="username" placeholder="Username" key="usernameContent">
            </transition-group>
            <input type="password" id="password" placeholder="Password">
            <button class="proceed" @click="login">Proceed</button>
            <div class="text-info">
                <div class="text">{{ isLogin ? "Don't have an account?" : "Already have an account?" }}</div>
                <button class="info-button" @click="switchIsLogin">{{ isLogin ? "Register Now" : "Login" }}</button>
            </div>
        </div>
        <div class="side-content">
            <div class="header" ref="header-side">
                <div class="h-1">Home</div>
                <div class="h-2">Budget</div>
            </div>
            <img ref="login-img" src="https://r2.fivemanage.com/9fHGnEBEfnR89IeQ0njaD/213464_1_orig.jpg"/>
        </div>
    </div>
</template>
<script>
import anime from 'animejs'
import {APICall} from '@/utils/apiCall.js'
import { useNotificationStorage } from '../../storage/notifications'
import { useBaseStorage } from '../../storage/base'
export default {
    data() {
        return({
            notifications: useNotificationStorage(),
            base: useBaseStorage(),
            isLogin: true,
        })
    },
    methods: {
        register() {
            const email = document.getElementById('email').value
            const password = document.getElementById('password').value
            const username = document.getElementById('username').value
            APICall('/users/register/', 'POST', {'Content-Type': 'application/json'}, JSON.stringify({
                email: email,
                password: password,
                username: username,
            }), async (status, body)=> {
                if (status != 201) {
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Login', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    this.access()
                }
            })
        },
        login() {
            
            if (!this.isLogin) {
                this.register()
            } else {
                this.access()
            }
        }, 
        access() {
            const email = document.getElementById('email').value
            const password = document.getElementById('password').value
            APICall('/users/login/', 'POST', {'Content-Type': 'application/json'}, JSON.stringify({
                email: email,
                password: password,
            }), async (status, body)=> {
                if (status != 200) {
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Login', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    let bodyData = await body.json()
                    localStorage.setItem('access', bodyData.access)
                    this.$router.push('/landing')
                    APICall('/wallets/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                        if (status != 200) {
                        } else {
                            let bodyData = await body.json()
                            this.base.setWallets(bodyData.slice(0, 8))
                        }
                    })
                    APICall('/goals/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                        if (status != 200) {
                        } else {
                            let bodyData = await body.json()
                            this.base.setGoals(bodyData.slice(0, 8))
                        }
                    })
                    APICall('/transactions/categories/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                        if (status != 200) {
                            //this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                        } else {
                            let bodyData = await body.json()
                            this.base.setCategories(bodyData)
                        }
                    })
                }
                
            })
        },
        switchIsLogin() {this.isLogin = !this.isLogin},
        onInputEnter(el, done) {
            anime({
                targets: el,
                'max-height': ['0vw', '3vw'],
                marginBottom: ['0vw', '.5vw'],
                paddingTop: [0, '.5vw'],
                paddingBottom: [0, '.5vw'],
                opacity: [0, 1],
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                duration: 500,
                complete: done,
            })
        }, onInputLeave(el, done) {
            anime({
                targets: el,
                'max-height': ['3vw', '0vw'],
                marginBottom: ['.5vw', 0],
                paddingTop: ['.5vw', 0],
                paddingBottom: ['.5vw', 0],
                opacity: [1, 0],
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                duration: 400,
                complete: done,
            })
        }
    },
    mounted() {
        anime({
            targets: this.$refs['header-side'],
            delay: 650,
            right: ['20vw', '-10vw'],
            duration: 1250,
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
            update: anim=> {
                if (anim.progress > 35) {
                    this.$refs['login-img'].classList.add('active')
                    this.$refs['header-side'].classList.add('active')
                }
            }
        })

        anime({
            targets: this.$refs['login-form'],
            delay: 950,
            left: ['-20vw', '0'],
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
        })
    },
}
</script>
<style scoped>
    
    .login-content {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        width: 100%;
        height: 100%;
        position: absolute;
        left: 0;
        top: 0;
        overflow: hidden;
    }

    .side-content {
        width: 100%;
        height: 100%;
        display: flex;
        position: relative;
    }

    .side-content img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0%) invert(1);
        transform: scale(2.0);
        transition: transform .48s cubic-bezier(0.075, 0.82, 0.165, 1), filter .125s ease-in-out;
    }

    .side-content img.active {
        filter: brightness(64%) invert(0);
        transform: scale(1.0);
    }

    .side-content .header {
        position: absolute;
        right: 5vw;
        top: 50%;
        z-index: 9999;
        color: white;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        text-transform: uppercase;
        transform: translate(-50%, -50%);
        color: #1a1a1a;
        transition: color .125s ease-in-out;
    }

    .side-content .header.active {color: white;}

    .side-content .header .h-1 {
        font-size: 4vw;
        height: 2.5vw;
    }

    .side-content .header .h-2 {
        font-size: 7vw;
        font-weight: 700;
    }

    .form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 20vw;
        height: 100%;
        box-sizing: border-box;
        padding: 3.5vw;
        flex-shrink: 0;
        position: absolute;
        left: -20vw;
        background-color: white;
        z-index: 99999;
    }

    .form .header {
        font-size: 1.5vw;
        font-weight: 700;
        color: var(--main-color-text);
        text-transform: uppercase;
        margin-bottom: 1vw;
    }

    .form input {
        width: 100%;
        background-color: var(--main-element-bg);
        border: 0;
        outline: 0;
        font-family: 'Montserrat', sans-serif;
        box-sizing: border-box;
        padding: .5vw .75vw;
        font-size: .75vw;
        margin-bottom: .5vw;
    }

    .form button.proceed {
        background-color: transparent;
        border: 0;
        outline: 0;
        font-family: 'Montserrat', sans-serif;
        margin-left: auto;
        font-size: .8vw;
        font-weight: 500;
        padding: 0;
    }
    .form .text-info {
        display: flex;
        width: 100%;
        align-items: center;
        justify-content: center;
        font-size: .6vw;
        margin: 0 auto;
        margin-top: 3vw;
    }

    .form .text-info button.info-button {
        background-color: transparent;
        border: 0;
        outline: 0;
        font-family: 'Montserrat', sans-serif;
        margin-left: .5vw;
        font-weight: 600;
        padding: 0;
        font-size: .6vw;
    }

    #username {
        min-height: 0;
        height: auto;
        opacity: 0;
    }
</style>