<template>
  <div title="Your transactions">
    <va-accordion ref="transactions">
      <va-collapse customHeader>
        <span slot="header">
          <va-card>
            <va-button outline style="width: 98%;">
              Add a cash payment
            </va-button>
          </va-card>
        </span>
        <div slot="body">
          <p class="title">Share this payment with your housemates.</p>
          <div class="flex">
            <span class="va-message-list__message text--secondary"> How much was this payment? </span>
            <va-input
              v-model="cashTransaction.amount"
              placeholder="Amount ($)"
            />
            <span class="va-message-list__message text--secondary"> What was this payment for? </span>
            <va-input
              v-model="cashTransaction.description"
              placeholder="Payment description"
            />
            <span class="va-message-list__message text--secondary"> Who was the payment to? </span>
            <va-input
              v-model="cashTransaction.merchantName"
              placeholder="Company name"
            />
            <span class="va-message-list__message text--secondary"> When was this payment made? </span>
            <va-date-picker
              v-model="cashTransaction.postingDateTime"
              weekDays
            />
            <span class="va-message-list__message text--secondary"> Add any notes about this payment. These will be shared with your group. </span>
            <va-input
              v-model="newTrans.notes"
              placeholder="Add notes (optional)"
            />
            <span class="va-message-list__message text--secondary"> Select rules to apply to this transaction. These will be enforced. </span>
            <va-select
              v-model="newTrans.rules"
              multiple
              :options="rules"
            />
            <span class="va-message-list__message text--secondary"> Add a photo of the purchase or receipt. This will validate the transaction. </span>
            <va-file-upload
              type="gallery"
              file-types=".png, .jpg, .jpeg, .gif"
              dropzone
              v-model="newTrans.photo"
            />
            <br>
            <va-button @click="updateCashTransaction(); quickAddTransaction()">
              Add transaction
            </va-button>
            <va-button outline @click="updateCashTransaction(); doBreakdown()">
              Change breakdown
            </va-button>
          </div>
        </div>
      </va-collapse>
      <va-collapse v-for="t in transactions" :key="t.transactionId" customHeader withBackground>
        <span slot="header">
          <va-list>
            <va-item clickable>
              <va-item-section>
                <va-item-label class="display-5">
                  {{ t.description }}
                </va-item-label>
                <va-item-label caption>
                  {{ 'This was paid to '.concat(t.merchantName,' on ',translateDate(t.postingDateTime),'.') }}
                </va-item-label>
              </va-item-section>
              <va-item-section side class="display-3">
                <va-item-label>
                  {{ '$'.concat(t.amount) }}
                </va-item-label>
              </va-item-section>
            </va-item>
          </va-list>
        </span>
        <div slot="body">
          <p class="title">Share this transaction with your housemates.</p>
          <div class="flex">
            <span class="va-message-list__message text--secondary"> Add any notes about this payment. These will be shared with your group. </span>
            <va-input
              v-model="newTrans.notes"
              placeholder="Add notes (optional)"
            />
            <span class="va-message-list__message text--secondary"> Select rules to apply to this transaction. These will be enforced. </span>
            <va-select
              v-model="newTrans.rules"
              multiple
              :options="rules"
            />
            <span class="va-message-list__message text--secondary"> Add a photo of the purchase or receipt. This will validate the transaction. </span>
            <va-file-upload
              type="gallery"
              file-types=".png, .jpg, .jpeg, .gif"
              dropzone
              v-model="newTrans.photo"
            />
            <br>
            <va-button @click="newTrans.transaction = t; quickAddTransaction(t)">
              Add transaction
            </va-button>
            <va-button outline @click="newTrans.transaction = t; doBreakdown(t)">
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
import BankTransactions from '../../../../../../bankingAPI/getbanktransactions.json'

export default {
  data () {
    return {
      showModal: false,
      transactions: BankTransactions.transactions,
      rules: [],
      users: [],
      breakdown: [],
      cashTransaction: {
        transactionId: '',
        status: 'CASH',
        description: '',
        postingDateTime: new Date().toISOString().slice(0,10),
        amount: '',
        merchantName: '',
        merchantCategoryCode: '0',
      },
      newTrans: {
        transaction: {},
        notes: '',
        rules: [],
        photo: [],
        breakdown: {},
        //   add new transaction info
      },
    }
  },
  computed: {
  },
  methods: {
    pushTransaction () {
      var paidBy = this.$myName
      var disputeStatus = []
      var breakdownSum =  this.breakdown.reduce((a,b)=>parseInt(a)+parseInt(b),0)
      for (var n in this.users) {
        this.newTrans.breakdown[this.users[n]] = this.breakdown[n].concat('/',breakdownSum)
      }
      console.log(this.newTrans.breakdown)

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
        // console.log(resp.data)
        this.showToast(
          "Payment added successfully",
          {
            icon: 'fa-star-o',
            duration: 2500,
          },
        )
      })

      console.log(transaction)
    },
    getRules () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_rules?groupID='+this.$groupID).then(resp => {
        this.rules = resp.data
        // console.log(this.users)
      })
    },
    quickAddTransaction (t) {
      // breakdown = split equally for everybody
      this.pushTransaction()
    },
    updateCashTransaction () {
      this.cashTransaction.transactionId = Math.floor(Math.random() * 100000).toString()
      this.newTrans.transaction = this.cashTransaction
    },
    fullAddTransaction () {
      // fix breakdown
      // this.newTrans.breakdown = this.newTrans.breakdown
      this.pushTransaction()
    },
    doBreakdown (t) {
      this.showModal = true
      // console.log(this.newTrans)
    },
    translateDate (date) {
      const _date = new Date(date)
      return _date.toString().slice(0, 15)
    },
    initBreakdown () {
      if (this.breakdown.size > 0) {
        return
      }
      this.breakdown = []
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_users?groupID='+this.$groupID).then(resp => {
        this.users = resp.data
        for (var user in resp.data) {
          // console.log(resp.data[user])
          this.breakdown[user] = '1'
        }
        // console.log(this.users)
      })
    },
  },
  created () {
    this.initBreakdown()
    this.getRules()
    console.log(this.$refs)
  },
}
</script>

<style lang="scss">
</style>
