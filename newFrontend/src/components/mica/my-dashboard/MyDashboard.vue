<template>
  <div class="dashboard">
    <div class="row">
      <va-list class="display-5" fit>
        <va-list-label>
          Balances
        </va-list-label>
        <va-item v-for="(owing,name) in totals[$myName]" :key="name.concat('Owing')" clickable>
          <va-item-section>
            <va-item-label>
              {{parseOwingString(owing,name)}}
            </va-item-label>
          </va-item-section>
          <br><br>
        </va-item>
        <va-button outline style="width: 98%;" :to="{ name: 'add-transactions' }">
          Add a payment
        </va-button>
      </va-list>
    </div>
  </div>
</template>

<script>

export default {
  name: 'my-dashboard',
  data () {
    return {
      totals: [],
      users: [],
    }
  },
  methods: {
    parseOwingString (owing, name) {
      if (owing < 0) {
        return name.concat(' owes you $', -owing, '.')
      }
      if (owing > 0) {
        return 'You owe '.concat(name, ' $', owing, '.')
      }
    },
    getTotals () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_total?groupID='+this.$groupID).then(resp => {
        this.totals = resp.data
        console.log(resp.data)
      })
    },
  },
  created () {
    this.getTotals()
  },
}
</script>

<style lang="scss">
</style>