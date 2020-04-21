<template>
  <div title="Your transactions">
    <va-accordion>
      <va-collapse customHeader>
        <span slot="header">
          <va-card>
            <va-button outline style="width: 90%;">
              Add a cash transaction
            </va-button>
          </va-card>
        </span>
        <div slot="body">
          <p class="title">Share this transaction with your housemates.</p>
          <div class="flex">
            <span class="va-message-list__message text--secondary"> What was this payment for? </span>
            <va-input
              v-model="newTrans.name"
              placeholder="Name payment"
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
            <va-button @click="quickAddTransaction()">
              Add transaction
            </va-button>
            <va-button outline @click="doBreakdown()">
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
            <va-button @click="quickAddTransaction(t)">
              Add transaction
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
      okText="Add transaction"
      @ok="fullAddTransaction()"
      size="small"
    >
      inside modal {{this.newTrans}}
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
      newTrans: {
        name: '',
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
    pushTransaction () {
      // console.log(this.breakdown)
      var paidBy = 'Michael'
      var disputeStatus = []
      var transaction = {
        transactionID: this.newTrans.transaction.transactionId,
        paidBy: paidBy,
        description: this.newTrans.transaction.description,
        postingDateTime: this.newTrans.transaction.postingDateTime,
        amount: this.newTrans.transaction.amount,
        merchantName: this.newTrans.transaction.merchantName,
        merchantCategoryCode: this.newTrans.transaction.merchantCategoryCode,
        breakdown: this.newTrans.breakdown,
        disputeStatus: disputeStatus,
        notes: this.newTrans.notes,
      }
      var groupID = '2'
      const axios = require('axios')
      axios.put('http://127.0.0.1:5000/put_trans', {
        transaction: transaction,
        groupID: groupID,
      }).then(resp => {
        // console.log(resp.data)
      })

      // console.log(transaction)
    },
    getRules () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_rules?groupID=1').then(resp => {
        this.rules = resp.data
        // console.log(this.users)
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
      axios.get('http://127.0.0.1:5000/get_users?groupID=1').then(resp => {
        this.users = resp.data
        for (var user in resp.data) {
          // console.log(resp.data[user])
          this.newTrans.breakdown[resp.data[user]] = '1'
        }
        // console.log(this.users)
      })
    },
  },
  created () {
    this.initBreakdown()
    this.getRules()
  },
}
</script>

<style lang="scss">
</style>
