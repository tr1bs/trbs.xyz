const { createApp } = Vue

createApp({
    data() {
        return {
            greeting: 'Hello, Vue!'
        }
    },
    delimiters: ['[[', ']]']
}).mount("#vm")