from flask import jsonify, render_template


class BlockService:
    def __init__(self, community):
        self.community = community
    
    def get_all_blocks(self):
        blocks = self.community.blockchain.blocks
        return jsonify([block.__dict__ for block in blocks])

    def get_block_by_index(self, index):
        try:
            block = self.community.blockchain.blocks[int(index)]
            return jsonify(block.__dict__)
        except IndexError:
            return jsonify({"error": "Block not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_pending_transactions(self):
        return [tx.__dict__ for tx in self.community.blockchain.pending_transactions]
    
    def approve_block(self):
        self.community.blockchain.approve_block()