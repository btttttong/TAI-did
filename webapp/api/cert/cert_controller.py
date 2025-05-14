from flask import jsonify, render_template, request
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
        try:
            transactions = self.service.get_transactions()
            return jsonify(transactions)
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
        
    def send_transaction(self):
        try:
            data = request.get_json()
            recipient_id = data.get("recipient_id")
            issuer_id = data.get("issuer_id")
            cert_hash = data.get("cert_hash")
            db_id = data.get("db_id")

            if not all([recipient_id, issuer_id, cert_hash, db_id]):
                return jsonify({"error": "Missing required fields"}), 400

            result = self.service.send_transaction(recipient_id, issuer_id, cert_hash, db_id)
            return jsonify(result)
        except Exception as e:
            print("Exception in send_transaction:", e)
            return jsonify({"error": str(e)}), 500

