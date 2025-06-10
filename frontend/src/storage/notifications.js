import { defineStore } from 'pinia'
export const useNotificationStorage = defineStore('notify_storage', {
  state: () => ({
    list: []
  }), actions: {
    add(icon, header, text) {
        let id = 'notify_'+Math.floor(Math.random() * 100)
        this.list.push({
            id: id,
            icon: icon || 'fas fa-envelope',
            header: header || 'Information',
            text: text
        })
        console.log(this.list);
        
        setTimeout(()=> {
            for (const[key, notify] of Object.entries(this.list)) {
                if (notify.id == id) {
                    this.list.splice(key, 1)
                }
            }
        }, 10000)
    }
  }
})