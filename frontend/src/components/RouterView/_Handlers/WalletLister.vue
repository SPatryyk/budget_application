<template>
    <div class="wallet">
        <div class="icon" @mousedown.left="addDirectFunds" @mousedown.right="transferFunds" @contextmenu.prevent>
            <template v-if="type == 'cash'">
                <i class="fas fa-coins"></i>
            </template>
            <template v-else-if="type == 'bank'">
                <i class="far fa-credit-card"></i>
            </template>
        </div>
        <div class="col">
            <input class="header" :value="name" @keydown.enter="handleHeaderUpdate">
            <div class="name">Currency <input class="currency" :value="currency" @keydown.enter="handleCurrencyUpdate"></div>
        </div>
        <div class="balance">
            <div class="value">{{ balance.toLocaleString('en-US', {style: 'currency', currency: 'USD' }).replace('$', '').replace(',', ' ') }}</div>
            <div class="currency">{{ currency }}</div>
        </div>
        <div class="trash-wallet" @click="callbackRemove(id)">
            <i class="fas fa-trash"></i>
        </div>
    </div>
</template>
<script>
import { useBaseStorage } from '../../../storage/base'

export default {
    data() {
        return({
            base: useBaseStorage()
        })
    },  
    props: {
        id: String,
        name: String,
        balance: Number,
        currency: String,
        type: String,
        rawObject: Object,
        callbackRemove: Function,
        callbackUpdateCurrency: Function,
        callbackUpdateHeader: Function
    },
    methods: {
        addDirectFunds(e) {
            e.preventDefault()
            this.base.setSelectedWalletId({id: this.id, currency: this.currency})
            this.base.setForm(true, 'addFunds')
        },
        transferFunds(e) {
            e.preventDefault();
            this.base.setForm(true, 'transfer')
        },
        handleHeaderUpdate(e) {
            const value = e.target.value
            this.callbackUpdateHeader(this.rawObject, value)
        },
        handleCurrencyUpdate(e) {
            const value = e.target.value
            this.callbackUpdateCurrency(this.rawObject, value)
        }
    }
}
</script>
<style scoped>
    .wallet {
        display: flex;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.05);
        box-sizing: border-box;
        padding: 1vw 1.2vw;
        position: relative;
        width: 25vw;
        color: #1a1a1a;
    }

    .wallet:hover .trash-wallet {width: 3.5vw;}
    input.header {
        background-color: transparent;
        font-size: .95vw;
        font-weight: 700;
        text-transform: uppercase;
        font-family: 'Montserrat', sans-serif;
        border: 0;
        padding: 0;
        margin: 0;
        outline: 0;
    }

    input.currency {
        background-color: transparent;
        font-size: .6vw;
        font-weight: 600;
        text-transform: uppercase;
        color: rgba(0, 0, 0, 1);
        text-transform: uppercase;
        font-family: 'Montserrat', sans-serif;
        border: 0;
        padding: 0;
        margin: 0;
        outline: 0;
    }
    .wallet .trash-wallet {
        overflow: hidden;
        width: 0vw;
        height: 100%;
        position: absolute;
        left: 100%;
        top: 0;
        background-color: rgba(212, 77, 77, 0.815);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1vw;
        color: #1a1a1a;
        transition: width .48s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .wallet .icon {
        font-size: 1.5vw;
        margin-right: 1.2vw;
    }

    .wallet .col {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .wallet .col .header {
        font-size: .95vw;
        font-weight: 700;
        text-transform: uppercase;
    }

    .wallet .col .name {
        display: flex;
        gap: .25vw;
        font-size: .6vw;
        font-weight: 400;
        text-transform: uppercase;
        color: rgba(0, 0, 0, 0.3);
    }

    .wallet .col .name span {color: #1a1a1a;}
    .wallet .balance {
        display: flex;
        flex-direction: column;
        margin-left: auto;
        align-items: flex-end;
    }

    .wallet .balance .value {
        font-size: .9vw;
        height: .9vw;
        font-weight: 600;
    }

    .wallet .balance .currency {
        font-size: .5vw;
    }
</style>