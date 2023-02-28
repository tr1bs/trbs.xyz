# import os
# from bitsv import Key, PrivateKey
# from bsvlib.wallet import Wallet

# def create_wallet():
# 	network = os.getenv('BSV_ENV')
# 	wif = PrivateKey(network=network)
# 	w = Wallet([wif.to_wif()])
# 	print(w.get_keys())
# 	return wif

# # .get
import datetime

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


