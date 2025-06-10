import { defineStore } from 'pinia'
export const useBaseStorage = defineStore('base_storage', {
  state: () => ({
    goal: {
      selected: false,
      data: {},
      selectedTransactions: [],
      list: []
    },
    wallets: {
      selected: false,
      list: [],
    },
    categories: {
      list: []
    },
    form: {
      isActive: false,
      selectedForm: ''
    }
  }), actions: {
    setGoalSelected(isSelected, data) {
      this.goal.selected = isSelected
      this.goal.data = data || {}
    },
    setForm(active, form) {
      this.form.isActive = active
      if (form) this.form.selectedForm = form
     },
     setGoals(data) {
      this.goal.list = data
     },
     setWallets(data) {
      this.wallets.list = data
     },
     setCategories(data) {
      this.categories.list = data
     },
     setGoalTransactions(data) {
      this.goal.selectedTransactions = data
      this.goal.selectedTransactions.sort((a, b)=> {
        return new Date(b.created_at) - new Date(a.created_at)
      })
      this.goal.selectedTransactions = this.goal.selectedTransactions.slice(0, 5)
     },

     setSelectedWalletId(data) {
      this.wallets.selected = data
     }
  }
})