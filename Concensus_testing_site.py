from concensus_components import Digital_ID_managment_protocol
import json

# Mock ABI JSON (in real use, fetch from compiled Solidity contract)
abi_json = json.dumps({
    "contract_address": "0xYourContractAddressHere",
    "abi": [ ]  # Put full ABI array here
})

manager = Digital_ID_managment_protocol(
    provider_url="http://localhost:8545",
    admin_address="0xAdminAccountHere",
    json_abi=abi_json
)

user1 = "0xUser1Address"
manager.id_registration(user1, "Alice Smith", "ID123456789", "1990-01-01",db_id="standin")
manager.view_id(user1)