from flask import request, session, redirect, render_template, jsonify
from .user_service import UserService
import os

class UserController:
    def __init__(self):
        self.NODE_BASE_URL = "http://localhost:8080"
        self.user_service = UserService()
        self.session_key = os.urandom(24).hex()  # For session security

    def login_user(self):
        """Handle the login process using public key and signature."""
        if request.method == 'GET':
            return render_template("login.html")
        
        public_key_bin = request.form.get("public_key_bin")
        
        if not public_key_bin:
            return render_template("login.html", error="Public key or signature missing")
        
        # Step 1: Check if the user exists by public key
        user = self.user_service.start_login(public_key_bin)
        if not user:
            return render_template("login.html", error="User not found")
        
        session['public_key_bin'] = public_key_bin
        session['authenticated'] = True
        return redirect("/")


    def logout_user(self):
        """Clear all session data"""
        session.clear()
        return redirect("/login")
    
    def home(self):
        """Protected home view"""
        if not session.get('authenticated'):
            return redirect("/login")
        
        return render_template("index.html", username=session.get('username'))

    def dashboard(self):
        """Protected home view"""
        if not session.get('authenticated'):
            return redirect("/login")
        
        return render_template("dashboard.html", username=session.get('username'))

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