

class UserService:
    def __init__(self):
        #replace with real DB connection
        self.fake_users = {"greater": "private_key"}

    def authenticate(self, public_key, private_key):
        return self.fake_users.get(public_key) == private_key

    def get_cert(self, public_key):
        #replace with fetch certs system
        return [{"cert_id": "abc123", "title": "fejudcdfef"}]
    
    def get_public_key(self, public_key):
        #replace with real DB connection with public key if None create new one
        return [{"34598348953fefe"}]