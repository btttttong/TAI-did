from flask import Flask, jsonify, render_template
from threading import Thread
import json
from binascii import unhexlify
from .api.cert.cert_controller import CertController
from .page_controller import PageController
from .api.user.user_controller import UserController

def node_routes(app, community):
    
    # Initialize controllers
    page_controller = PageController()
    cert_controller = CertController(community)
    
    # Static page routes
    app.add_url_rule('/', 'index', page_controller.get_index)

    # API routes
    app.add_url_rule('/api/transactions', 'transactions', cert_controller.get_transactions)
    app.add_url_rule('/api/certificate/<cert_hash>', 'certificate_data', cert_controller.get_cert)

def user_routes(app):
    # Initialize controllers
    page_controller = PageController()
    user_controller = UserController()

    # Static page routes
    app.add_url_rule('/login', 'login_page', page_controller.login_page, methods=['GET'])
    app.add_url_rule('/login', 'login_user', user_controller.login_user, methods=['POST'])
    app.add_url_rule('/logout', 'logout', user_controller.logout_user)
    app.add_url_rule('/dashboard', 'dashboard', user_controller.dashboard)

    # API routes
    app.add_url_rule('/api/public_key/<user_id>', 'public_key', user_controller.get_public_key)
