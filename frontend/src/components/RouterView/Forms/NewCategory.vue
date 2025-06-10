<template>
    <div class="header">New Category</div>
    <Select
        id="category_type"
        label="Type"
        :selected="type ? type : ''"
        :list="typesList"
        :update="HandleInputUpdate('type')"
    />
    <Text
        id="category_name"
        label="Category"
        placeholder="Job payout"
        :update="HandleInputUpdate('category')"
    />

    <button @click="addTransfer">Add Category</button>
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
            category: false,
            errorExist: true,
            type: false,
            typesList: [
                {
                    id: 'expense',
                    name: 'Expense',
                },
                {
                    id: 'income',
                    name: 'Income',
                }
            ],
        })
    }, 
    mounted() {
        //get wallets and categories
        this.category = false
        this.type = this.typesList[0]
    }, 
    methods: {
        handleError() {
            let categoryCorrect = this.category != false && this.category.length > 2 && typeof this.category == 'string'
            let typeCorrect = this.type && this.typesList.some(type => type.name === this.type.name) && typeof this.type == 'object'
            this.errorExist = !categoryCorrect || !typeCorrect
        },  
        HandleInputUpdate(input) {
            return updatedVal=> {
                this[input] = updatedVal
                this.handleError()
            }
        }, 
        addTransfer() {
            if (this.errorExist) return this.notification.add('fas fa-exclamation-triangle', 'Form', 'Make sure to fulfill the data properly in the form!')
            ///api/transactions/categories/
            APICall('/transactions/categories/', 'POST', {
                Authorization: "Bearer "+localStorage.getItem('access'),
                "Content-Type": "application/json"
            }, JSON.stringify({
                name: this.category,
                type: this.type.id,
            }), async(status, body)=> {
                if (status != 201) {
                    let bodyData = await body.json()
                    this.notification.add('fas fa-exclamation-triangle', 'Form', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    this.notification.add('fas fa-check', 'Form', 'Added new category.')
                    setTimeout(()=> {
                        APICall('/transactions/categories', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                            if (status != 200) {
                                console.log(body);
                                
                                let bodyData = await body.json()
                                console.log(bodyData);
                                this.notifications.add('fas fa-exclamation-triangle', 'Category', bodyData[Object.keys(bodyData)[0]][0])
                            } else {
                                let bodyData = await body.json()
                                this.base.setCategories(bodyData)
                            }
                        })  
                    }, 100)
                    this.base.setForm(false)
                }
            })
            this.base.setForm(false)
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