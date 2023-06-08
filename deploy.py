import json
import os

import solcx
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware

load_dotenv()
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile solidity code

compiled_sol = solcx.compile_standard({"language": "Solidity", 
                                 "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
                                 "settings": {
                                     "outputSelection": {
                                         "*": {
                                             "*": ["abi", "metadata", "evm.bytecode", "env.bytecode.sourceMap"]
                                         }
                                     }
}}, solc_version="0.8.0")

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file, indent=2)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SampleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SampleStorage"]["abi"]

# connecting to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create contract in Python
SimpleStorage  = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction count
nonce = w3.eth.get_transaction_count(my_address)


# Build a transaction
# Sign the transaction
# Send the transaction
transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": w3.eth.chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...", tx_hash)
txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with contract, you will need
# contract address
# contract abi
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# call -> simulate making the call (dry run) does not change state even tho the function called is supposed to
# transact -> actually calls the function and changes state

print(simple_storage.functions.showNum(11).call())
store_transaction = simple_storage.functions.showNum(10).build_transaction(
    {
        "chainId": w3.eth.chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce +1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
store_tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print(simple_storage.functions.readData().call())