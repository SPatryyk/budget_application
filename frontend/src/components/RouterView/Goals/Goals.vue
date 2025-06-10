<template>
    <div class="goals-content">
        <transition-group
            @enter="onSwitchEnter"
            @leave="onSwitchLeave"
            :css="false"
        >
            <template v-if="!base.goal.selected">
                <div class="converted-content">
                    <div class="left-panel" ref="goals-left-panel">
                        <div class="element" v-for="goal in base.goal.list">
                                <GoalsLister 
                                    :id="goal.id"
                                    :header="goal.name"
                                    :amount="goal.current_amount"
                                    :deadline="goal.deadline"
                                    :targetAmount="goal.target_amount"
                                    :rawData="goal"
                                    :callbackGo="selectGoal"
                                    :callbackRemoveGoal="removeGoal"
                                    isInGoalPath="true"
                                />
                            </div>
                        <div class="goal-new" @click="addNewGoal">Add new goal</div>
                    </div>
                    <div class="right-panel">
                        <div class="header">
                            <div class="h-1" ref="goals-right-panel-1">Goals</div>
                            <div class="h-2" ref="goals-right-panel-2">Configure and handle your active goals</div>
                        </div>
                    </div>
                </div>
                
            </template>
            <template v-else>
                <div class="converted-content">
                    <div class="left-panel not-centerized" ref="goals-left-panel">
                        <div class="go-back-button" @click="goToGoals">Goals list</div>
                        <div class="new-transaction-button" @click="newTransfer">New transaction</div>
                        <div class="element" v-for="goalTransaction in base.goal.selectedTransactions">
                            <GoalTransaction
                                :type="goalTransaction.type"
                                :amount="goalTransaction.amount"
                                :category="goalTransaction.category"
                                :date="goalTransaction.date"
                                :description="goalTransaction.description"
                            />
                        </div>
                    </div>
                    <div class="right-panel" ref="goals-right-panel-1">
                        <GoalProgress
                            :targetAmount="base.goal.data.target_amount"
                            :currentAmount="base.goal.data.current_amount"
                            :currency="'PLN'"
                        />
                    </div>
                </div>

            </template>
        </transition-group>
        
    </div>
</template>
<script>
import anime from 'animejs';
import { useBaseStorage } from '../../../storage/base';
import { APICall } from '../../../utils/apiCall';
import GoalsLister from '../_Handlers/GoalsLister.vue';
import GoalTransaction from '../_Handlers/GoalTransaction.vue';
import GoalProgress from '../_Handlers/GoalProgress.vue';
export default {
    components: {GoalsLister, GoalProgress, GoalTransaction},
    methods: {
        onSwitchEnter(el, done) {
            anime({
                targets: el,
                translateX: ['100%', '0vw'],
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                complete: done,
            })
        },

        onSwitchLeave(el, done) {
            anime({
                targets: el,
                translateX: ['0vw', '-100%'],
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                complete: done
            })
        },
        addNewGoal() {
            this.base.setForm(true, 'goal')
        },  
        selectGoal(state, goal) {
            APICall('/goals/'+goal.id, 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                if (status != 200) {
                    console.log(body);
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    let bodyData = await body.json()
                    this.base.setGoalSelected(true, bodyData)
                    APICall('/goals/transactions/?goal='+goal.id, 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
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
        },  
        removeGoal(id) {
            console.log(id);
            
            APICall('/goals/'+id+'/', 'DELETE', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                if (status != 204) {
                    console.log(body);
                    
                    let bodyData = await body.json()
                    console.log(bodyData);
                    this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                } else {
                    setTimeout(()=>{
                        
                        APICall('/goals', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
                            if (status != 200) {
                                console.log(body);
                                
                                let bodyData = await body.json()
                                console.log(bodyData);
                                this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
                            } else {
                                let bodyData = await body.json()
                                this.base.setGoals(bodyData)
                            }
                        })
                    }, 100)
                }
            })
        },  
        newTransfer() {
            this.base.setForm(true, 'transaction')
        },
        goToGoals() {
            this.base.setGoalSelected(false)
        }
    },
    data() {
        return({
            base: useBaseStorage(),
            goals: [
                {
                    id: 'asdfasdf23r23rfdafas',
                    name: "Holidays 2025",
                    target_amount: 10000,
                    current_amount: 3251.35,
                    deadline: "2025-08-01",
                }
            ],
            transactions: [],
        })
    }, mounted() {
        if (this.base.goal.selected) {
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
        }
        
        APICall('/goals/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
            if (status != 200) {
                console.log(body);
                
                let bodyData = await body.json()
                console.log(bodyData);
                this.notifications.add('fas fa-exclamation-triangle', 'Goals', bodyData[Object.keys(bodyData)[0]][0])
            } else {
                let bodyData = await body.json()
                console.log(bodyData);
                
                this.base.setGoals(bodyData.slice(0, 10))
            }
        })
        anime({
            targets: this.$refs['goals-right-panel-1'],
            translateX: ['10vw', 0],
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)'
        })
        anime({
            targets: this.$refs['goals-right-panel-2'],
            translateX: ['-8vw', 0],
            duration: 2250,
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)'
        })

        anime({
            targets: this.$refs['goals-left-panel'],
            translateX: ['-8vw', 0],
            delay: 300,
            duration: 1950,
            easing: 'cubicBezier(0.075, 0.82, 0.165, 1)'
        })
    }
}
</script>
<style scoped>
    .converted-content {
        width: calc(100% - 10vw);
        height: calc(100% - 15vw);
        position: absolute;
        left: 5vw;
        top: 10vw;
        display: flex;
        justify-content: space-between;
        overflow: hidden;
    }
    .new-transaction-button {
        width: 25vw;
        box-sizing: border-box;
        padding: .5vw .75vw;
        font-weight: 600;
        text-transform: uppercase;
        font-size: .7vw;
        text-align: center;
        background-color: var(--main-element-bg);
        transform: translateX(0vw);
        transition: transform .48s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .new-transaction-button:hover {
        transform: translateX(2vw);
    }


    .go-back-button {
        width: 9vw;
        box-sizing: border-box;
        padding: .5vw .75vw;
        font-weight: 600;
        text-transform: uppercase;
        font-size: .7vw;
        text-align: center;
        background-color: var(--main-element-bg);
        transform: translateX(0vw);
        margin-bottom: 5vw;
        transition: width .48s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .go-back-button:hover {
        width: 12vw;
    }
    .go-back-button {
        font-size: .7vw;
        font-weight: 600;
    }
    .goals-content {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: space-between;
        overflow: hidden;
    }

    .goals-content .right-panel {
        width: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .goals-content .right-panel .header {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .goals-content .right-panel .header .h-1 {
        font-size: 3vw;
        text-transform: uppercase;
        font-weight: 700;height: 3.3vw;
    }

    .goals-content .right-panel .header .h-2 {
        font-size: .9vw;
        font-weight: 400;
    }

    .goals-content .left-panel {
        width: 50%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        gap: .5vw;
        position: relative;
    }

    .goals-content .left-panel.not-centerized {justify-content: flex-start; }

    .goals-content .left-panel  .goal-new {
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

    .goals-content .left-panel  .goal-new:hover {
        margin-left: 2vw;
    }
</style>