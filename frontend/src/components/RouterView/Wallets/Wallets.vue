<template>
    <div class="wallets-content">
        <div class="left-panel" ref="wallet-left-panel">
            <div class="element" v-for="wallet in base.wallets.list">
                <WalletLister
                    :id="wallet.id"
                    :name="wallet.name"
                    :currency="wallet.currency"
                    :balance="wallet.balance"
                    :type="wallet.type"
                    :rawObject="wallet"
                    :callbackRemove="removeWallet"
                    :callbackUpdateHeader="handleUpdate('name')"
                    :callbackUpdateCurrency="handleUpdate('currency')"
                />
            </div>
            <div class="wallet-new" @click="addNewWallet">Add new balance</div>
        </div>
        <div class="right-panel">
            <div class="header">
                <div class="h-1" ref="wallet-right-panel-1">Wallets</div>
                <div class="h-2" ref="wallet-right-panel-2">Configure and handle your available wallets</div>
            </div>
        </div>
    </div>
    
</template>
<script>
import WalletLister from '../_Handlers/WalletLister.vue';
import anime from 'animejs';
import { APICall } from '../../../utils/apiCall';
import { useBaseStorage } from '../../../storage/base';
import { useNotificationStorage } from '../../../storage/notifications';
export default {
    components: {WalletLister},
    methods: {
        handleUpdate(element) {
            return (rawObject, val)=> {
                let object = {
                    name: rawObject.name,
                    currency: rawObject.currency,
                    type: rawObject.type
                }

                object[element] = val
                
                APICall('/wallets/'+rawObject.id+'/', 'PUT', {
                    Authorization: "Bearer "+localStorage.getItem('access'),
                    "Content-Type": "application/json"
                }, JSON.stringify(object), async (status, body)=> {
                    if (status != 200) {
                        console.log(body);
                        
                        let bodyData = await body.json()
                        console.log(bodyData);
                        this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                    } else {
                        setTimeout(()=>{
                            console.log('x');
                            
                            APICall('/wallets/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                                if (status != 200) {
                                    console.log(body);
                                    
                                    let bodyData = await body.json()
                                    console.log(bodyData);
                                    this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                                } else {
                                    let bodyData = await body.json()
                                    this.base.setWallets(bodyData.slice(0, 8))
                                }
                            })
                        }, 100)
                    }
                })
            }
        },  
        addNewWallet() {
            this.base.setForm(true, 'wallet')
        },
        removeWallet(id) {
            APICall('/wallets/'+id+'/', 'DELETE', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
            if (status != 204) {
                console.log(body);
                
                let bodyData = await body.json()
                console.log(bodyData);
                this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
            } else {
                setTimeout(()=>{
                    console.log('x');
                    
                    APICall('/wallets/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                        if (status != 200) {
                            console.log(body);
                            
                            let bodyData = await body.json()
                            console.log(bodyData);
                            this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                        } else {
                            let bodyData = await body.json()
                            this.base.setWallets(bodyData.slice(0, 8))
                        }
                    })
                }, 100)
            }
        })
        }
    },
    data() {
        return({
            base: useBaseStorage(),
            notifications: useNotificationStorage()
        })
    }, mounted() {
        APICall('/wallets/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
            if (status != 200) {
                console.log(body);
                
                let bodyData = await body.json()
                console.log(bodyData);
                this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
            } else {
                let bodyData = await body.json()
                this.base.setWallets(bodyData.slice(0, 8))
            }
        })
        anime({
            targets: this.$refs['wallet-right-panel-1'],
            duration: 1200,
            translateY: ['-5vw', 0],
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)'
        })
        anime({
            targets: this.$refs['wallet-right-panel-2'],
            translateY: ['8vw', 0],
            duration: 2250,
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)'
        })

        anime({
            targets: this.$refs['wallet-left-panel'],
            translateX: ['-8vw', 0],
            delay: 300,
            duration: 1950,
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)'
        })
    }
}
</script>
<style scoped>
    .wallets-content {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: space-between;
        overflow: hidden;
    }

    .wallets-content .right-panel {
        width: 50%;
        display: flex;
        flex-direction: column;
        align-items: cener;
        justify-content: center;
    }

    .wallets-content .right-panel .header {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .wallets-content .right-panel .header .h-1 {
        font-size: 3vw;
        text-transform: uppercase;
        font-weight: 700;height: 3.3vw;
    }

    .wallets-content .right-panel .header .h-2 {
        font-size: .9vw;
        font-weight: 400;
    }

    .wallets-content .left-panel {
        width: 50%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        gap: .5vw;
    }

    .wallets-content .left-panel  .wallet-new {
        width: 25vw;
        background-color: rgba(0, 0, 0, 0.05);
        box-sizing: border-box;
        padding: 1vw 1.25vw;
        text-align: center;
        text-transform: uppercase;
        font-weight: 600;
        font-size: .9vw;
        margin-left: 0;
        transition: margin-left .48s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .wallets-content .left-panel  .wallet-new:hover {
        margin-left: 2vw;
    }
</style>