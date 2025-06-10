<template>
    <div class="input-content">
        <div class="label">{{ label }}</div>
        <div class="text">{{ value }}</div>
    </div>
</template>
<script>
export default {
    props: {
        label: String,
        id: String,
        value: String,
        update: Function,
    },
    methods: {
        handleKeydown(e) {
            const value = e.target.value
            this.update(value)
        }
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
    .label {
        font-size: .9vw;
        font-weight: 600;
    }
    .text {
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