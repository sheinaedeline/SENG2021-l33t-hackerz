<template>
  <div title="My House shared transactions">
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
    <br><br>
    <va-accordion>
      <va-collapse v-for="t in transactions" :key="t.transactionId" customHeader withBackground>
        <span slot="header">
          <va-list>
            <va-item clickable>
              <va-item-section>
                <va-item-label class="display-5">
                  {{ t.description }}
                </va-item-label>
                <va-item-label caption>
                  {{ t.paidBy.concat(' paid $',t.amount,' to ',t.merchantName,' on ',translateDate(t.postingDateTime),'.') }}
                </va-item-label>
              </va-item-section>
              <va-item-section side class="display-3">
                <va-item-label>
                  {{ '$'.concat((t.amount*(t.breakdown[$myName].split("/")[0]/t.breakdown[$myName].split("/")[1])).toFixed(2)) }}
                </va-item-label>
              </va-item-section>
            </va-item>
          </va-list>
        </span>
        <div slot="body">
          <div class="flex">
          <va-button outline @click="doRules()">
            Dispute this payment
          </va-button>
          <va-modal
            v-model="showModal1"
            title="Choose rule"
            okText="Add rule"
            @ok="getRules()"
            size="small"
          >
          Pick which rules you want to dispute.
          <div class = "row">
            <div class="row">
            <va-select
              v-model="newTrans.rules"
              multiple
              :options="rules"
            />
            </div>
          </div>
        </va-modal>
        <va-button outline>
          Add note
        </va-button>
            <va-button outline @click="doBreakdown(t)">
              Change breakdown
            </va-button>
          </div>
        </div>
      </va-collapse>
    </va-accordion>
    <va-modal
      v-model="showModal"
      title="Split payment"
      okText="Add payment"
      @ok="fullAddTransaction()"
      size="small"
    >
      Update the breakdown of the payment here. Label how many parts each house member should pay, and the payment will be split accordingly.
      <div class="row md6 offset--md3">
        <div v-for="user in users" :key="user" class="my-4 px-3">
          <va-input
            v-model="breakdown[user]"
            :label="user"
          >
            <va-icon
              slot="prepend"
              color="gray"
              name="fa fa-user"
            />
          </va-input>
        </div>
      </div>

    </va-modal>
  </div>
</template>

<script>

// new version
export default {
  data () {
    return {
      showModal: false,
      showModal1: false,
      totals: [],
      transactions: [],
      rules: [],
      users: [],
      breakdown: [],
      newTrans: {
        transaction: [],
        notes: '',
        rules: [],
        photo: [],
        breakdown: [],
        //   add new transaction info
      },
    }
  },
  computed: {
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
    getSharedTrans () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_shared_trans?groupID='+this.$groupID).then(resp => {
        this.transactions = resp.data
        console.log(resp.data)
      })
    },
    getTotals () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_total?groupID='+this.$groupID).then(resp => {
        this.totals = resp.data
        console.log(resp.data)
      })
    },
    pushTransaction () {
      console.log(this.breakdown)
      var paidBy = this.$myName
      var disputeStatus = []
      var transaction = {
        transactionID: this.newTrans.transaction.transactionId,
        paidBy: paidBy,
        description: this.newTrans.transaction.description,
        postingDateTime: this.newTrans.transaction.postingDateTime,
        amount: this.newTrans.transaction.amount,
        merchantName: this.newTrans.transaction.merchantName,
        merchantCatergoryCode: this.newTrans.transaction.merchantCategoryCode,
        breakdown: this.newTrans.breakdown,
        disputeStatus: disputeStatus,
        notes: this.newTrans.notes,
      }
      const axios = require('axios')
      axios.put('http://127.0.0.1:5000/put_trans', {
        transaction: transaction,
        groupID: this.$groupID,
      }).then(resp => {
        console.log(resp.data)
      })

      console.log(transaction)
    },
    doRules () {
      this.showModal1 = true
    },
    getRules () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_rules?groupID='+this.$groupID).then(resp => {
        this.rules = resp.data
        console.log(this.users)
        console.log(this.rules)
      })
    },
    quickAddTransaction (t) {
      this.newTrans.transaction = t
      // breakdown = split equally for everybody
      this.pushTransaction()
    },
    fullAddTransaction () {
      // fix breakdown
      this.newTrans.breakdown = this.breakdown
      this.pushTransaction()
    },
    doBreakdown (t) {
      this.newTrans.transaction = t
      this.showModal = true
    },
    translateDate (date) {
      const _date = new Date(date)
      return _date.toString().slice(0, 15)
    },
    initBreakdown () {
      if (this.newTrans.breakdown.size > 0) {
        return
      }
      this.newTrans.breakdown = []
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_users?groupID='+this.$groupID).then(resp => {
        this.users = resp.data
        for (var user in resp.data) {
          console.log(resp.data[user])
          this.newTrans.breakdown[resp.data[user]] = '1'
        }
        console.log(this.users)
      })
    },
  },
  created () {
    this.initBreakdown()
    this.getRules()
    this.getTotals()
    this.getSharedTrans()
  },
}
</script>

<style lang="scss">
</style>
