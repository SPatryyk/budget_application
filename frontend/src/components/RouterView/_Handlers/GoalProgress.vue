<template>
    <div class="progress-content">
        <div class="svg">
            <svg viewBox="0 0 504 504" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="252" cy="252" r="252" class="progress-background"/>
                <circle cx="252" cy="252" r="252" ref="main_progress" class="progress-val"/>
            </svg>
        </div>
        <div class="text-content">
            <div class="current-amount">{{ currentAmount.toLocaleString('en-US', {style: 'currency', currency: 'USD' }).replace('$', '').replace(',', ' ') }} {{currency}}</div>
            <div class="target-amount">{{ targetAmount.toLocaleString('en-US', {style: 'currency', currency: 'USD' }).replace('$', '').replace(',', ' ') }} {{currency}}</div>
        </div>
    </div>
</template>
<script>
import anime from 'animejs';

export default {
    props: {
        currentAmount: Number,
        targetAmount: Number,
        currency: String,
    }, data() {
        return({
            convertedBalance: 0,
            dashArray: false,
            lastTick: false,
        })
    }, watch: {
        'currentAmount'(newVal) {
            this.animateProgress()
        }
    } ,mounted() {
        this.$nextTick(()=> {
            this.dashArray = document.querySelector('.progress-val').getTotalLength()
            this.$refs['main_progress'].style.strokeDasharray = this.dashArray
            this.$refs['main_progress'].style.strokeDashoffset = this.dashArray
            this.animateProgress()
        })
    }, methods: {
        calculateDashOffset(current, max) {
            let percentage = current/max >= 1.0 ? 1.0 : current/max
            let progress = this.dashArray + (this.dashArray * percentage)
            
            return progress
        },
        animateProgress() {
            anime({
                targets: this.$refs['main_progress'],
                strokeDashoffset: this.calculateDashOffset(this.currentAmount, this.targetAmount),
                strokeDasharray: this.dashArray,
                easing: 'cubicBezier(0.075, 0.82, 0.165, 1)',
                // update: anim=> {
                //     this.convertedBalance = this.currentAmount * (anim.progress / 100)
                // },
            })
        }
    }
}
</script>
<style scoped>
    .progress-content {
        width: 25vw;
        height: 25vw;
        position: relative;
    }
    svg {overflow: visible;}
    .progress-background {
        stroke: rgba(0, 0, 0, 0.05);
        stroke-width: 2vw;
    }

    .progress-val {
        stroke: #76F8CA;
        stroke-width: 2vw;
    }

    .progress-content .svg {
        width: 100%;
        height: 100%;
    }

    .progress-content .text-content {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 1.9vw;
        font-weight: 700;
    }

    .progress-content .text-content .target-amount {
        position: absolute;
        bottom: 5vw;
        font-size: 1.2vw;
        font-weight: 700;

    }
</style>