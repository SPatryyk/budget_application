<template>
  <Notifications/>
  <RouterView />
</template>
<script>
import { RouterView } from 'vue-router'
import {useBaseStorage} from '@/storage/base'
import Notifications from './components/Notifications.vue'
import { useNotificationStorage } from './storage/notifications'
import { APICall } from './utils/apiCall'
export default {
  components: {Notifications},
  data() {
    return({
      base: useBaseStorage(),
      notifications: useNotificationStorage()
    })
  },
  mounted() {
    APICall('/wallets/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
            if (status != 200) {
            } else {
                let bodyData = await body.json()
                this.base.setWallets(bodyData.slice(0, 8))
            }
        })
        APICall('/goals/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
            if (status != 200) {
            } else {
                let bodyData = await body.json()
                this.base.setGoals(bodyData.slice(0, 8))
            }
        })
        APICall('/transactions/categories/', 'GET', {'Authorization': 'Bearer '+localStorage.getItem('access')}, false, async (status, body)=> {
            if (status != 200) {
                //this.notifications.add('fas fa-exclamation-triangle', 'Wallets', bodyData[Object.keys(bodyData)[0]][0])
            } else {
                let bodyData = await body.json()
                this.base.setCategories(bodyData)
            }
        })
  },  
  created() {
    this.$nextTick(()=> {
      if (!localStorage.getItem('access')) {
        this.$router.push('/login')
      } else {
        this.$router.push('/landing')
        
      }
    })
  },
  updated() {
    
  },
  methods: {

  }
}
</script>