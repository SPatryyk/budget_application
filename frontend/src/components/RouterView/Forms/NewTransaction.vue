<template>
    <div class="header">New Transaction</div>
    <Select
        id="new_transaction_category"
        label="Wallet"
        :selected="wallet ? wallet : ''"
        :list="base.wallets.list"
        :update="HandleInputUpdate('wallet')"
    />
    <Number
        id="new_transaction_amount"
        label="Amount"
        placeholder="5000"
        :update="HandleInputUpdate('amount')"
    />
    <Text
        id="new_transaction_description"
        label="Description"
        placeholder="Bought new monitor"
        :update="HandleInputUpdate('description')"
    />
    <!-- <Select
        id="new_transaction_category"
        label="Category"
        :selected="category ? category : ''"
        :list="base.categories.list"
        :update="HandleInputUpdate('category')"
    /> -->
    <button @click="addTransaction">Add Transaction</button>
</template>
<script>
import { useBaseStorage } from '../../../storage/base';
import { useNotificationStorage } from '../../../storage/notifications';
import Number from './Inputs/Number.vue';
import Select from './Inputs/Select.vue';
import Text from './Inputs/Text.vue';
import { APICall } from '../../../utils/apiCall';
export default {
    components: {Number, Text, Select},
    data() {
        return({
            base: useBaseStorage(),
            notification: useNotificationStorage(),
            amount: false,
            description: false,
            category: false,
            wallet: false,
            errorExist: true,
        })
    }, 
    mounted() {
        //get wallets and categories

        this.amount = false
        this.description = false
        this.category = false
        this.category = this.base.categories.list[0]
        this.wallet = this.base.wallets.list[0]
        console.log(this.wallet);
        
        
    }, 
    methods: {
        handleError() {
            let amountCorrect = this.amount != false && this.amount > 0 && typeof this.amount == 'number'
            let descriptionCorrect = this.description != false && this.description.length > 5 && typeof this.description == 'string'
            let walletCorrect = this.wallet && this.base.wallets.list.some(wallet => wallet.id === this.wallet.id) && typeof this.wallet == 'object'
            
            this.errorExist = !amountCorrect || !descriptionCorrect || !walletCorrect
            
        },  
        HandleInputUpdate(input) {
            return updatedVal=> {
                this[input] = updatedVal
                this.handleError()
            }
        }, 
        addTransaction() {
            if (this.errorExist) return this.notification.add('fas fa-exclamation-triangle', 'Form', 'Make sure to fulfill the data properly in the form!')
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');

            const formattedDate = `${yyyy}-${mm}-${dd}`;
            APICall('/wallets/transfers/', 'POST', {
                Authorization: "Bearer "+localStorage.getItem('access'),
                "Content-Type": "application/json"
            }, JSON.stringify({
                from_wallet: this.wallet.id,
                to_goal: this.base.goal.data.id,
                amount: this.amount,
                description: this.description,
                date: formattedDate,
            }), async(status, body)=> {
                if (status != 201) {
                    let bodyData = await body.json()
                    this.notification.add('fas fa-exclamation-triangle', 'Form', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    setTimeout(()=> {
                        APICall('/goals/'+this.base.goal.data.id, 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                            if (status != 200) {
                                console.log(body);
                                
                                let bodyData = await body.json()
                                console.log(bodyData);
                                this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                            } else {
                                let bodyData = await body.json()
                                this.base.setGoalSelected(true, bodyData)
                                APICall('/goals/transactions/?goal='+this.base.goal.data.id, 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                                    if (status != 200) {
                                        console.log(body);
                                        
                                        let bodyData = await body.json()
                                        console.log(bodyData);
                                        this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                                    } else {
                                        let bodyData = await body.json()
                                        this.base.setGoalTransactions(bodyData)
                                    }
                                })  
                            }
                        })  
                    }, 200)
                    this.base.setForm(false)
                    this.notification.add('fas fa-check', 'Form', 'Added new transaction.')
                }
            })
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