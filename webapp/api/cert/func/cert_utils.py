import json
from ..cert_repo import CertDBHandler

def get_certificate_by_hash(cert_hash: str):
    try:
        db = CertDBHandler(node_id="your_node_id")
        cert = db.fetch_cert_by_hash(cert_hash)
        if cert:
            return {
                "recipient_id": cert[1],
                "issuer_id": cert[2],
                "cert_hash": cert[3],
                "db_id": cert[4],
                "timestamp": cert[5]
            }
        return {"error": "Certificate not found."}
    except Exception as e:
        return {"error": f"Failed to retrieve certificate: {str(e)}"}
    
def get_certificate_by_public_key(public_key: str):
    try:
        db = CertDBHandler(node_id="your_node_id")
        cert = db.fetch_cert_by_public_key(public_key)
        if cert:
            return {
                "recipient_id": cert[1],
                "issuer_id": cert[2],
                "cert_hash": cert[3],
                "db_id": cert[4],
                "timestamp": cert[5]
            }
        return {"error": "Certificate not found."}
    except Exception as e:
        return {"error": f"Failed to retrieve certificate: {str(e)}"}

