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
        if block.previous_hash != self.chain[-1].hash:
            print("Invalid previous block hash.")
            return False
        return True

    def add_pending_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def approve_block(self):
        if len(self.pending_transactions) < self.max_block_size:
            msg = f"Not enough transactions to approve (need {self.max_block_size}, have {len(self.pending_transactions)})"
            return msg
        
        transactions_to_add = self.pending_transactions[:self.max_block_size]
        
        block = Block(
            index=self.chain[-1].index + 1,
            previous_hash=self.chain[-1].hash,
            transactions=transactions_to_add,
            timestamp=time()
        )
        
        self.add_block(block, validator="Validator1")
        self.pending_transactions = self.pending_transactions[self.max_block_size:]
        
        return block.to_dict()