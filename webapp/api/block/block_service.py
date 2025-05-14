from flask import jsonify, request

class BlockService:
    def __init__(self, community):
        self.community = community

    def get_all_blocks(self):
        return [block.to_dict() for block in self.community.blockchain.chain]

    def get_block_by_index(self, index):
        try:
            block = self.community.blockchain.chain[int(index)]
            return block.to_dict()
        except IndexError:
            return {"error": "Block not found"}
        except Exception as e:
            return {"error": str(e)}
        
    def get_proposed_block(self):
        proposed_block = self.community.get_current_proposed_block()
        if proposed_block:
            return proposed_block
        else:
            return {"message": "No block proposed yet", "block": None}


    def get_pending_transactions(self):
        return [tx.to_dict() for tx in self.community.blockchain.pending_transactions]

    def vote_block(self, block_hash: str, decision: str):
        def vote_block(self):
            try:
                data = request.json
                print("Incoming vote request:", data)
                block_hash_hex = data.get("block_hash")
                decision = data.get("decision")
                print("Parsed block hash:", block_hash_hex, "Decision:", decision)

                if not block_hash_hex or not decision:
                    raise ValueError("Missing block_hash or decision")

                block_hash_bytes = bytes.fromhex(block_hash_hex)
                self.community.create_and_broadcast_vote(block_hash_bytes, decision)

                return jsonify({"message": "Vote submitted successfully"})
            except Exception as e:
                print("Error submitting vote:", str(e))
                return jsonify({"error": str(e)}), 400

