<template>
  <div class="chat">
    <div class="row">
      <div class="flex xs12 md12">
        <va-card title="Noticeboard">
          <chat v-model="chatMessages"/>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>
import Chat from '../../../ui/chat/Chat'

export default {
  name: 'chat-page',
  components: { Chat },
  data () {
    return {
      chatMessages: [
        {
          text: 'Hello! Will you be home this weekend? I\'m thinking of throwing a party.',
          yours: false,
        },
        {
          text: 'Yeah, that would be cool. Maybe this Sunday at 3 pm?',
          yours: true,
        },
        {
          text: 'Keen! See you later!',
          yours: false,
        },
        {
          text: 'Just chucked the water bill on Mica. It\'s a bit more than usual could you please be careful.',
          yours: false,
        },
        {
          text: 'Sure',
          yours: true,
        },
        {
          text: 'Do you know where the TV remote is?',
          yours: false,
        },
        {
          text: 'Try under the sofa. 😂 lol',
          yours: true,
        },
        {
          text: 'Could you please buy milk while you\'re out? Finished it this morning',
          yours: false,
        },
      ],
    }
  },
}
</script>

<style lang='scss'>

</style>
