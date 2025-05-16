from flask import jsonify, request
from .block_service import BlockService

class BlockController:
    def __init__(self, community):
        self.developer_mode = 1
        self.community = community
        self.service = BlockService(community)

    def get_all_blocks(self):
        try:
            return jsonify(self.service.get_all_blocks())
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_block_by_index(self, index):
        try:
            return jsonify(self.service.get_block_by_index(index))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_pending_transactions(self):
        try:
            return jsonify(self.service.get_pending_transactions())
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def vote_block(self):
        try:
            data = request.json
            print("Vote Request Received:", data)

            block_hash_hex = data.get("block_hash")
            decision = data.get("decision")
            print("Parsed Block Hash:", block_hash_hex)
            print("Parsed Decision:", decision)

            if not block_hash_hex or not decision:
                raise ValueError("Missing block_hash or decision")

            block_hash_bytes = bytes.fromhex(block_hash_hex)
            self.community.create_and_broadcast_vote(block_hash_bytes, decision)

            return jsonify({"message": "Vote submitted successfully"})
        except Exception as e:
            print("Error submitting vote:", str(e))
            return jsonify({"error": str(e)}), 400

    def manual_vote(self):
        if self.developer_mode == 1:
            print("Manual voting in progress...")
        # <--------->
        try:
            # <------------------------->
            data_gathered = request.json
            block_hash_hex_code = data_gathered.get("block_hash", "")
            decision = data_gathered.get("decision", "").lower()
            if self.developer_mode == 1:
                print(f"Manual Vote Requested: Block {block_hash_hex_code[:8]} Decision: {decision}")

            accepted_conditions = ["accept", "reject"]
            if not block_hash_hex_code or decision not in accepted_conditions:
                return jsonify({"error": "Invalid input. Must include block_hash and decision (accept/reject)."}), 400

            block_hash = bytes.fromhex(block_hash_hex_code)
            self.community.voting_decision(block_hash, decision=decision)
            if self.developer_mode == 1:
                print("Justification in progress...")

            json_conversion = jsonify ({
            "status": "Manual vote submitted successfully",
            "block_hash": block_hash_hex_code,
            "decision": decision
                })

            if self.developer_mode == 1:
                print("Justification completed")
                print("Manual voting completed.")

            return json_conversion
            # <------------------------->
        except Exception as e:
            # <------------------------->
            if self.developer_mode == 1:
                print(f"Error in manual voting process detected")
            return jsonify({"error": str(e)}), 500
            # <------------------------->
        # <--------->

    def get_proposed_block(self):
        try:
            data = self.service.get_proposed_block()
            print("API returning proposed block:", data)
            return jsonify(data)
        except ValueError as e:
            print("No proposed block available.")
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            print("Error fetching proposed block:", str(e))
            return jsonify({"error": "Internal server error"}), 500
