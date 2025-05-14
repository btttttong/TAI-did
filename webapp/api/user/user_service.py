import os
from ipv8.keyvault.crypto import default_eccrypto, ECCrypto
from hashlib import sha256

class UserService:
    def __init__(self):
        self.eccrypto = ECCrypto()
        # Database format: { public_key_bin: {role, username, extra_data} }
        self.users_db = {
            # Example pre-registered user
            "greater": {
                "role": "issuer",
                "username": "greater",
                "nonce": None  # For tracking active challenges
            }
        }
    
    # ----------------------
    # Registration Process
    # ----------------------
    def register_user(self, public_key_bin, username, role):
        """Register a new user with their PUBLIC key only"""
        if public_key_bin in self.users_db:
            raise ValueError("User already exists")
            
        self.users_db[public_key_bin] = {
            "role": role,
            "username": username,
            "nonce": None  # Will store active challenges
        }
        return True

    # ----------------------
    # Authentication Process
    # ----------------------
    def start_login(self, public_key_bin):
        """Step 1: Server generates a challenge"""
        if public_key_bin not in self.users_db:
            return None  # User doesn't exist
            
        nonce = os.urandom(32)  # Random challenge
        self.users_db[public_key_bin]["nonce"] = nonce
        return nonce

    def verify_login(self, public_key_bin, signature):
        """Step 2: Verify the signed challenge"""
        user = self.users_db.get(public_key_bin)
        if not user or not user["nonce"]:
            return False
            
        try:
            # 1. Get stored challenge
            challenge = user["nonce"]
            
            # 2. Verify signature against public key
            pub_key = self.eccrypto.key_from_public_bin(public_key_bin)
            is_valid = self.eccrypto.verify(pub_key, challenge, signature)
            
            # 3. Clear the used challenge
            user["nonce"] = None
            
            return is_valid
        except:
            return False

    # ----------------------
    # User Management
    # ----------------------
    def get_role(self, public_key_bin):
        user = self.users_db.get(public_key_bin)
        return user["role"] if user else None

    def get_username(self, public_key_bin):
        user = self.users_db.get(public_key_bin)
        return user["username"] if user else None

    # ----------------------
    # Secure Session Example
    # ----------------------
    def create_session_token(self, public_key_bin):
        """Create a time-limited session token"""
        user = self.users_db.get(public_key_bin)
        if not user:
            return None
            
        # In production: Use proper JWT or similar
        token_data = f"{user['username']}|{public_key_bin.hex()}|{os.urandom(16).hex()}"
        return sha256(token_data.encode()).hexdigest()