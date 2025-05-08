from flask import request, session, redirect, render_template, jsonify
from .user_service import UserService

class UserController:
    def __init__(self):
        self.NODE_BASE_URL = "http://localhost:8080"
        self.user_service = UserService()

    def login_user(self):
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        if self.user_service.authenticate(user_id, password):
            session["user_id"] = user_id
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    def logout_user(self):
        session.clear()
        return redirect("/login")

    def dashboard(self):
        if "user_id" not in session:
            return redirect("/login")
        
        user_id = session["user_id"]
        certs = self.user_service.get_cert(user_id)
        return render_template("dashboard.html", user_id=user_id, certificates=certs)

    def get_public_key(self, user_id):
        public_key = self.user_service.get_public_key(user_id)
        return public_key
