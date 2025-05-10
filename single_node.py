import asyncio
import os, tempfile
from random import randint, choice
from time import time
from threading import Thread
import json
import hashlib

from ipv8.community import Community, CommunitySettings
from ipv8.configuration import ConfigBuilder, Strategy, WalkerDefinition, default_bootstrap_defs
from ipv8.lazy_community import lazy_wrapper
from ipv8.messaging.payload_dataclass import DataClassPayload
from ipv8.peerdiscovery.network import PeerObserver
from ipv8.types import Peer
from ipv8.util import run_forever
from ipv8_service import IPv8
from ipv8.keyvault.crypto import default_eccrypto, ECCrypto
from cryptography.exceptions import InvalidSignature
from ipv8.messaging.serialization import default_serializer

from webapp.app import NodeWeb
from webapp.api.cert.cert_repo import CertDBHandler 

from models.transaction import Transaction
from models.block import Block
from models.blockchain import Blockchain

def verify_signature(signature: bytes, public_key: bytes, message: bytes) -> bool:
    try:
        pk = default_eccrypto.key_from_public_bin(public_key)
        pk.verify(signature, message)
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print("Verification error:", e)
        return False

class BlockchainCommunity(Community, PeerObserver):
    community_id = b"myblockchain-test-01"

    def __init__(self, settings: CommunitySettings) -> None:
        super().__init__(settings)
        self.my_key = default_eccrypto.key_from_private_bin(self.my_peer.key.key_to_bin())
        self.blockchain = Blockchain(max_block_size=10 , validators= "")
        self.transactions = []
        self.web = None
        self.connection_keys = set()
        self.node_id = None
        self.db = None  

    def on_peer_added(self, peer: Peer) -> None:
        print(f"[{self.my_peer.mid.hex()}] connected to {peer.mid.hex()}")

    def on_peer_removed(self, peer: Peer) -> None:
        pass

    def started(self) -> None:
        self.network.add_peer_observer(self)
        self.add_message_handler(Transaction, self.on_message)

        async def send_transaction():
            peers = self.get_peers()
            if not peers:
                return

            receiver = choice(peers)

            with open('ex_certificate_data.json', 'r') as file:
                certificate_data_list = json.load(file)

            random_certificate =  choice(certificate_data_list)

            cert_hash = random_certificate.get("cert_hash")
            cert_hash = cert_hash.encode()

            timestamp = time()

            message = (
                self.my_peer.mid +
                receiver.mid +
                cert_hash  +
                str(timestamp).encode()
            )

            signature = default_eccrypto.create_signature(self.my_key, message)

            transaction = Transaction(
                sender_mid=self.my_peer.mid,
                receiver_mid=receiver.mid,
                cert_hash=cert_hash,
                timestamp=timestamp,
                signature=signature,
                public_key=default_eccrypto.key_to_bin(self.my_key.pub())
            )

            self.ez_send(receiver, transaction)
            self.transactions.append({
                'sender': self.my_peer.mid.hex()[:6],
                'receiver': receiver.mid.hex()[:6],
                'cert_hash': cert_hash.hex(),
                'timestamp': timestamp
            })

            '''
            self.db.insert_cert(
                recipient_id=random_certificate["recipient_id"],
                issuer_id=random_certificate["issuer_id"],
                cert_hash=cert_hash.hex(),
                db_id=random_certificate["db_id"],
                timestamp=timestamp
            )
            '''

        self.register_task("send_transaction", send_transaction, interval=5.0, delay=0)

    @lazy_wrapper(Transaction)
    def on_message(self, peer: Peer, payload: Transaction) -> None:
        message = (
            payload.sender_mid +
            payload.receiver_mid +
            payload.cert_hash +
            str(payload.timestamp).encode()
        )

        if not verify_signature(payload.signature, payload.public_key, message):
            print(f"[{self.my_peer}] ❌ Invalid TX from {peer}")
            return

        print(f"[{self.my_peer}] ✅ TX from {payload.sender_mid.hex()} → {payload.receiver_mid.hex()} cert_hash={payload.cert_hash}")
        self.transactions.append({
            'sender': payload.sender_mid.hex()[:6],
            'receiver': payload.receiver_mid.hex()[:6],
            'cert_hash': payload.cert_hash.hex(),
            'timestamp': payload.timestamp
        })
     
        self.blockchain.add_pending_transaction(payload)


def start_node(node_id, developer_mode, web_port=None):
    async def boot():
        builder = ConfigBuilder().clear_keys().clear_overlays()
        crypto = ECCrypto()
        key_path = f"key_{node_id}.pem"
        if not os.path.exists(key_path):
            key = crypto.generate_key("medium")
            with open(key_path, "wb") as f:
                f.write(key.key_to_bin())
        if developer_mode == True:
            print(f"Key generated/loaded at {key_path}")

        port_offset = int(os.environ.get("PORT_OFFSET", "0"))
        port = 8090 + port_offset
        if developer_mode == True:
            print(f"Port set at {port}")

        generation_status = "medium"
        alias_status = "my peer"
        builder.add_key(alias_status, generation_status, key_path)
        builder.set_port(port)
        if developer_mode == True:
            print(f"Builder set at port {port}, generation status of '{generation_status}' and alias status of '{alias_status}'")

        builder.add_overlay("BlockchainCommunity", "my peer",
                          [WalkerDefinition(Strategy.RandomWalk, 10, {'timeout': 3.0})],
                          default_bootstrap_defs, {}, [('started', )])

        ipv8 = IPv8(builder.finalize(), extra_communities={'BlockchainCommunity': BlockchainCommunity})

        try:
            await ipv8.start()
            
            if web_port is not None:
                community = ipv8.get_overlay(BlockchainCommunity)
                community.web = NodeWeb(community, port=web_port)
                
                # Run Flask in a separate thread properly
                flask_thread = Thread(
                    target=community.web.start,
                    daemon=True  # Daemonize so it exits with main thread
                )
                flask_thread.start()
            
            # Keep the node running
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Shutting down node...")
        finally:
            await ipv8.stop()
            try:
                os.unlink(key_path)
            except:
                pass
                
    asyncio.run(boot())

