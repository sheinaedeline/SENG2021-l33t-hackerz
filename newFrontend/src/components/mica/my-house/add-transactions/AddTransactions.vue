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
                  {{ 'This was paid to '.concat(t.merchantName,' on ',t.postingDateTime,'.') }}
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
          <p class="display-5">Share transaction with your house </p>
          <br>
          <div class="flex">
            <va-input
              v-model="newTrans.notes"
              placeholder="Add notes (optional)"
              :messages="messages"
            />
            <va-button @click="addTransaction">
              Add transaction
            </va-button>
          </div>
        </div>
      </va-collapse>
    </va-accordion>
  </va-card>
</template>

<script>
import BankTransactions from '../../../../../../bankingAPI/getbanktransactions.json'

export default {
  data () {
    return {
      transactions: BankTransactions.transactions,
      messages: ['Add any notes about this payment. ' + 'These will be shared with your group.'],
      newTrans: {
        notes: '',
        //   add new transaction info
      },
    }
  },
  methods: {
    edit (user) {
      alert('Edit User: ' + JSON.stringify(user))
    },
    addTransaction () {
      console.log(this.newTrans)
    //   add transaction using api here
    },
  },
}
</script>

<style lang="scss">
</style>
