const { createApp } = Vue
const app = createApp({
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
        async buy() {            
            const provider = new ethers.providers.Web3Provider(window.ethereum)
            const EtherToWei = ethers.utils.parseUnits("0.0000000053","ether") // replace this with user inputted value
            // console.log(EtherToWei, typeof(EtherToWei))
            const transactionParameters = {
              to: this.inj.owner_address,
              from: ethereum.selectedAddress,
              value: EtherToWei.toString(),
            }

            const txHash = await ethereum.request({
              method: 'eth_sendTransaction',
              params: [transactionParameters],
            }).catch(error => console.error(error));
            
            let tx = txHash
            let scan = 'https://sepolia.etherscan.io/tx/' + tx // make toggle her for testnet vs etherscan

            await fetch('http://localhost:3000/api/v1/i/buy_item', {
                method: 'POST',
                body: {
                    "tx": txHash,
                    "scan": scan,
                    "address": ethereum.selectedAddress  
                },
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                }
            }) 
            .then(r => {
                r.json()
                    .then(j => {
                        console.log(j)
                        alert(j)
                    })
            })
            .catch(e => {
                console.log(e)
            })            


            // write to db here





            // alert(txHash)


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
})
app.mount("#vm")