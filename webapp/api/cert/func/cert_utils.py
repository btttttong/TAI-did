import json

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


