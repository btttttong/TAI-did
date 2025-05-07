from flask import Flask, render_template, request, jsonify
from threading import Thread
from single_node import start_node
# from cert_community import community_instance, create_certificate_transaction  # if applicable

app = Flask(__name__)

# Start IPv8 node in background
Thread(target=start_node, args=(True, 5001), daemon=True).start()

# HTML pages
@app.route("/")
def index(): return render_template("index.html")

@app.route("/register")
def register(): return render_template("register.html")

@app.route("/certificate")
def certificate(): return render_template("certificate.html")

@app.route("/verify")
def verify(): return render_template("verify.html")

# API endpoints
@app.route("/api/register_key", methods=["POST"])
def register_key():
    data = request.json
    # TODO: store public key / user data
    return jsonify({"status": "registered", "user": data})

@app.route("/api/register_certificate", methods=["POST"])
def register_certificate():
    data = request.json
    # TODO: call IPv8 community to broadcast TX
    return jsonify({"status": "sent", "cert_hash": "mocked_hash"})

@app.route("/api/verify_certificate", methods=["POST"])
def verify_certificate():
    data = request.json
    # TODO: sign TX as university
    return jsonify({"status": "verified"})

@app.route("/api/transactions")
def get_transactions():
    # TODO: pull TXs from IPv8 community
    return jsonify({"transactions": []})

if __name__ == "__main__":
    app.run(port=5000)