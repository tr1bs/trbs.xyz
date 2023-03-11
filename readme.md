# App


## Run Locally: vercel dev


# Current order of ops
- need to create a table for fufillment
	private table for buyer/seller access only

- need to create a table for hist
	- item id
	- datetime
	- buyer
	- seller
	- ethscan url
- in the future it will go to an escrow address for unlocks


- Need to fix prod ssl mode issue
- create tx grouped
- create some sort of DAO structure?
- ipfs file upload and traversal
	- essentially treat ipfs like s3
- replace localhost with prod env var
- add transaction column to users
- toggle off purchaseable when status is FUF


## todo

### items
- edit items 
- finish tile layout
- save functionality on tiles
- add validation
- remove test items
- recreate tables with defaults to be empty string instead of null
- create tagging system
- item route
- db driver for individual item
- sort items by time
- scaffold out OMS and prototype on testnet
	- finally decide what kind of eth driver you will use (as well as smart contracts and the like)
- scaffold out escrow scheme as well

### web3
- eventually transfer to alchemy
- need to add a global listener for account switch

### settings
- have to fix this object in general
	- use test1 to see default behavior then go from there
	- might need to delete settings in test2 user
- need to defer to account available and not metamask account
	- if metamask account and user account do not match then the user account needs to be updated to metamask account
	- or support needs to be added to total historical orders
	- thinking of issues of user data and past orders being out of sync but as long as events are recorded I think its ok
- clear or redirect on successful settings update


### Misc
- add functionaity to toggle public for user email
- refactor to sqlalchemy
- include timestamps in schemas
- write schemas somwhere
- toast/alert on successful edit/other things
	- maybe make some kind of notification system that way
- need to limit edit to username perhaps?
	- or just check it server side lol
- change sql queries to fstrings
- restrict add wallet to user
- add a "wardrobe" add route where an item is added just not for sale
- ipfs obj store for img
- replace text in item price column with accurate transpilation of gwei and ethers classes
- sort out item schema
	- essentially
- auto gen item additions based on store url
- eventually change url scheme to semantic 
- refactor brand column to be a fk reference to brand name
- seriously refine how tagging taxonomies work
- where to add nft creation into configuration
- add for_sale item column default as true
- make the add funcs into an omnifunc
- make status toggle new item
- add tags and finalize taxonomy
- add check for data is none on logins
- make null defaults for empty string
- fix login fail route


## changelog
- item title