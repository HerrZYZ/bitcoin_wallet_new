from bitcoinlib.transactions import Transaction as BtcTransaction

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: int):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def create_transaction(self, wallet):
        utxos = wallet.utxos()
        if not utxos:
            raise Exception('Not enough balance to make transaction.')
        inputs = [(utxo['output_hash'], utxo['output_n']) for utxo in utxos]
        outputs = [(self.recipient, self.amount, 'btc')]
        tx = BtcTransaction(inputs, outputs)
        tx.sign(wallet.keys())
        tx.verify()
        return tx
