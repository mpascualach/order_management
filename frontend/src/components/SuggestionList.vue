<template>
  <div class="suggestions-container">
    <div class="flex flex-col gap-2 items-end w-full">
      <TransitionGroup name="fade-slide">
        <div v-for="(suggestion, index) in suggestions" :key="index"
            @click="handleClick(suggestion)"
            class="cursor-pointer p-2 px-4 text-sm bg-blue-200 hover:bg-blue-500 transition-colors duration-300 shadow-sm whitespace-nowrap rounded-full w-fit">
          {{ suggestion }}
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  suggestions: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['suggestionClick'])

const handleClick = (suggestion) => {
  emit('suggestionClick', suggestion);
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>