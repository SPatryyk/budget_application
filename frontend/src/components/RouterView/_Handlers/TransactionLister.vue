<template>
    <div class="transaction">
        <div class="col">
            <div class="category">{{ category ? category : 'uncategorized' }}</div>
            <div class="description">{{ description }}</div>
        </div>
        <div class="col">
            <div class="date">{{ date }}</div>
            <div class="amount" :style="{color: type == 'expense' ? 'red' : 'green'}">{{ type == "expense" ? '-' : '+' }} {{ amount.toLocaleString('en-US', {style: 'currency', currency: 'USD' }).replace('$', '').replace(',', ' ') }}PLN</div>
        </div>
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
    },
}
</script>
<style scoped>
    .transaction {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: rgba(0, 0, 0, 0.05);
        box-sizing: border-box;
        padding: 1vw 1.2vw;
        position: relative;
        width: 20vw;
    }

    .transaction .col {
        display: flex;
        flex-direction: column;
        position: relative;
    }

    .transaction .category {
        font-size: .5vw;
        font-weight: 600;
        text-transform: uppercase;
        
    }

    .transaction .description {
        font-size: .7vw;
        font-weight: 500;
    } 

    .transaction .amount {
        font-size: .9vw;
        font-weight: 600;
    }

    .transaction .date {
        margin-left: auto;
        font-size: .5vw;
        opacity: .3;
    }
</style>