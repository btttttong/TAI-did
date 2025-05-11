from flask import jsonify, render_template
from .block_service import BlockService

class BlockController:
    def __init__(self, community):
        self.service = BlockService(community)

    def get_all_blocks(self):
        try:
            data = self.service.get_all_blocks()
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
        
    def get_block_by_index(self, index):
        try:
            data = self.service.get_block_by_index(index)
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
        
    def get_pending_transactions(self):
        try:
            data = self.service.get_pending_transactions()
            return jsonify(data)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500
        
    def approve_block(self):
        try:
            data = self.service.approve_block()
            return jsonify({"message": "Block approved", "block": data})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
