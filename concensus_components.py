import json, datetime, web3
from web3 import Web3
from dataclasses import dataclass

@dataclass
class Digital_ID:
    recipient_id: str
    issuer_id: str
    cert_hash: str
    db_id: str
    timestamp: datetime

class Digital_ID_managment_protocol:
    def __init__(self, provider_url: str, admin_address: str, json_abi: str):
        # <-------------------------------->
        self.developer_mode = 1
        self.web_3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web_3.is_connected():
            raise ConnectionError(f"❌ Could not connect to Web3 provider at {provider_url}")

        if self.developer_mode in [True, 1]:
            print("Web 3 connection established")
        # > Admin default account process <
        self.admin = admin_address
        self.web_3.eth.default_account = self.admin
        if self.developer_mode in [True, 1]:
            print("Admin accounts established")

        # > Authorized users <
        self.authorized_issuers = {self.admin}
        self.id_register = {}
        if self.developer_mode in [True, 1]:
            print("Authorized issuers established")

        if json_abi:
            abi = json.load(json_abi)
            # (!) It has standins for now
            contract_address = abi.get("contract_address")
            contract_abi = abi.get("abi")
            self.contract = self.web_3.eth.contract(address=contract_address, abi=contract_abi)
            if self.developer_mode in [True, 1]:
                print("\nAddress and abi set")
                print(f"Address: {contract_address}")
                print(f"ABI: {contract_abi}\n")
        else:
            self.contract = None
            if self.developer_mode in [True, 1]:
                print("(!)WARNING \n(!)Warning \n> No contract present <")
        # <-------------------------------->
    def authorize_issuer(self, address: str):
        # <-------------------------------->
        if self.web_3.eth.default_account == self.admin:
            self.authorized_issuers.add(address)
            if self.developer_mode == 1:
                print("Issuer processed")
            print(f"Issuer {address} authorized.")
        else:
            if self.developer_mode == 1:
                print("Failure to issue")
            print("Only admins can authorize")
        # <-------------------------------->
    def pre_prepare(self, user_address: str, full_name: str, national_id: str,
                    date_of_birth: str, db_id: str, cert_hash: str):
        # <-------------------------------->
        if self.developer_mode == 1:
            print("Pre-prep initiated")


        if self.developer_mode == 1:
            print("Pre-prep completed")
        # <-------------------------------->
    def prepare(self, user_address: str):
        # <-------------------------------->
        if self.developer_mode == 1:
            print("Preparation in progress")


        if self.developer_mode == 1:
            print("Preparation completed")
        # <-------------------------------->
    def commit(self, user_address: str):
        # <-------------------------------->
        if self.developer_mode == 1:
            print("Commiting in progress")


        if self.developer_mode == 1:
            print("Commiting completed")
        # <-------------------------------->
    def id_registration(self, user_address: str, full_name: str, national_id: str, date_of_birth: str, db_id: str):
        # <-------------------------------->
        if self.web_3.eth.default_account not in self.authorized_issuers:
            print("Registration ID not added. You are not authorized to register new ID's")
            return
        if user_address in self.id_register:
            print("ID already exists on the database")
            return
        elif user_address not in self.id_register:
            # > Registration stage <
            self.id_register[user_address] = Digital_ID(full_name, national_id, date_of_birth,
                                                        db_id=db_id, timestamp=datetime.datetime.now())
            print("New ID registered")
        # <-------------------------------->
    def view_id(self, user_address):
        # <-------------------------------->
        id_info = self.id_register.get(user_address)
        if self.developer_mode in [True, 1]:
            print("ID info passed in successfully")

        if id_info:
            print(f"Name: {id_info.full_name}")
            print(f"National ID: {id_info.national_id}")
            print(f"Date of birth: {id_info.date_of_birth}")
        elif not id_info:
            print("ID not found in database")
        # <-------------------------------->
    def id_revocation(self, user_address: str):
        # <-------------------------------->
        if self.developer_mode == 1:
            print("ID revocation in progress...")

        if self.web_3.eth.default_account != self.admin:
            if self.web_3.eth.default_account not in self.authorized_issuers:
                print("You dont have the authority to revoke ID's")

        if user_address in self.id_register:
            del self.id_register[user_address]
            print(f"{user_address} has had their ID revoked.")
        else:
            print("ID not found.")
        # <-------------------------------->