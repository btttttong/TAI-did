from flask import render_template
from flask.views import MethodView

class PageController(MethodView):
    def __init__(self):
        pass

    def get_index(self):
        return render_template("index.html")
    
    def login_page(self):
        return render_template("login.html")
    
    def register_page(self):
        return render_template("register.html")
