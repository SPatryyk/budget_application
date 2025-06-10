<template>
    <div class="input-content">
        <div class="label">{{ label }}</div>
        <div class="select">
            
            <template v-if="label == 'Wallet'">
                <div class="selected" @click="switchActive">{{ selected.name || '' }} [{{ selected.balance }} {{ selected.currency }}]</div>
            </template>
            <template v-else>
                <div class="selected" @click="switchActive">{{ selected.name || '' }}</div>
            </template>
            <div class="list" :class="{active: isActive}">
                <template v-if="label == 'Wallet'">
                    <div class="list-element" v-for="element in list" @click="handleUpdate(element)" :key="element.id">{{ element.name }} <span>[{{ element.balance }} {{ element.currency }}]</span></div>
                </template>
                <template v-else>
                    <div class="list-element" v-for="element in list" @click="handleUpdate(element)" :key="element.id">{{ element.name }}</div>
                </template>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        label: String,
        id: String,
        selected: String,
        list: Array,
        update: Function,
    },
    methods: {
        switchActive() {
            this.isActive = !this.isActive
        },
        handleUpdate(id) {
            this.isActive = false
            this.update(id)
        }
    }, data() {
        return({
            isActive: false
        })
    }
}
</script>
<style scoped>
    .input-content {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .select {
        font-size: .9vw;
        font-weight: 500;
        background: var(--main-element-bg);
        box-sizing: border-box;
        padding: .4vw;
        width: 100%;
        margin-bottom: .5vw;
    }

    .selected {
        font-size: .8vw;
        font-weight: 500;
        padding-left: .5vw;
    }

    .list {
        display: flex;
        flex-direction: column;
        padding-left: 1vw;
        padding-top: 0vw;
        font-size: .7vw;
        font-weight: 500;
        max-height: 0;
        opacity: 0;
        overflow: hidden;
        transition: all .48s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .list.active { max-height: 10vw; opacity: 1; padding-top: .5vw;}

    .list .list-element {
        opacity: .3;
        transition: opacity .125s ease-in-out;
    }

    .list .list-element.active, .list .list-element:hover {opacity: 1;}

    .label {
        font-size: .9vw;
        font-weight: 600;
    }
    input {
        width: 100%;
        background-color: var(--main-element-bg);
        border: 0;
        outline: 0;
        font-family: 'Montserrat', sans-serif;
        box-sizing: border-box;
        padding: .5vw .75vw;
        font-size: .75vw;
        margin-bottom: .5vw;
    }
</style>