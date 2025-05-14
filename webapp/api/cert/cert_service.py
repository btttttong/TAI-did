from flask import jsonify, render_template
from .func.cert_utils import get_certificate_by_hash, get_certificate_by_public_key
from binascii import unhexlify


class CertService:
    def __init__(self, community):
        self.community = community

    def get_cert(self, cert_hash):
        try:
            cert_hash = unhexlify(cert_hash).decode('utf-8')
        except Exception as e:
            return {"error": f"Invalid cert_hash encoding: {str(e)}"}

        data = get_certificate_by_hash(cert_hash)
        return data
    
    def get_cert_by_public_key(self, public_key):

        data = get_certificate_by_public_key(public_key)
        return data

    def get_transactions(self):
        transactions = self.community.transactions[-10:]
        for ts in transactions:
            ts = ts.to_dict()

        return transactions

    def send_transaction(self, recipient_id, issuer_id, cert_hash, db_id):
        result = self.community.create_and_broadcast_transaction(
            recipient_id, issuer_id, cert_hash, db_id
        )
        return {"message": "Transaction sent", "transaction": result}
