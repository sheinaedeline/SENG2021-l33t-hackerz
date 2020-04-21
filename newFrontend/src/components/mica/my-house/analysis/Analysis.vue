<template>
  <div class="charts">
    <div class="row">
      <div class="flex md6 xs12">
        <va-card
          class="chart-widget"
          title="Household spending breakdown"
        >
          <va-chart ref="pieChart" :data="pieChartData" type="pie"/>
        </va-card>
      </div>
      <div class="flex md6 xs12">
        <va-card
          class="chart-widget"
          title="Household spending breakdown"
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
      pieChartData: {
        labels: [],
        datasets: [
          {
            backgroundColor: [this.$themes.primary, this.$themes.secondary, this.$themes.danger],
            data: [],
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
        for (var key in resp.data) {
          if (resp.data[key] == '0') {
              continue
          }
          this.pieChartData.labels.push(key)
          this.pieChartData.datasets[0].data.push(resp.data[key])
          this.$refs.pieChart.$refs.chart.refresh()
        }

        console.log(this.pieChartData)
      })
    },
  },
  created () {
      this.getData()
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
