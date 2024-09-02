<template>
  <div class="fixed z-[1000] right-6 bottom-6">
    <div
      class="w-[360px] h-[600px] bg-[white] shadow-[0_0_20px_rgba(0,0,0,0.1)] flex flex-col overflow-hidden rounded-lg container">
      <h1>MyBASF Chat</h1>
      <div
        class="grow overflow-y-auto flex flex-col gap-3 max-h-[400px] overflow-y-auto grow py-0 p-4 border-y-[#f0f0f0] border-t border-solid border-b">
        <template v-for="(message, index) in messages" :key="index">
          <div class="flex mb-2"
            :class="message.from == 'user' ? 'bg-[#1877F2] text-[white] rounded-tl-none' : 'messageFromChatGpt'">
            <div class="flex flex-col" :class="message.from == 'user' ?
              'align-end' :
              'align-start'">
              <div class="max-w-[60%] text-sm leading-[1.4] mb-0.5 px-3 py-2 rounded-[18px];" :class="message.from == 'user' ?
                  'bg-[#1877F2] text-[white] rounded-tl-none' :
                  'bg-[#EDEDED] text-[#222] rounded-tr-none'">
                {{ message.data }}
              </div>
            </div>
          </div>
        </template>
      </div>
      <div class="flex items-center bg-[#f0f0f0] p-2">
        <input v-model="currentMessage" type="text" class="grow text-base bg-[white] mr-2 p-3 rounded-3xl border-[none]"
          placeholder="Ask me anything..." />
        <button @click="sendMessage(currentMessage)"
          class="bg-[#1877F2] text-[white] text-base cursor-pointer transition-[background-color] duration-[0.3s] ease-[ease-in-out] px-4 py-2 rounded-3xl border-[none] hover:bg-[#145CB3]">
          Ask
        </button>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  name: 'ChatBot',
  data() {
    return {
      currentMessage: '',
      messages: [],
    };
  },
  methods: {
    async sendMessage(message) {
      this.messages.push({
        from: 'user',
        data: message,
      });
      // await axios
      //   .post('http://localhost:3000/chatbot', {
      //     message: message,
      //   })
      //   .then((response) => {
      //     this.messages.push({
      //       from: 'chatGpt',
      //       data: response.data.data, // Access the 'data' property of the response object
      //     });
      //   });
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

@media (max-width: 480px) {
  .container {
    @apply w-full max-w-none rounded-none;
  }
}


</style>
