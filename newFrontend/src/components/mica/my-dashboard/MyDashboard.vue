<template>
  <div>
    <div class="row">
      <div class="flex align--start xs6">
        <va-list class="display-3">
          <va-list-label>
            House Balances
          </va-list-label>
          <br><br>
          <va-item v-for="(owing,name) in totals[$myName]" :key="name.concat('Owing')" clickable>
            <va-item-section>
              <va-item-label>
                {{parseOwingString(owing,name)}}
              </va-item-label>
            </va-item-section>
            <br>
          </va-item>
          <br>
          <div class="justify--center">
            <va-button flat :to="{ name: 'add-transactions' }">
              Add a payment
            </va-button>
          <!-- <br> -->
          </div>
          <br>
        </va-list>
        <br><br>
      </div>
      <div class="flex xs6">
        <!-- INFOBLOCKS-->
        <div
          class="flex"
          v-for="(info, idx) in infoTiles"
          :key="idx"
        >
          <va-card class="" :color="info.color">
            <p class="display-2 mb-0" style="color: white;">{{ info.value }}</p>
            <p>{{$t(info.text)}}</p>
          </va-card>
        </div>
      </div>
    </div>
    <br/><br/>
    <div class="row">
      <!-- PIEGRAPH -->
      <div class="va-card flex align--start xs6">
        <va-chart ref="pieChart" :data="pieChartData" type="pie"/>
      </div>
      <!-- RULES -->
      <div class="flex xs6 align--start">
        <va-list class="display-7" fit>
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
        text: 'shared payments',
        icon: '',
      }, {
        color: 'danger',
        value: '$204.36',
        text: 'spent this month',
        icon: '',
      }, {
        color: 'info',
        value: 'Four',
        text: 'housemates',
        icon: '',
      }],
      totals: [],
      users: [],
      rules: [],
      pieChartData: {
        labels: [],
        datasets: [
          {
            backgroundColor: [this.$themes.primary, this.$themes.secondary, this.$themes.danger, '#FFAA6F', '#2432ff', '#CDA6FB', '#19fbff', '#f0f71e'],
            data: [],
          }],
      },
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
      axios.get('http://127.0.0.1:5000/get_total?groupID=' + this.$groupID).then(resp => {
        this.totals = resp.data
        console.log(resp.data)
      })
    },
    getRules () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_rules?groupID=' + this.$groupID).then(resp => {
        this.rules = resp.data
      })
    },
    getData () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_stats?groupID=' + this.$groupID).then(resp => {
        for (var key in resp.data.result) {
          if (resp.data.result[key] === 0) {
            continue
          }
          this.pieChartData.labels.push(key)
          this.pieChartData.datasets[0].data.push(resp.data.result[key])
          this.$refs.pieChart.$refs.chart.refresh()
        }
      })
    },
  },
  created () {
    this.getTotals()
    this.getRules()
    this.getData()
  },
}
</script>

<style lang="scss">
</style>
