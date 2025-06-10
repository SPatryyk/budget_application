<template>
    <div class="header">New Transfer</div>
    <Select
        id="new_transfer_from_wallet"
        label="From Wallet"
        :selected="wallet ? wallet : ''"
        :list="walletsList"
        :update="HandleInputUpdate('wallet')"
    />
    <template v-if="base.goal.selected">
        <PlaceholderX
            id="new_transfer_placeholder"
            :value="base.goal.data.name"
            label="Goal"
        />
    </template>
    <template v-else>
        <Select 
            id="new_transfer_to_wallet"
            label="To Wallet"
            :selected="toWallet ? toWallet : ''"
            :list="toWalletGoal"
            :update="HandleInputUpdate('toWallet')"
        />
    </template>
    <Number
        id="new_transfer_amount"
        label="Amount"
        placeholder="5000"
        :update="HandleInputUpdate('amount')"
    />
    <Text
        id="new_transfer_description"
        label="Description"
        placeholder="Bought new monitor"
        :update="HandleInputUpdate('description')"
    />

    <button @click="addTransfer">Add Transfer</button>
</template>
<script>
import { useBaseStorage } from '../../../storage/base';
import { useNotificationStorage } from '../../../storage/notifications';
import Number from './Inputs/Number.vue';
import Select from './Inputs/Select.vue';
import Text from './Inputs/Text.vue';
import PlaceholderX from './Inputs/Placeholder.vue';
import { APICall } from '../../../utils/apiCall';
export default {
    components: {Number, Text, PlaceholderX, Select},
    data() {
        return({
            base: useBaseStorage(),
            notification: useNotificationStorage(),
            amount: false,
            description: false,
            category: false,
            wallet: false,
            toWallet: false,
            errorExist: true,
            categoriesList: [
                {
                    id: 'aldsuoiewqtoiwet',
                    name: 'Groceries',
                    type: 'expense'
                },
                {
                    id: 'asdotwqtoiewdjgkadrhd',
                    name: 'Media',
                    type: 'expense'
                }
            ],
            toWalletGoal: [],
            walletsList: []
        })
    }, 
    mounted() {
        this.amount = false
        this.description = false
        this.wallet = this.base.wallets.list[0]

        APICall('/goals', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
            if (status != 200) {
                console.log(body);
                
                let bodyData = await body.json()
                console.log(bodyData);
                this.notifications.add('fas fa-exclamation-triangle', 'Form', bodyData[Object.keys(bodyData)[0]][0])
            } else {
                let bodyData = await body.json()
                bodyData.forEach(obj => {
                    obj.name = `Goal - ${obj.name}`
                });
                this.toWalletGoal = bodyData
                let arr = this.base.wallets.list.map(obj => ({ ...obj }))
                arr.forEach(obj => {
                    obj.name = `Wallet - ${obj.name}`
                })
                this.toWalletGoal = this.toWalletGoal.concat(arr)
                this.toWallet = this.toWalletGoal[0]
            }
        })
    }, 
    methods: {
        handleError() {
            let amountCorrect = this.amount != false && this.amount > 0 && typeof this.amount == 'number'
            let descriptionCorrect = this.description != false && this.description.length > 5 && typeof this.description == 'string'
            let walletCorrect = this.wallet && this.base.wallets.list.some(wallet => wallet.name === this.wallet.name) && typeof this.wallet == 'object'
            this.errorExist = !amountCorrect || !descriptionCorrect || !walletCorrect
        },  
        HandleInputUpdate(input) {
            return updatedVal=> {
                this[input] = updatedVal
                this.handleError()
            }
        }, 
        addTransfer() {
            if (this.errorExist) return this.notification.add('fas fa-exclamation-triangle', 'Form', 'Make sure to fulfill the data properly in the form!')
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            const formattedDate = `${yyyy}-${mm}-${dd}`;

            APICall('/wallets/transfers/', 'POST', {
                'Authorization': 'Bearer '+localStorage.getItem('access'),
                "Content-Type": "application/json"
            }, JSON.stringify({
                from_wallet: this.wallet.id,
                to_goal: this.toWallet.name.startsWith("Goal") ? this.toWallet.id : null,
                to_wallet: this.toWallet.name.startsWith("Wallet") ? this.toWallet.id : null,
                amount: this.amount,
                description: this.description,
                date: formattedDate,
            }), async (status, body)=> {
                if (status != 201) {
                    console.log(body);
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Form', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    let bodyData = await body.json()
                    
                }
            })
            this.base.setForm(false)
            this.notification.add('fas fa-check', 'Form', 'Added new transfer.')
        }
    }
}
</script>
<style scoped>
    .header {
        font-size: 2vw;
        font-weight: 700;
        transform: translateY(-2vw);
    }

    button {
        transform: translateY(2vw);
        background-color: var(--main-element-bg);
        border: 0;
        outline: 0;
        width: 50%;
        box-sizing: border-box;
        padding: .5vw;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: .7vw;
        margin: 0 auto;
        transition: width .48s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    button:hover {
        width: 100%;
    }
</style>