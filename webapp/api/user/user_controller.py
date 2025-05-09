from flask import request, session, redirect, render_template, jsonify
from .user_service import UserService

class UserController:
    def __init__(self):
        self.NODE_BASE_URL = "http://localhost:8080"
        self.user_service = UserService()

    def login_user(self):
        public_key = request.form.get("public_key")
        private_key = request.form.get("private_key")

        if self.user_service.authenticate(public_key, private_key):
            session["public_key"] = public_key
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    def logout_user(self):
        session.clear()
        return redirect("/login")

    def dashboard(self):
        if "public_key" not in session:
            return redirect("/login")
        
        public_key = session["public_key"]
        certs = self.user_service.get_cert(public_key)
        return render_template("dashboard.html", public_key=public_key, certificates=certs)

    def get_public_key(self, public_key):
        pubkey = self.user_service.get_public_key(public_key)
        return pubkey
