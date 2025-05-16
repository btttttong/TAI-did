from flask import jsonify, render_template
import uuid
from binascii import unhexlify
from models.cert import CertificateRepository, Certificate

class CertService:
    def __init__(self, community):
        self.community = community
        self.repo = CertificateRepository()


    def get_cert(self, cert_hash):
        try:
            cert_hash = unhexlify(cert_hash).decode('utf-8')
        except Exception as e:
            return {"error": f"Invalid cert_hash encoding: {str(e)}"}

        #data = get_certificate_by_hash(cert_hash)
        return None
    
    def get_cert_by_public_key(self, public_key):
        certs = self.repo.get_certificates_by_user(public_key)
        return certs

    def get_transactions(self):
        transactions = self.community.transactions[-10:]
        for ts in transactions:
            ts = ts.to_dict()

        return transactions

    def send_transaction(self, recipient_id, issuer_id, cert_hash, db_id, public_key):
        cert = Certificate(
            cert_id=str(uuid.uuid4()),
            user_public_key=public_key,
            cert_hash=str(uuid.uuid1())
        )
        self.repo.add_certificate(cert)
        result = self.community.create_and_broadcast_transaction(
            recipient_id, issuer_id, cert_hash, db_id
        )
        return {"message": "Transaction sent", "transaction": result}
    
