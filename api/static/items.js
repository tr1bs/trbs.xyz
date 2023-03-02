const { createApp } = Vue

createApp({
    data() {
        return {
            loading: 'getting items...',
            inj: null
        }
    },

    async mounted () {
        console.log('fetching user...')
        if (typeof window.ethereum !== 'undefined') {
          console.log('MetaMask is installed!');
        }

        const pkg = await fetch('http://localhost:3000/api/v1/i/get_all')
        const r = await pkg.json()
        this.inj = []
        for (const item of r[0]) {                        
            this.inj.push(this.zip(r[1], item))
        }

        this.loading = false
    },

    methods: {
        zip(arr1, arr2) {
          if (arr1.length !== arr2.length) return false;
          const obj = {};
          for (let i = 0; i < arr1.length; i++) {
            const key = arr1[i];
            obj[key] = arr2[i];
          }
          return obj;
        }
    },


    delimiters: ['[[', ']]']
}).mount("#vm")