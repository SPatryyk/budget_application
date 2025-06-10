<template>
    <div class="landing-content">
        <div class="left-panel">
            <div class="panel-containment panel-slider-1" ref="landing-left-panel-1">
                <div class="panel-liner">Goals Progress</div>
                <template v-if="goals.length == 0">
                    <div class="element">
                        <div class="tex">Create a goal!</div>
                    </div>
                </template>
                <template v-else>
                    <div class="element" v-for="goal in goals">
                        <GoalsLister 
                            :name="goal.id"
                            :header="goal.name"
                            :amount="goal.current_amount"
                            :deadline="goal.deadline"
                            :targetAmount="goal.target_amount"
                        />
                    </div>
                </template>
            </div>

            <div class="panel-containment panel-slider-1" ref="landing-left-panel-2">
                <div class="panel-liner">Recent transactions</div>
                <template v-if="transactions.length == 0">
                    <div class="element">
                        <div class="tex">Add transactions!</div>
                    </div>
                </template>
                <template v-else>
                    <div class="element" v-for="transaction in transactions">
                        <TransactionLister 
                            :type="transaction.type"
                            :amount="transaction.amount"
                            :category="transaction.category?.name"
                            :description="transaction.description"
                            :date="transaction.date"
                        />
                    </div>
                </template>
            </div>
            
        </div>
        <div class="right-panel">
            <div class="header">
                <div class="h-1" ref="welcome-text-panel">Welcome,</div>
                <div class="h-2" ref="user-text-panel">{{ user.username }}</div>
            </div>
        </div>
    </div>
</template>
<script>
import { useUserStorage } from '../../../storage/user';
import anime from 'animejs'
import GoalsLister from '../_Handlers/GoalsLister.vue';
import TransactionLister from '../_Handlers/TransactionLister.vue';
import {APICall} from '@/utils/apiCall.js'
export default {
    components: {
        GoalsLister, TransactionLister
    },
    data() {
        return({
            user: useUserStorage(),
            transactions: [
                {
                    wallet: "asdfasdfasdf",
                    type: "income",
                    amount: 500,
                    category: null,
                    description: "Sold Malboro Gold to some kid",
                    date: "2025-04-12",
                }, {
                    wallet: "asdfasdfasdf",
                    type: "expense",
                    amount: 1250,
                    category: null,
                    description: "Bought new monitor",
                    date: "2025-04-13",
                }, {
                    wallet: "asdfasdfasdf",
                    type: "income",
                    amount: 4241.99,
                    category: null,
                    description: "Job payout",
                    date: "2025-04-15",
                },
            ],
            goals: [
                {
                    id: 'asdfasdf23r23rfdafas',
                    name: "Holidays 2025",
                    target_amount: 10000,
                    current_amount: 3251.35,
                    deadline: "2025-08-01",
                }
            ]
        })
    },
    mounted() {
        this.$nextTick(()=> {

            APICall('/users/me', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                if (status != 200) {
                    console.log(body);
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Login', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    let bodyData = await body.json()
                    this.user.setUsername(bodyData.username)
                    
                }
            })
            APICall('/transactions/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                if (status != 200) {
                    console.log(body);
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Login', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    let bodyData = await body.json()
                    this.transactions = bodyData
                    
                    this.transactions.sort((a,b)=> {
                        return new Date(b.created_at) - new Date(a.created_at);
                    })
                    this.transactions = this.transactions.slice(0, 3)
                    
                }
            })
            APICall('/goals/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                if (status != 200) {
                    console.log(body);
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Login', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    let bodyData = await body.json()
                    this.goals = bodyData.slice(0, 3)
                }
            })
            this.initTransition()
        })
    },
    methods: {
        initTransition() {

            anime({
                targets: this.$refs['landing-left-panel-1'],
                translateX: ['-8vw', 0],
                opacity: [0,1],
                delay: 150,
                duration: 2000,
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
            })

            anime({
                targets: this.$refs['landing-left-panel-2'],
                translateX: ['-8vw', 0],
                opacity: [0,1],
                delay: 450,
                duration: 2000,
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
            })
            anime({
                targets: this.$refs['welcome-text-panel'],
                marginLeft: ['.9vw', '0']
            })

            anime({
                targets: this.$refs['user-text-panel'],
                marginLeft: ['0vw', '9vw'],
            })
        }
    },
}
</script>
<style scoped>
    .landing-content {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: space-between;
    }
    .left-panel {
        display: flex;
        flex-direction: column;
        gap: .5vw;
        margin: 2vw 0;
    }

    .panel-containment {
        display: flex;
        flex-direction: column;
        gap: .25vw;
    }

    .left-panel .panel-liner {
        font-size: .9vw;
        font-weight: 600;
        margin-bottom: .25vw;

    }

    .right-panel {
        width: 50%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    

    .right-panel .header {
        display: flex;
        flex-direction: column;
    }

    .right-panel .header .h-1 {
        font-size: 2.5vw;
    }

    .right-panel .header .h-2 {
        font-size: 3.5vw;
        font-weight: 600;
        margin-left: 5vw;
    }
</style>