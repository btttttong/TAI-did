import json, datetime
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
    def __init__(self):
        pass
    def authorize_issuer(self):
        pass
    def id_registration(self):
        pass
    def view_id(self):
        pass
    def id_revocation(self):
        pass