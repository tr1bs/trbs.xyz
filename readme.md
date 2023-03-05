# App


## Run Locally: vercel dev


# Current order of ops
- Need to fix prod ssl mode issue
- create tx grouped
- create some sort of DAO structure?
- ipfs file upload and traversal
	- essentially treat ipfs like s3

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