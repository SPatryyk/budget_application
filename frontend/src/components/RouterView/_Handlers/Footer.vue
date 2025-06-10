<template>
    <div class="footer-content">
        <div class="left-panel">
            <div class="header">Home Budget</div>
            <div class="description">This app was made just for educational purposes. Any distribute, edit, modification is herebly prohibited.</div>
        </div>
        <div class="panel">
            <div class="header">Developers</div>
            <div class="text-box">
                <div class="text">Frontend</div>
                <div class="value">--</div>
            </div>
            <div class="text-box">
                <div class="text">Backend</div>
                <div class="value">--</div>
            </div>
        </div>
        <div class="right-panel">
            <div class="element" @click="newCategory">New Category</div>
        </div>
    </div>
</template>
<script>
import { useBaseStorage } from '../../../storage/base';

export default {
    data() {
        return({
            base: useBaseStorage()
        })
    }, methods: {
        newCategory() {
            this.base.setForm(true, 'category')
        }
    }
}
</script>
<style scoped>
    .footer-content {
        position: absolute;
        z-index: 999999999999999999999999999;
        width: 100%;
        left: 0;
        bottom: 0;
        display: flex;
        gap: 1vw;
        background-color: black;
        box-sizing: border-box;
        padding: 1vw 1.25vw;
        color: white;
    }

    .footer-content .left-panel {
        display: flex; 
        flex-direction: column;
        width: 15vw;
    }

    .left-panel .header {
        font-size: .7vw;
        text-transform: uppercase;
        font-weight: 600;
    }

    .panel {
        display: flex;
        flex-direction: column;
    }

    .panel .header {
        font-size: .6vw;
        font-weight: 600;
        text-transform: uppercase;
    }

    .panel .text-box {
        display: flex;
        text-transform: uppercase;
        font-size: .5vw;
    }

    .text-box .text {opacity: .3; width: 3.2vw;}
    .text-box .value {font-weight: 500;}

    .left-panel .description {
        opacity: .3;
        font-size: .5vw;
    }

    .right-panel {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: center;
        margin-left: auto;
    }

    .right-panel .element {
        font-size: .6vw;
        text-transform: uppercase;
        font-weight: 600;
    }
</style>