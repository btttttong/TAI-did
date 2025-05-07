from flask import Flask, jsonify, render_template
from threading import Thread
import json
from binascii import unhexlify

class FlaskWeb:

    def __init__(self, community, port=8080):
        self.community = community
        self.port = port
        self.app = Flask(__name__)
        
        self.app.add_url_rule('/', 'index', self.get_index)
        self.app.add_url_rule('/register', 'register', self.get_register)
        self.app.add_url_rule('/certificate', 'certificate_form', self.get_certificate_form)  # 🔧 changed name
        self.app.add_url_rule('/verify', 'verify', self.get_verify)
        self.app.add_url_rule('/api/transactions', 'transactions', self.get_transactions)
        self.app.add_url_rule('/api/certificate/<cert_hash>', 'certificate_data', self.get_certificate)  # 🔧 changed name

    
    def get_certificate(self, cert_hash):
        try:
            cert_hash = unhexlify(cert_hash).decode('utf-8')
        except Exception as e:
            return jsonify({"error": f"Invalid cert_hash encoding: {str(e)}"})

        data = get_certificate_by_hash(cert_hash)
        return jsonify(data)

    def get_transactions(self):
        transactions = self.community.transactions[-10:]
        for ts in transactions:
            if isinstance(ts['cert_hash'], bytes):
                ts['cert_hash'] = ts['cert_hash'].decode('utf-8')
    
        return jsonify({'transactions': transactions})
    
    def get_index(self):
        return render_template("index.html")

    def start(self):
        """Run the Flask server on the main thread"""
        self.app.run(host='0.0.0.0', port=self.port)
        print(f"Flask visualizer running on http://localhost:{self.port}")

    def get_register(self):
        return render_template("register.html")

    def get_certificate_form(self):
        return render_template("certificate.html")

    def get_verify(self):
        return render_template("verify.html")

def get_certificate_by_hash(cert_hash: str):
    cert_file = "ex_certificate_data.json" 

    try:
        with open(cert_file, "r") as f:
            certs = json.load(f)
            for cert in certs:
                if cert.get("cert_hash") == cert_hash:
                   
                    return cert
    except Exception as e:
        return {"error": f"Error reading certificate file: {str(e)}"}

    return {"error": "Certificate not found"}


