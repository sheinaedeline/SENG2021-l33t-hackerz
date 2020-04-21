<template>
  <div class="charts">
    <div class="row">
      <div class="flex md6 xs12">
        <va-card
          class="chart-widget"
          :title="$t('charts.pieChart')"
        >
          <va-chart :data="pieChartData" type="pie"/>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      categories: [],
      dataInput: [],
      pieChartData: {
        labels: this.categories,
        datasets: [
          {
            label: 'Label1',
            backgroundColor: [this.$themes.primary, this.$themes.warning, this.$themes.danger],
            data: this.$dataInput,
          }],
      },
    }
  },
  computed: {
  },
  methods: {
    getData () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_stats?groupID=1').then(resp => {
        for (var key in resp.result) {
          this.categories.push(key)
          this.dataInput.push(resp.result[key])
        }
      })
    },
  },
}
</script>

<style lang="scss">
.chart-widget {
  .va-card__body {
    height: 550px;
  }
}
</style>
