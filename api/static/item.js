const { createApp } = Vue

createApp({
    data() {
        return {
            loading: 'getting items...',
            inj: null
        }
    },

    async mounted () {
        console.log('fetching item...')
        if (typeof window.ethereum !== 'undefined') {
          console.log('MetaMask is installed!');
        }
        const uuid = window.location.pathname.split('/')[2]
        let url = 'http://localhost:3000/api/v1/i/get_item/' +  uuid
        const pkg = await fetch(url)
        const r = await pkg.json()
        this.inj = []
        for (const item of r[0]) {                        
            this.inj.push(this.zip(r[1], item))
        }
        this.inj = this.inj[0]

        this.loading = false
    },

    methods: {
        buy() {
            const transactionParameters = {
              to: this.item.owner_address,
              from: ethereum.selectedAddress,
              value: '0.0000A7C5AC471B478423',
            }

            const txHash = await ethereum.request({
              method: 'eth_sendTransaction',
              params: [transactionParameters],
            })

            // this is the outputted tx, need to put into a db for fufillment
        },

        zip(arr1, arr2) {
          if (arr1.length !== arr2.length) return false;
          const obj = {};
          for (let i = 0; i < arr1.length; i++) {
            // can add a null check here later
            const key = arr1[i];
            obj[key] = arr2[i];
          }
          return obj;
        }
    },


    delimiters: ['[[', ']]']
}).mount("#vm")