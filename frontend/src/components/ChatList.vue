<template>
  <div class="flex flex-col h-full">
    <h2 class="text-lg font-semibold mb-4">Past Chats</h2>
    <div class="overflow-y-auto flex-grow">
      <div
        v-for="chat in chats"
        :key="chat.id"
        @click="handleClick(chat)"
        class="p-3 hover:bg-gray-100 cursor-pointer rounded-md mb-2">
          <div class="font-medium">{{ chat.title }}</div>
          <div class="text-sm text-gray-500">{{ formatDate(chat.date) }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['chats'],
  emits: ['select-chat'],
  setup(props, { emit }) {
    const handleClick = (chat) => {
      console.log("Chat clicked in ChatList: ", chat);
      emit('select-chat', chat);
    };

    const formatDate = (date) => {
      return new Date(date).toLocaleString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    };

    return {
      formatDate,
      handleClick
    }
  }
}
</script>