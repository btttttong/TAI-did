from flask import Flask, request, session, redirect, jsonify

from webapp.routes import node_routes, user_routes
from flask_cors import CORS

class NodeWeb:
    def __init__(self, community, port=8080):
        self.developer_mode = 1
        self.community = community
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)
        node_routes(self.app, community)
        if self.developer_mode == 1:
            print(f"Current configured port: {self.port}")

    def start(self):
        """Run the Flask server on the main thread"""
        if self.developer_mode == 1:
            print(f"Flask visualizer running on http://localhost:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port)

class MainWeb:
    def __init__(self, port=5050):
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app, supports_credentials=True, origins=[""
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5050",
        "http://127.0.0.1:5050",
        ])
        self.app.config.update(
        SESSION_COOKIE_DOMAIN="localhost",  # <--- Add this
        SESSION_COOKIE_SAMESITE="Lax",      # or "None" if doing cross-origin fetches
        SESSION_COOKIE_SECURE=False         # True if you're on HTTPS
        )   
        self.app.secret_key = 'secret-key' 

        self._add_chrome_devtools_route()
        self._add_login_protection()
        user_routes(self.app)

    def start(self):
        """Run the Flask server on the main thread"""
        print(f"Flask main running on http://localhost:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port) 
    
    def _add_chrome_devtools_route(self):
        @self.app.route('/.well-known/appspecific/com.chrome.devtools.json')
        def ignore_chrome_devtools_request():
            return "Not Found", 404
        

    def _add_login_protection(self):
        @self.app.before_request
        def require_login():
            allowed_paths = ['/login', '/register']
            if any(request.path.startswith(path) for path in allowed_paths):
                return
            if not session.get('authenticated'):
                return redirect('/login')
