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
          title="Total spending per month"
        >
          <va-chart ref="horizontalBarChart" :data="horizontalBarChartData" type="horizontal-bar"/>
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
            backgroundColor: [this.$themes.primary, this.$themes.secondary, this.$themes.danger, this.$themes.warning],
            data: [],
          }],
      },
      horizontalBarChartData: {
        labels: [],
        datasets: [
          {
            label: 'Amount ($)',
            backgroundColor: this.$themes.primary,
            borderColor: 'transparent',
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
      axios.get('http://127.0.0.1:5000/get_stats?groupID='+this.$groupID).then(resp => {

        for (var key in resp.data.result) {
          console.log(resp.data.result[key])
          if (resp.data.result[key] === 0) {
            continue
          }
          this.pieChartData.labels.push(key)
          this.pieChartData.datasets[0].data.push(resp.data.result[key])
          this.$refs.pieChart.$refs.chart.refresh()
        }

        for (var month in resp.data.totalAmount) {
          if (resp.data.totalAmount[month] === 0) {
            continue
          }
          this.horizontalBarChartData.labels.push(month)
          this.horizontalBarChartData.datasets[0].data.push(resp.data.totalAmount[month])
          this.$refs.horizontalBarChart.$refs.chart.refresh()
        }

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
