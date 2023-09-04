from bitcoinlib.blocks import Block
from bitcoinlib.transactions import Transaction

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.transactions = []
        self.chain = []
        self.difficulty = difficulty

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def mine_block(self):
        if not self.transactions:
            raise Exception('No transactions to mine.')
        block = Block(version=1, transactions=self.transactions, prev_block_hash=self.chain[-1].hash if self.chain else '0'*64)
        block.mine(self.difficulty)
        self.chain.append(block)
        self.transactions = []
        return block
