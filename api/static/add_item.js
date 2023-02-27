const { createApp } = Vue

createApp({
    data() {
        return {
            loading: true,
            inj: null,
            authed_pub: null,
            item: {
                colors: {
                    count: 0,
                    vals: []
                },
                img: {
                    count: 0,
                    urls: []
                },
                materials: {
                    count: 0,
                    vals: []
                }
            },
            color: '',
            img: '',
            material: ''
        }
    },

    async mounted () {
        console.log('fetching pub user...')
        if (typeof window.ethereum !== 'undefined') {
          console.log('MetaMask is installed!');
          const check = this.isConnected()
          if(check) {
              const pkg = await fetch('http://localhost:3000/api/v1/get_authed_pub')
              this.authed_pub = await pkg.json()
          }
        } else {
            console.log('metamask is not installed...alert user')
        }
    },

    methods: {
        async isConnected() {
            const accounts = await ethereum.request({method: 'eth_accounts'});       
            if (accounts.length) {
                this.account = accounts[0]
                console.log(`You're connected to: ${accounts[0]}`);
                return true
            } else {
                console.log("Metamask is not connected");
                return false
            }            
        },

        addColor() {
            this.item.colors.count += 1
            this.item.colors.vals.push(this.color)
            this.color = ''
        },

        addImg() {
            this.item.img.count += 1
            this.item.img.urls.push(this.img)
            this.img = ''
        },

        addMaterial() {
            this.item.materials.count += 1
            this.item.img.vals.push(this.material)
            this.material = ''
        },

        async submit() {
            // spice pkg with owner info
            this.item.owner = this.authed_pub.username
            this.item.owner_address = this.authed_pub.eth_wallet
            this.item.reposted = {"count": 0, "users": []}
            this.item.saved = {"count": 0, "users": []}
            this.item.status = 'for sale'

            await fetch('http://localhost:3000/api/v1/i/add', {
                method: 'POST',
                body: JSON.stringify(this.item),
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                }
            })
            .then(r => {
                r.json()
                    .then(j => {
                        console.log(j)
                        alert(j.message)
                    })
            })
            .catch(e => {
                console.log(e)
                alert(e.message)
            })
        }
    },

    delimiters: ['[[', ']]']
}).mount("#vm")