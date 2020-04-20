<template>
  <va-card title="Your transactions">
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
                :options="getRules()"
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
    >
        inside modal {{this.newTrans}}
    </va-modal>
  </va-card>
</template>

<script>
import BankTransactions from '../../../../../../bankingAPI/getbanktransactions.json'

export default {
  data () {
    return {
      showModal: false,
      transactions: BankTransactions.transactions,
      rules: ["Michael always pays 25% of all water bills"],
      newTrans: {
        transaction : [],
        notes: '',
        rules: [],
        photo: [],
        //   add new transaction info
      },
    }
  },
  computed: {
  },
  methods: {
    pushTransaction() {
        console.log(this.newTrans)
    },
    getRules () {
      return this.rules
    },
    quickAddTransaction (t) {
        this.newTrans.transaction = t
        // breakdown = 1/4 for everybody
        this.pushTransaction()
    },
    fullAddTransaction () {
        // fix breakdown
        this.pushTransaction()
    },
    doBreakdown (t) {
        this.newTrans.transaction = t
        this.showModal = true
    },
    translateDate(date) {
        var monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]
        const _date = new Date(date)
        return _date.toString().slice(0,15)
    }
  },
}
</script>

<style lang="scss">
</style>
