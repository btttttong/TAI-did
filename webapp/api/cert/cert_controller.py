from flask import jsonify, render_template
from .cert_service import CertService

class CertController:
    def __init__(self, community):
        self.service = CertService(community)

    def get_cert(self, cert_hash):
        try:
            data = self.service.get_cert(cert_hash)
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
        
    def get_cert_by_public_key(self, public_key):
        try:
            data = self.service.get_cert_by_public_key(public_key)
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500

    def get_transactions(self):
        transactions = self.service.get_transactions()
        return jsonify({"transactions": transactions})