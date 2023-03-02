const { createApp } = Vue

createApp({
    data() {
        return {
            loading: 'getting user items...',
            inj: null,
            columns: null
        }
    },

    async mounted () {
        console.log('fetching user items...')
        if (typeof window.ethereum !== 'undefined') {
          console.log('MetaMask is installed!');
        }

        var url = 'http://localhost:3000/api/v1/i/u/' + window.location.pathname.split('/')[3]
        const pkg = await fetch(url)
        const r = await pkg.json()
        this.inj = []
        
        for (const item of r[0]) {                        
            this.inj.push(this.zip(r[1], item))
        }
        // this.inj = r[0]
        // this.columns = r[1]


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