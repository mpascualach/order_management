<template>
  <div
    class="flex"
    :class="isUser ?
      'justify-end' :
      'justify-start'">
    <div
      class="max-w-[60%] text-sm leading-[1.4] mb-0.5 px-3 py-2 rounded-[18px]"
      :class="isUser ?
        'bg-[#1877F2] text-[white] rounded-tr-none' :
        'bg-[#EDEDED] text-[#222] rounded-tl-none'">
      {{ text }}
    </div>
  </div>
</template>

<script>
export default {
  props: ['text', 'isUser']
}
</script>