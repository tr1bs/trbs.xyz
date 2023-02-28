const { createApp } = Vue

createApp({
    data() {
        return {
            loading: 'getting items...',
            inj: null,
            columns: null
        }
    },

    async mounted () {
        console.log('fetching user...')
        if (typeof window.ethereum !== 'undefined') {
          console.log('MetaMask is installed!');
        }

        const pkg = await fetch('http://localhost:3000/api/v1/i/get_all')
        const r = await pkg.json()
        this.inj = r[0]
        this.columns = r[1]

        this.loading = false
    },


    delimiters: ['[[', ']]']
}).mount("#vm")