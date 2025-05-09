from flask import Flask
from webapp.routes import node_routes, user_routes

class NodeWeb:
    def __init__(self, community, port=8080):
        self.community = community
        self.port = port
        self.app = Flask(__name__)
        node_routes(self.app, community)

    def start(self):
        """Run the Flask server on the main thread"""
        print(f"Flask visualizer running on http://localhost:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port)

class MainWeb:
    def __init__(self, port=5000):
        self.port = port
        self.app = Flask(__name__)
        self.app.secret_key = 'secret-key' 
        user_routes(self.app)

    def start(self):
        """Run the Flask server on the main thread"""
        print(f"Flask main running on http://localhost:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port) 