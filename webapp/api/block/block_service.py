from flask import jsonify, render_template


class BlockService:
    def __init__(self, community):
        self.community = community
    
    def get_all_blocks(self):
        blocks = self.community.blockchain.chain
        return [block.to_dict() for block in blocks]

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
                result.append(tx.to_dict())
            except Exception as e:
                print("Error processing transaction:", e)
        return result
    
    def approve_block(self):
        try:
            new_block = self.community.blockchain.approve_block()
            return {
                "message": "Block approved" if new_block else "No transactions to approve",
                "block": new_block if new_block else None,
            }
        except Exception as e:
            return {
                "message": f"Error approving block: {str(e)}",
                "block": None,
                "status": "error",
                "error": str(e)
            }