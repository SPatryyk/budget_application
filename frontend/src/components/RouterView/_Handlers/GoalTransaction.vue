<template>
    <div class="transcation">
         <div class="col">
            <div class="value">
                <div class="icon" :style="{color: type != 'expense' ? '#12CC34' : 'red'}">{{ type == 'expense' ? '-' : '+' }}</div>
                <div class="text">{{ amount.toLocaleString('en-US', {style: 'currency', currency: 'USD' }).replace('$', '').replace(',', ' ') }}</div>
            </div>
            <div class="description">{{ description }}</div>
         </div>
         <div class="date">{{ date }}</div>
    </div>
</template>
<script>
export default {
    props: {
        type: String,
        amount: Number,
        category: String,
        description: String,
        date: String,
    }
}
</script>
<style scoped>
    .transcation {
        width: 25vw;
        box-sizing: border-box;
        padding: .75vw 1vw;
        padding-left: 2vw;
        display: flex;
        justify-content: space-between;
        background-color: rgba(0, 0, 0, 0.05);
    }

    .transcation .col {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .transcation .value {
        position: relative;
        font-size: .9vw;
        font-weight: 600;
    }

    .transcation .value .icon {
        position: absolute;
        width: 1vw;
        left: -1.2vw;
        color: red;
        display: flex;
        justify-content: center;
        align-items: center;
    }


    .transcation .date {
        font-size: .6vw;
        color: black;
        opacity: .3;
    }
</style>