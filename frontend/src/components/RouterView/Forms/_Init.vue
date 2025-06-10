<template>
    <div class="forms-content" :class="{active: base.form.isActive}">
        <div class="close" @click="closeForm">
            <i class="fas fa-times"></i>
        </div>
        <template v-if="base.form.selectedForm == 'transaction'">
            <NewTransaction/>
        </template>
        <template v-if="base.form.selectedForm == 'transfer'">
            <NewTransfer/>
        </template>
        <template v-if="base.form.selectedForm == 'category'">
            <NewCategory/>
        </template>
        <template v-if="base.form.selectedForm == 'goal'">
            <NewGoal/>
        </template>
        <template v-if="base.form.selectedForm == 'wallet'">
            <NewWallet/>
        </template>
        <template v-if="base.form.selectedForm == 'addFunds'">
            <AddFunds/>
        </template>
    </div>
</template>
<script>
import { useBaseStorage } from '../../../storage/base';
import NewTransaction from './NewTransaction.vue';
import NewTransfer from './NewTransfer.vue';
import NewCategory from './NewCategory.vue';
import NewGoal from './NewGoal.vue';
import NewWallet from './NewWallet.vue';
import AddFunds from './AddFunds.vue';
export default {
    components: {
        NewTransaction, NewTransfer, NewCategory, NewGoal, NewWallet, AddFunds
    },
    data() {
        return({
            base: useBaseStorage()
        })
    }, methods: {
        closeForm() {
            this.base.setForm(false)
        }
    }
}
</script>
<style scoped>
    .forms-content {
        width: 40vw;
        height: 100%;
        position: absolute;
        left: -40vw;
        top: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        box-sizing: border-box;
        padding: 5vw;
        background-color: var(--main-element-bg2);
        z-index: 9999;
        transition: left .48s cubic-bezier(0.075, 0.82, 0.165, 1);
    }

    .forms-content.active {
        left: 0;
    }
    .close {
        position: absolute;
        right: 2vw;
        top: 2vw;
        font-size: 1vw;
        opacity: .3;
        transition: opacity .125s ease-in-out;
    }
    .close svg {pointer-events: none;}
    .close:hover {
        opacity: 1;
    }
</style>