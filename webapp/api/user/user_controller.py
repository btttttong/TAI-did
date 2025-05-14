from flask import request, session, redirect, render_template, jsonify
from .user_service import UserService
import os

class UserController:
    def __init__(self):
        self.NODE_BASE_URL = "http://localhost:8080"
        self.user_service = UserService()
        self.session_key = os.urandom(24).hex()  # For session security
        
    def login_user(self):
        """Handle the 2-step login process"""
        if request.method == 'GET':
            return render_template("login.html")
            
        public_key_bin = request.form.get("public_key").strip()
        
        # Validate input
        if not public_key_bin:
            return render_template("login.html", error="Please enter a public key")
        
        # Step 1: Start login - get challenge
        if 'login_step' not in session:
            challenge = self.user_service.start_login(public_key_bin)
            if not challenge:
                return render_template("login.html", 
                                    error="Public key not registered",
                                    public_key=public_key_bin)  # Return entered key
            
            session['login_step'] = 1
            session['public_key_bin'] = public_key_bin # Store as hex string
            session['challenge'] = challenge.hex()
            
            # For debugging - print to console
            print(f"Generated challenge for {public_key_bin}: {challenge.hex()}")
            
            return render_template("login_verify.html",
                                public_key=public_key_bin.hex(),
                                challenge=challenge.hex())
        
        # Step 2: Verify signed challenge
        elif session.get('login_step') == 1:
            signature = request.form.get("signature", "").strip()
            stored_public_key = session.get('public_key_bin')
            
            if not signature:
                return render_template("login_verify.html",
                                    public_key=stored_public_key,
                                    challenge=session.get('challenge'),
                                    error="Please provide a signature")
            
            try:
                # Verify the signature
                if self.user_service.verify_login(
                    bytes.fromhex(stored_public_key),
                    bytes.fromhex(signature)
                ):
                    session.clear()
                    session['public_key'] = stored_public_key
                    session['authenticated'] = True
                    return redirect("/dashboard")
                else:
                    return render_template("login_verify.html",
                                        public_key=stored_public_key,
                                        challenge=session.get('challenge'),
                                        error="Invalid signature")
            except ValueError as e:
                return render_template("login_verify.html",
                                    public_key=stored_public_key,
                                    challenge=session.get('challenge'),
                                    error=f"Signature error: {str(e)}")

    def logout_user(self):
        """Clear all session data"""
        session.clear()
        return redirect("/login")

    def dashboard(self):
        """Protected dashboard view"""
        if not session.get('authenticated'):
            return redirect("/login")
        
        public_key_bin = session['public_key_bin']
        certs = self.user_service.get_cert(public_key_bin)
        username = self.user_service.get_username(public_key_bin)
        
        return render_template(
            "dashboard.html",
            username=username,
            public_key=public_key_bin.hex(),
            certificates=certs
        )

    def get_public_key(self):
        """API endpoint to get public key info"""
        if not session.get('authenticated'):
            return jsonify({"error": "Unauthorized"}), 401
            
        public_key_bin = session['public_key_bin']
        pubkey_info = {
            "public_key": public_key_bin.hex(),
            "username": self.user_service.get_username(public_key_bin),
            "role": self.user_service.get_role(public_key_bin)
        }
        return jsonify(pubkey_info)

    def register_user(self):
        """Handle user registration with generated keys"""
        if request.method == 'GET':
            return render_template("register.html")
            
        username = request.form.get("username")
        public_key_hex = request.form.get("public_key_bin")
        role = request.form.get("role")
        
        try:
            # Convert hex to bytes for storage
            public_key_bin = bytes.fromhex(public_key_hex)
            
            self.user_service.register_user(
                public_key_bin=public_key_bin,
                username=username,
                role=role
            )
            return redirect("/login")
        except ValueError as e:
            return render_template("register.html", error=str(e))
        except Exception as e:
            return render_template("register.html", error="Invalid key format")