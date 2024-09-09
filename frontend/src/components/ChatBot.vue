<template>
  <div class="fixed z-[1000] h-[600px] right-6 bottom-6">
    <div
      class="w-[360px] h-full bg-[white] shadow-[0_0_20px_rgba(0,0,0,0.1)] flex flex-col overflow-hidden rounded-lg container">
      <div class="p-4 flex flex-col gap-4 justify-center items-center">
        <div class="flex w-full justify-center items-center relative">
          <BackButton
            class="absolute left-0"
            v-if="!isInPastChatsMode"
            @click="isInPastChatsMode = true">
          </BackButton>
          <h1 class="text-xl">myOrderManagement</h1>
        </div>

        <!-- <SimulationSwitch
          v-model="isSimulated"
          @update:modelValue="toggleChatMode">
        </SimulationSwitch> -->
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

            <LoadingIcon v-if="isLoading"></LoadingIcon>
          </TransitionGroup> 

          <SuggestionsList
            v-if="messages.length === 1"
            :suggestions="visibleSuggestions"
            @suggestionClick="handleSuggestionClick"
          />
        </template>
        <template v-else>
          <ChatList
            :chats=chats
            @select-chat="selectChat">
          </ChatList> 
        </template>

      </div>
      <div class="flex items-center justify-center bg-[#f0f0f0] p-2">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          class="grow text-base bg-[white] mr-2 p-3 rounded-3xl border-[none]"
          placeholder="Ask me anything..."
          v-if="!isInPastChatsMode"/>

        <button
          @click="sendMessage"
          class="bg-[#1877F2] text-[white] text-base cursor-pointer transition-[background-color] duration-[0.3s] ease-[ease-in-out] px-4 py-2 rounded-3xl border-[none] hover:bg-[#145CB3]"
          v-if="!isInPastChatsMode">
          Ask
        </button>
        <button
          v-else
          @click="startNewChat"
          class="bg-[#1877F2] text-[white] text-base cursor-pointer transition-[background-color] duration-[0.3s] ease-[ease-in-out] px-4 py-2 rounded-3xl border-[none] hover:bg-[#145CB3]">
          New Chat
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ChatMessage from './ChatMessage.vue';
// import SimulationSwitch from './SimulationSwitch.vue';
import ChatList from './ChatList.vue';
import SuggestionsList from './SuggestionList.vue'
import LoadingIcon from './icons/LoadingIcon.vue';
import BackButton from './icons/BackButton.vue';

export default {
  components: {
    ChatMessage,
    // SimulationSwitch,
    ChatList,
    SuggestionsList,
    LoadingIcon,
    BackButton
  },
  setup() {
    const messages = ref([]);
    const newMessage = ref('');
    let messageId = 0;
    const isInPastChatsMode = ref(false);
    const chats = ref([]);
    const chatIndex = ref(1);
    const currentChat = ref(null);

    const isLoading = ref(false);

    const allSuggestions = ref([
      'Get order on latest status',
      'Provide table of orders'
    ])
    const visibleSuggestions = ref([]);

    const addMessage = async(text, isUser) => {
      const message = {
        id: messageId++,
        text,
        isUser,
        show: false,
      }
      messages.value.push(message);

      if (currentChat.value) {
        currentChat.value.messages.push(message);
      }

      setTimeout(() => {
        messages.value = messages.value.map(msg => 
          msg.id === message.id ? {...msg, show: true} : msg
        );
      }, 100);
    };

    const graduallyLoadSuggestions = () => {
      allSuggestions.value.forEach((suggestion, index) => {
        setTimeout(() => {
          visibleSuggestions.value.push(suggestion);
        }, index * 500);
      });
    }

    const handleSuggestionClick = async (suggestion, index) => {
      console.log("Suggestion: ", suggestion);
      setTimeout(() => {
        visibleSuggestions.value.pop();
      }, index * 500);

      newMessage.value = suggestion;
      sendMessage();

      isLoading.value = true;
    }

    const sendMessage = () => {
      if (newMessage.value.trim()) {
        addMessage(newMessage.value, true);

        // If this is the first user message, add the chat to the chats list
        if (currentChat.value && currentChat.value.messages.length === 2) {
          currentChat.value.date = new Date().toISOString();
          currentChat.value.title = generateChatTitle(newMessage.value);
          chats.value.push(currentChat.value);
          chatIndex.value++;
          saveChats();
        }

        newMessage.value = "";
        isLoading.value = true;
        // API call and waiting goes here
        setTimeout(() => {
          isLoading.value = false;
          addMessage("Hi this is a Chatbot response!", false);
        }, 500)
      }
    };

    const generateChatTitle = (message) => {
      const maxLength = 30; // truncate if too long
      let title = message.trim().split(' ').slice(0, 5).join(' ');
      if (title.length > maxLength) {
        title = title.substring(0, maxLength) + "...";
      }
      return title;
    }

    const selectChat = (chat) => {
      isInPastChatsMode.value = false;
      messages.value = chat.messages.map((msg, index) => ({
        ...msg,
        id: index,
        show: true
      }));

      visibleSuggestions.value = [];
    }

    const startNewChat = () => {
      currentChat.value = {
        id: chatIndex.value,
        messages: []
      };

      isInPastChatsMode.value = false;
      messages.value = [];
      visibleSuggestions.value = [];
      addMessage("Hi! Welcome to myOrderManagement. How may I be of help?", false);
      graduallyLoadSuggestions();
    }

    // simulating chats
    const saveChats = () => {
      const chatsToSave = chats.value.filter(chat => chat.messages.length > 1)
      localStorage.setItem('chats', JSON.stringify(chatsToSave));
    };

    const loadChats = () => {
      const savedChats = localStorage.getItem('chats');
      if (savedChats) {
        chats.value = JSON.parse(savedChats);

        chats.value = chats.value.map((chat, index) => ({
          ...chat,
          id: chat.id || Date.now() + index
        }))
      }
    };

    const loadNewestChat = () => {
      if (JSON.parse(chats).length > 0) {
        const newestChat = chats.value[chats.value - 1];
        messages.value = newestChat.messages.map((msg, index) => ({
          ...msg,
          id: index,
          show: true
        }));
        return true;
      }
      return false;
    }

    // checking API status
    const checkHealth = async() => {
      try {
        const response = await axios.get('http://localhost:5000/api/health');
        console.log("Helath check response: ", response.data.status);
      } catch (error) {
        console.error("Error checking health: ", error);
      }
    }
    checkHealth();

    onMounted(() => {
      loadChats();
      if (chats.value.length === 0) {
        startNewChat();
      } else {
        // Load the most recent chat
        const lastChat = chats.value[chats.value.length - 1];
        messages.value = lastChat.messages.map((msg, index) => ({
          ...msg,
          id: index,
          show: true
        }));
      }
    })

    return {
      visibleSuggestions,
      graduallyLoadSuggestions,
      isInPastChatsMode,
      chats,
      messages,
      newMessage,
      sendMessage,
      selectChat,
      startNewChat,
      saveChats,
      loadNewestChat,
      handleSuggestionClick,
      isLoading,
      currentChat
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
