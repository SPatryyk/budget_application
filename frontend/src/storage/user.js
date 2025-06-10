import { defineStore } from 'pinia'
export const useUserStorage = defineStore('user_storage', {
  state: () => ({
    username: 'MarkSmith_01',
  }), actions: {
    setUsername(username) {
        this.username = username
    }
  }
})