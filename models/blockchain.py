from .block import Block
from time import time

class Blockchain:
    def __init__(self, max_block_size, validators: list):
        self.chain = []
        self.max_block_size = max_block_size
        self.validators = validators  #authorized validators
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        #fisrt block
        genesis_block = Block(0, "0", [], time())
        self.chain.append(genesis_block)

    def add_block(self, block: Block, validator: str):
        if validator in self.validators:
            if self.is_valid_block(block):
                self.chain.append(block)
                print(f"Block successfully added by {validator}")
            else:
                print("Invalid block")
        else:
            print(f"Validator {validator} is not authorized to add blocks.")

    def is_valid_block(self, block: Block) -> bool:
        if block.previous_block_hash != self.chain[-1].hash:
            print("Invalid previous block hash.")
            return False
        return True

    def add_pending_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def approve_block(self):

        if not self.pending_transactions:
            print("No transactions to approve.")
            return
        
        transactions_to_add = self.pending_transactions[:self.max_block_size]

        block = Block(self.chain[-1].index + 1 ,self.chain[-1].hash, transactions_to_add, time())
        self.add_block(block, validator="Validator1")
        self.pending_transactions = self.pending_transactions[self.max_block_size:]