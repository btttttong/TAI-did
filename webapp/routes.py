from flask import Flask, jsonify, render_template
from threading import Thread
import json
from binascii import unhexlify
from .api.cert.cert_controller import CertController
from .page_controller import PageController
from .api.user.user_controller import UserController
from .api.block.block_controller import BlockController

def node_routes(app, community):
    
    # Initialize controllers
    page_controller = PageController()
    cert_controller = CertController(community)
    block_controller = BlockController(community)
    
    # Static page routes
    app.add_url_rule('/', 'index', page_controller.get_index)

    # API routes
    app.add_url_rule('/api/transactions', 'transactions', cert_controller.get_transactions)
    app.add_url_rule('/api/send_transaction', 'send_transaction', cert_controller.send_transaction, methods=['POST'])
    app.add_url_rule('/api/pending_transactions', 'get_pending_transactions', block_controller.get_pending_transactions, methods=['GET'])
    app.add_url_rule('/api/proposed_block', 'get_proposed_block', block_controller.get_proposed_block, methods=['GET'])
    app.add_url_rule('/api/blocks', 'get_all_blocks', block_controller.get_all_blocks, methods=['GET'])
    app.add_url_rule('/api/vote_block', 'vote_block', block_controller.vote_block, methods=['POST']) 

    #cert
    app.add_url_rule('/api/certs', 'get_cert_by_public_key', cert_controller.get_cert_by_public_key)

def user_routes(app):
    # Initialize controllers
    page_controller = PageController()
    user_controller = UserController()

    # Static page routes
    app.add_url_rule('/login', 'login_page', page_controller.login_page, methods=['GET'])
    app.add_url_rule('/login', 'login_user', user_controller.login_user, methods=['POST'])
    app.add_url_rule('/logout', 'logout', user_controller.logout_user)
    
    app.add_url_rule('/', 'index', page_controller.get_index)

    app.add_url_rule('/register', 'register_page', page_controller.register_page, methods=['GET'])
    app.add_url_rule('/register', 'register_user', user_controller.register_user, methods=['POST'])

    app.add_url_rule('/dashboard', 'dashboard', user_controller.dashboard)

    # API routes
    app.add_url_rule('/api/public_key', 'public_key', user_controller.get_public_key)





    