<template>
    <div class="goal" :class="{goalPath: isInGoalPath}">
        <div class="row" @click="callbackGo(true, rawData)">
            <div class="col">
                <div class="header">{{ header }}</div>
                <div class="time">{{ countTimeleft() }}</div>
            </div>
            <div class="progress-text">{{ progress }}%</div>
        </div>
        <div class="progress">
            <div class="value" :ref="'progress_value_'+name"></div>
        </div>
        <template v-if="isInGoalPath">
            <div class="trash-goal" @click="callbackRemoveGoal(id)">
                <i class="fas fa-trash"></i>
            </div>
        </template>
    </div>
</template>
<script>
import anime from 'animejs';
export default {
    props: {
        id: String,
        name: String,
        header: String,
        amount: Number,
        targetAmount: Number,
        deadline: String,
        isInGoalPath: Boolean,
        rawData: Object,
        callbackRemoveGoal: Function,
        callbackGo: Function
    }, data() {
        return({
            progress: 0,
        })
    }, 
    mounted() {
        console.log(this.id);
        
        this.animateProgress()
    },
    methods: {
        countTimeleft() {
            const today = new Date();
            const start = new Date(today.toISOString().split('T')[0]);
            const end = new Date(this.deadline);

            let diff = end - start;

            if (diff <= 0) {
                return "Time is up!";
            }

            
            let months = (end.getFullYear() - start.getFullYear()) * 12 + (end.getMonth() - start.getMonth());

            const tempDate = new Date(start);
            tempDate.setMonth(tempDate.getMonth() + months);

            if (tempDate > end) {
            months--;
            tempDate.setMonth(tempDate.getMonth() - 1);
            }

            const msInHour = 1000 * 60 * 60;
            const msInDay = msInHour * 24;

            const daysDiff = Math.floor((end - tempDate) / msInDay);

            tempDate.setDate(tempDate.getDate() + daysDiff);

            const hoursDiff = Math.floor((end - tempDate) / msInHour);

            return "Time left " + (months > 0 ? `${months} months ` : `${daysDiff} days`);
        },
        animateProgress() {
            anime({
                targets: this.$refs['progress_value_'+this.name],
                width: [0, ((this.amount/this.targetAmount)* 100) + '%'],
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                duration: 1000, 
                update: anim=> {
                    this.progress = Math.floor((anim.progress * (this.amount/this.targetAmount)))
                }
            })
        }
    }
}
</script>
<style scoped>
    .goal:hover .trash-goal {width: 3.5vw;}
    .goal .trash-goal {
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
    .goal {
        display: flex;
        background-color: rgba(0, 0, 0, 0.05);
        box-sizing: border-box;
        padding: 1vw 1.2vw;
        position: relative;
        width: 20vw;
    }

    .goal.goalPath {
        width: 25vw;
    }

    .goal .row {
        width: 100%;
        display: flex;
        justify-content: space-between;
    }

    .goal .row .col {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
    }

    .goal .row .col .header {
        font-size: .8vw;
        height: .8vw;
        font-weight: 600;
        text-transform: uppercase;
    }

    .goal .row .col .time {
        font-size: .6vw;
    }

    .goal .progress-text {
        font-size: .95vw;
        font-weight: 700;
        margin: auto 0;
    }

    .goal .progress {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.3);
        height: .3vw;
        overflow: hidden;
    }

    .goal .progress .value {
        height: 100%;
        background-color: rgb(1, 255, 158);
    }
</style>