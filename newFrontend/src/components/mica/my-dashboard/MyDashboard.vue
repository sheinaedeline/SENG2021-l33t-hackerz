<template>
  <div>
    <div class="row">
      <div class="dashboard flex md4">
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
      </div>
      <div class="va-card flex offset--md2 md6">
        <!-- INFOBLOCKS-->
        <div
          class="flex offset--md4 md4"
          v-for="(info, idx) in infoTiles"
          :key="idx"
        >
          <va-card class="mb-0" :color="info.color">
            <p class="display-2 mb-0" style="color: white;">{{ info.value }}</p>
            <p>{{$t(info.text)}}</p>
          </va-card>
        </div>
      </div>
    </div>
    <br/><br/>
      <!-- RULES -->
  <div class="row">
    <div class="dashboard flex md4">
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
    <!-- PIEGRAPH -->
    <div class="va-card flex offset--md2 md6">

    </div>
  </div>
</div>
</div>
</template>

<script>

export default {
  name: 'my-dashboard',
  data () {
    return {
    infoTiles: [{
      color: 'success',
      value: '29',
      text: 'Shared transactions',
      icon: '',
    }, {
      color: 'danger',
      value: '$204.36',
      text: 'Personal contributions',
      icon: '',
    }, {
      color: 'info',
      value: '4',
      text: 'Housemates',
      icon: '',
    }],
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
