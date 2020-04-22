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
        <va-button outline :to="{ name: 'add-transactions' }">
          Add a payment
        </va-button>
      </va-list>
      <!-- RULES -->
      <va-list class="display-5" fit>
        <va-list-label>
          My house rules
        </va-list-label>

        <template v-for="(rule,n) in rules">
          <va-item :key="n" clickable>
            <va-item-section>
              <va-item-label>
                {{ rule }}
              </va-item-label>
            </va-item-section>

            <va-item-section side>
              <va-icon name="fa fa-eye" color="gray" />
            </va-item-section>
          </va-item>

          <va-list-separator v-if="n < rules.length - 1" :key="'separator' + n" />
        </template>
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
      rules: [],
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
    getRules () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_rules?groupID='+this.$groupID).then(resp => {
        this.rules = resp.data
      })
    },
  },
  created () {
    this.getTotals()
    this.getRules()
  },
}
</script>

<style lang="scss">
</style>