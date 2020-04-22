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
      months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      pieChartData: {
        labels: [],
        datasets: [
          {
            backgroundColor: [this.$themes.primary, '#CDA6FB', this.$themes.danger, '#FFAA6F', '#2432ff', this.$themes.secondary, '#19fbff', '#f0f71e'],
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
      axios.get('http://127.0.0.1:5000/get_stats?groupID=' + this.$groupID).then(resp => {
        for (var key in resp.data.result) {
          console.log(resp.data.result[key])
          console.log(key)
          if (resp.data.result[key] === 0) {
            continue
          }
          this.pieChartData.labels.push(key)
          this.pieChartData.datasets[0].data.push(resp.data.result[key])
          this.$refs.pieChart.$refs.chart.refresh()
        }

        for (var i = 0; i < resp.data.totalAmount.length; i++) {
          if( resp.data.totalAmount[i] == 0) {
            continue
          }
          this.horizontalBarChartData.labels.push(this.months[i])
          console.log(i + resp.data.totalAmount[i])
          this.horizontalBarChartData.datasets[0].data.push(resp.data.totalAmount[i])
          this.$refs.horizontalBarChart.$refs.chart.refresh()
        }

        console.log('test')
        console.log(this.horizontalBarChartData.datasets[0])
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
