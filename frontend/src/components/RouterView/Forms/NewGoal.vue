<template>
    <div class="header">New Goal</div>
    <Text
        id="goal_name"
        label="Name"
        placeholder="Holidays 2025"
        :update="HandleInputUpdate('name')"
    />
    <Number
        id="goal_target_amount"
        label="Target amount"
        placeholder="5000"
        :update="HandleInputUpdate('amount')"
    />
    
    <Text
        id="goal_deadline"
        label="Deadline"
        placeholder="YYYY-MM-DD"
        :update="HandleInputUpdate('deadline')"
    />
    <button @click="addTransfer">Add Goal</button>
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
            amount: false,
            deadline: false,
            errorExist: true,
            
        })
    }, 
    mounted() {
        //get wallets and categories
        this.name = false
        this.amount = false
        this.deadline = false
        this.errorExist = true
    }, 
    methods: {
        handleError() {
            const DatePattern = /^\d{4}-\d{2}-\d{2}$/;
            let nameCorrect = this.name != false && this.name.length > 2 && typeof this.name == 'string'
            let amountCorrect = this.amount != false && this.amount > 0 && typeof this.amount == 'number'
            let dateCorrect = this.deadline != false && DatePattern.test(this.deadline)
            console.log(this.deadline);
            
            console.log(nameCorrect, amountCorrect, dateCorrect, DatePattern.test(this.deadline));

            this.errorExist = !nameCorrect || !amountCorrect || !dateCorrect
        },  
        HandleInputUpdate(input) {
            return updatedVal=> {
                this[input] = updatedVal
                this.handleError()
            }
        }, 
        addTransfer() {
            if (this.errorExist) return this.notification.add('fas fa-exclamation-triangle', 'Form', 'Make sure to fulfill the data properly in the form!')
            APICall('/goals/', 'POST', {
                Authorization: "Bearer "+localStorage.getItem('access'),
                "Content-Type": "application/json"
            }, JSON.stringify({
                name: this.name,
                target_amount: this.amount,
                deadline: this.deadline
            }), async(status, body)=> {
                if (status != 201) {
                    let bodyData = await body.json()
                    this.notification.add('fas fa-exclamation-triangle', 'Form', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    this.notification.add('fas fa-check', 'Form', 'Added new goal.')
                    setTimeout(()=> {
                        APICall('/goals/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                            if (status != 200) {
                                console.log(body);
                                
                                let bodyData = await body.json()
                                console.log(bodyData);
                                this.notifications.add('fas fa-exclamation-triangle', 'Login', bodyData[Object.keys(bodyData)[0]][0])
                            } else {
                                let bodyData = await body.json()
                                this.base.setGoals(bodyData.slice(0, 10))
                            }
                        })
                    }, 100)
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