<template>
  <div class="fixed z-[1000] h-[600px] right-6 bottom-6">
    <div
      class="w-[360px] h-full bg-[white] shadow-[0_0_20px_rgba(0,0,0,0.1)] flex flex-col overflow-hidden rounded-lg container">
      <div class="p-4 flex flex-col gap-4 justify-center items-center">
        <div class="flex w-full justify-center items-center p-4 relative">
          <span
            class="absolute left-0"
            v-if="!isInPastChatsMode"
            @click="isInPastChatsMode = true">
            Back
          </span>
          <h1 class="text-xl">MyBASF Chat</h1>
        </div>

        <SimulationSwitch
          v-model="isSimulated"
          @update:modelValue="toggleChatMode">
        </SimulationSwitch>
      </div>
      <div
        class="h-full overflow-y-auto flex flex-col gap-3 overflow-y-auto grow p-4 border-y-[#f0f0f0] border-t border-solid border-b">
        <template v-if="!isInPastChatsMode">
          <TransitionGroup name="slide-fade">
            <ChatMessage
              v-for="message in messages"
              :key="message.id"
              :text="message.text"
              :isUser="message.isUser"
              v-show="message.show">
            </ChatMessage>
          </TransitionGroup> 
        </template>
        <template v-else>
          <ChatList
            :chats=chats
            @select-chat="selectChat">
          </ChatList> 
        </template>

      </div>
      <div class="flex items-center bg-[#f0f0f0] p-2">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          class="grow text-base bg-[white] mr-2 p-3 rounded-3xl border-[none]"
          placeholder="Ask me anything..." />

        <button
          @click="sendMessage"
          class="bg-[#1877F2] text-[white] text-base cursor-pointer transition-[background-color] duration-[0.3s] ease-[ease-in-out] px-4 py-2 rounded-3xl border-[none] hover:bg-[#145CB3]">
          Ask
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import ChatMessage from './ChatMessage.vue';
import SimulationSwitch from './SimulationSwitch.vue';
import ChatList from './ChatList.vue';
import { fakeChats } from '@/mock-data/fakeChats';

export default {
  components: {
    ChatMessage,
    SimulationSwitch,
    ChatList
  },
  setup() {
    const messages = ref([]);
    const newMessage = ref('');

    let messageId = 0;
    const isInPastChatsMode = ref(false);

    // hardcoded for now
    const chats = ref(fakeChats);

    const selectChat = (chat) => {
      console.log("Chat received in selectChat: ", chat);
      isInPastChatsMode.value = false;
      messages.value = chat.messages;
    }

    const addMessage = async(text, isUser) => {
      const message = {
        id: messageId++,
        text,
        isUser,
        show: false
      }
      messages.value.push(message);

      setTimeout(() => {
        messages.value[messages.value.length - 1].show = true;
      }, 100);
    };

    const sendMessage = () => {
      if (newMessage.value.trim()) {
        addMessage(newMessage.value, true);
        newMessage.value = "";

        setTimeout(() => {
          addMessage("Hi this is a Chatbot response!", false);
        }, 100)
      }
    };

    const checkHealth = async() => {
      try {
        const response = await axios.get('http://localhost:5000/api/health');
        console.log("Helath check response: ", response.data.status);
      } catch (error) {
        console.error("Error checking health: ", error);
      }
    }
    checkHealth();

    return {
      isInPastChatsMode,
      chats,
      messages,
      newMessage,
      sendMessage,
      selectChat
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

@media (max-width: 480px) {
  .container {
    @apply w-full max-w-none rounded-none;
  }
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}


</style>
