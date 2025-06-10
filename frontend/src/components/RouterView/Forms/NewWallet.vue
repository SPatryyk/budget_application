<template>
    <div class="header">New Wallet</div>
    <Text
        id="wallet_name"
        label="Name"
        placeholder="Credit Card"
        :update="HandleInputUpdate('name')"
    />
    <Select 
         id="wallet_type"
         label="Type"
         :selected="type ? type : ''"
         :list="types"
         :update="HandleInputUpdate('type')"
    />
    
    <Text
        id="wallet_currency"
        label="Currency"
        placeholder="USD"
        :update="HandleInputUpdate('currency')"
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
            name: false,
            currency: false,
            type: false,
            errorExist: true,
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

            availableCurrencies: {usd: 'USD', pln: 'PLN', eur: 'EUR'}
        })
    }, 
    mounted() {
        //get wallets and categories
        this.name = false
        this.currency = false
        this.type = this.types[0]
        this.errorExist = true
    }, 
    methods: {
        handleError() {
            let nameCorrect = this.name != false && this.name.length > 2 && typeof this.name == 'string'
            let typeCorrect = this.type != false && this.types.some(type => type === this.type)
            let currencyCorrect = this.currency != false && this.availableCurrencies[this.currency.toLowerCase()]

            this.errorExist = !nameCorrect || !typeCorrect || !currencyCorrect
        },  
        HandleInputUpdate(input) {
            return updatedVal=> {
                this[input] = updatedVal
                this.handleError()
            }
        }, 
        addTransfer() {
            if (this.errorExist) return this.notification.add('fas fa-exclamation-triangle', 'Form', 'Make sure to fulfill the data properly in the form!')
            APICall('/wallets/', 'POST', {
                Authorization: "Bearer "+localStorage.getItem('access'),
                "Content-Type": "application/json"
            }, JSON.stringify({
                name: this.name,
                type: this.type.id,
                currency: this.currency
            }), async(status, body)=> {
                if (status != 201) {
                    let bodyData = await body.json()
                    this.notification.add('fas fa-exclamation-triangle', 'Form', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    this.notification.add('fas fa-check', 'Form', 'Added new wallet.')
                    setTimeout(()=> {
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