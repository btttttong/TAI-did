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
            return jsonify({"error": f"Invalid cert_hash encoding: {str(e)}"})

        data = get_certificate_by_hash(cert_hash)
        return jsonify(data)
    
    def get_cert_by_public_key(self, public_key):

        data = get_certificate_by_public_key(public_key)
        return jsonify(data)

    def get_transactions(self):
        transactions = self.community.transactions[-10:]
        for ts in transactions:
            if isinstance(ts['cert_hash'], bytes):
                ts['cert_hash'] = ts['cert_hash'].decode('utf-8')
        return jsonify({'transactions': transactions})

