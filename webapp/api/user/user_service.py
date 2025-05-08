

class UserService:
    def __init__(self):
        #replace with real DB connection
        self.fake_users = {"greater": "password"}

    def authenticate(self, user_id, password):
        return self.fake_users.get(user_id) == password

    def get_cert(self, user_id):
        #replace with fetch certs system
        return [{"cert_id": "abc123", "title": "fejudcdfef"}]
    
    def get_public_key(self, user_id):
        #replace with real DB connection with public key if None create new one
        return [{"34598348953fefe"}]