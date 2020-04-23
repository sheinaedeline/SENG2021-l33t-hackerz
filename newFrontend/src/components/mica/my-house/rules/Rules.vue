<template>
  <div>
    <va-list fit class="mb-2">
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
    <va-card title="Add a new rule">
      <div class="flex">
        <va-input
          v-model="newRule"
          placeholder="Enter new rule here"
        >
          <va-button slot="append" style="margin-right: 0;" small @click="addNewRule">
            Submit
          </va-button>
        </va-input>
      </div>
    </va-card>
  </div>
</template>

<script>

export default {
  data () {
    return {
      rules: [],
      newRule: '',
    }
  },
  methods: {
    getRules () {
      const axios = require('axios')
      axios.get('http://127.0.0.1:5000/get_rules?groupID=' + this.$groupID).then(resp => {
        this.rules = resp.data
      })
    },
    addNewRule () {
      const axios = require('axios')
      axios.put('http://127.0.0.1:5000/put_rule', {
        rule: this.newRule,
        groupID: this.$groupID,
      }).then(resp => {
        this.getRules()
        this.newRule = ''
        // console.log(resp)
      })
    },
  },
  created () {
    this.getRules()
  },
}
</script>
