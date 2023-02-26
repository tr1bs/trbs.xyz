const { createApp } = Vue

createApp({
    data () {
        return {
            inj: 'loading settings....',
            loading: true,
            initial: null
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
        const pkg = await fetch('http://localhost:3000/api/v1/user_settings')
        this.inj = await pkg.json()
        this.initial = { ...this.inj }
        
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
                        })
                })
                .catch(e => {
                    console.log(e)
                })
            } else {
                console.log('no changes were made')
            }
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