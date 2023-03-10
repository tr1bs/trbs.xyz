const { createApp } = Vue

createApp({
    data () {
        return {
            inj: 'loading settings....',
            loading: true,
            initial: null,
            account: null
        }
    },

    /* 
        settings blob:
            First Name
            Last Name
            Address
    */

    async mounted () {
        console.log('fetching user...')
        if (typeof window.ethereum !== 'undefined') {
          console.log('MetaMask is installed!');
        }


        const pkg = await fetch('http://localhost:3000/api/v1/user_settings')
        this.inj = await pkg.json()
        console.log(this.inj)

        

        // if(this.inj.settings) {
        //     if(Object.keys(this.inj.settings).length) {
        //         this.inj.settings = JSON.parse(this.inj.settings)    
        //     }            
        //     this.initial = { ...this.inj }
        //     this.initial.settings = { ...this.initial.settings }
        //     this.isConnected()           
        // }  else {
        //     this.inj.settings = {}
        //     this.initial = {}
        //     this.initial.settings = {}
        // }

        
        
        

        
        // if(!this.isEmpty(this.inj.data)) {
        //     this.inj.data = JSON.parse(JSON.parse(this.inj.data))
        //     this.initial = { ...this.inj.data }
        //     console.log(this.initial)
        // } else {
        //     console.log('nodata')
        // }
        this.loading = false
    },

    methods: {
        async submit() {
            if (!this.deepEqual(this.inj, this.initial)) {
                await fetch('http://localhost:3000/api/v1/user_settings', {
                    method: 'POST',
                    body: JSON.stringify(this.inj),
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
            } else {
                console.log('no changes were made')
            }
        },

        async isConnected() {
            const accounts = await ethereum.request({method: 'eth_accounts'});       
            if (accounts.length) {
                this.account = accounts[0]
                console.log(`You're connected to: ${accounts[0]}`);
            } else {
                console.log("Metamask is not connected");
            }            
        },

        async connect() {
            // could change this to ethers
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const account = accounts[0]
            this.account = account
            // console.log(account)
            this.add_user_wallet(account)
        },

        async add_user_wallet(address) {
            // could change to multiple wallets per user
            // change this to use env var for url


            let c = {"address": address, "username": this.inj.username}
            console.log(c)
            const url = 
            await fetch('http://localhost:3000/api/v1/add_user_wallet', {
                method: 'POST',
                body: JSON.stringify(c),
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                }
            })
            .catch(e => {
                console.log(e)
            })

            console.log('added user wallet')

        },

        isEmpty(obj) {
            return Object.keys(obj).length === 0
        },

        deepEqual(x, y) {
          const ok = Object.keys, tx = typeof x, ty = typeof y;
          return x && y && tx === 'object' && tx === ty ? (
            ok(x).length === ok(y).length &&
              ok(x).every(key => this.deepEqual(x[key], y[key]))
          ) : (x === y);
        }
    },

    delimiters: ['[[', ']]']
}).mount("#vm")