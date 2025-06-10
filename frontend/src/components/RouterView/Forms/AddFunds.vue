<template>
    <div class="header">Add Funds</div>
    <Number
        id="wallet_amount"
        label="Amount"
        placeholder="5000"
        :update="HandleInputUpdate('amount')"
    />
    <Select 
         id="wallet_type"
         label="Category"
         :selected="category ? category : ''"
         :list="base.categories.list"
         :update="HandleInputUpdate('category')"
    />

    <Select 
         id="wallet_currency"
         label="Currency"
         :selected="currency ? currency : ''"
         :list="availableCurrencies"
         :update="HandleInputUpdate('currency')"
    />
    
    <Text
        id="wallet_description"
        label="Description"
        placeholder="Bought new monitor"
        :update="HandleInputUpdate('description')"
    />
    <button @click="addTransfer">Add Wallet</button>
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
            category: false,
            errorExist: true,
            currency: false,
            types: [
                {
                    name: 'Cash',
                    id: 'cash',
                },
                {
                    name: 'Bank',
                    id: 'bank',
                }
            ],

            availableCurrencies: [
                {
                    name: 'USD',
                },
                {
                    name: 'EUR'
                },
                {
                    name: 'PLN'
                }
            ]
        })
    }, 
    mounted() {
        //get wallets and categories
        this.amount = false,
        this.description = false,
        this.category = this.base.categories.list[0]
        this.currency = this.availableCurrencies[0]
        this.errorExist = true
    }, 
    methods: {
        handleError() {
            let amountCorrect = this.amount != false
            let descriptionCorrect = this.description != false && this.description.length > 2 
            
            this.errorExist = !amountCorrect || !descriptionCorrect 
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


            APICall('/transactions/', 'POST', {
                Authorization: "Bearer "+localStorage.getItem('access'),
                "Content-Type": "application/json"
            }, JSON.stringify({
                wallet: this.base.wallets.selected.id,
                currency: this.currency.name,
                type: this.amount > 0 ? 'income' : 'expense',
                amount: this.amount,
                category_id: this.category.id,
                description: this.description,
                date: formattedDate
            }), async(status, body)=> {
                if (status != 201) {
                    let bodyData = await body.json()
                    this.notification.add('fas fa-exclamation-triangle', 'Form', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    this.notification.add('fas fa-check', 'Wallets', 'Added amount to balance.')
                    setTimeout(()=> {
                        APICall('/wallets', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
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

                    this.$router.push('/wallets')
                    this.base.setForm(false)
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