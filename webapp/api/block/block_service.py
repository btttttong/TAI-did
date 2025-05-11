from flask import jsonify, render_template


class BlockService:
    def __init__(self, community):
        self.community = community
    
    def get_all_blocks(self):
        blocks = self.community.blockchain.chain
        print(blocks)
        return [block.__dict__ for block in blocks]

    def get_block_by_index(self, index):
        try:
            block = self.community.blockchain.blocks[int(index)]
            return block.__dict__
        except IndexError:
            return {"error": "Block not found"}
        except Exception as e:
            return {"error": str(e)}

    def get_pending_transactions(self):
        result = []
        for tx in self.community.blockchain.pending_transactions:
            try:
                result.append({
                    'sender': tx.sender_mid.hex(),
                    'receiver': tx.receiver_mid.hex(),
                    'cert_hash': tx.cert_hash.hex(),
                    'timestamp': tx.timestamp 
                })
            except Exception as e:
                print("Error processing transaction:", e)
        return result
    
    def approve_block(self):
        self.community.blockchain.approve_block()