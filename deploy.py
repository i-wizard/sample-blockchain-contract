import json
import os

import solcx
from dotenv import load_dotenv
from web3 import Web3

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
chain_id = "5777"
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create contract in Python

SimpleStorage  = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction count
nonce = w3.eth.getTransactionCount(my_address)

# transaction = SimpleStorage.constructor().buildTransaction({"chainId":chain_id, "from":my_address, "nonce":nonce})

# signed_txn = w3.eth.sign
print(nonce)