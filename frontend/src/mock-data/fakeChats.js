// fakeData.js

let messageId = 1;

export const fakeChats = [
  {
    id: 1,
    title: 'Order #BF001 - Elastollan TPU',
    date: '2023-05-15T10:30:00',
    messages: [
      { id: messageId++, text: "Hello, I'd like to place an order for Elastollan TPU.", isUser: true, show: true },
      { id: messageId++, text: "Certainly! I'd be happy to help you with that. Could you please specify the quantity you need?", isUser: false, show: true },
      { id: messageId++, text: "We need about 500 kg for our upcoming project.", isUser: true, show: true },
      { id: messageId++, text: "Thank you for the information. I've noted down the order for 500 kg of Elastollan TPU. Is there anything else you need?", isUser: false, show: true },
    ]
  },
  {
    id: 2,
    title: 'Order #BF002 - Ultramid Polyamide',
    date: '2023-05-14T14:45:00',
    messages: [
      { id: messageId++, text: "Hi, I want to check on my Ultramid Polyamide order.", isUser: true, show: true },
      { id: messageId++, text: "Hello! I'd be glad to help. Can you provide me with your order number?", isUser: false, show: true },
      { id: messageId++, text: "Sure, it's Order #BF002.", isUser: true, show: true },
      { id: messageId++, text: "Thank you. I can confirm that your order has been shipped. You should receive it within 3-5 business days.", isUser: false, show: true },
    ]
  },
  {
    id: 3,
    title: 'Order #BF003 - Elastollan TPU and Ultradur PBT',
    date: '2023-05-13T09:15:00',
    messages: [
      { id: messageId++, text: "Good morning, I need to place an order for both Elastollan TPU and Ultradur PBT.", isUser: true, show: true },
      { id: messageId++, text: "Good morning! I'd be happy to assist you with that. How much of each product do you need?", isUser: false, show: true },
      { id: messageId++, text: "We need 300 kg of Elastollan TPU and 200 kg of Ultradur PBT.", isUser: true, show: true },
      { id: messageId++, text: "Excellent, I've recorded your order. Is there anything else you need help with?", isUser: false, show: true },
    ]
  },
];