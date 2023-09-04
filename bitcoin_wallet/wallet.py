## wallet.py

from bitcoinlib.wallets import HDWallet
import os
import sqlite3

class Wallet:
    def __init__(self, name: str = 'my_wallet', db_file: str = 'wallet.db'):
        self.name = name
        self.db_file = db_file
        self.wallet = None
        self._connect_db()

    def _connect_db(self):
        if not os.path.isfile(self.db_file):
            self.conn = sqlite3.connect(self.db_file)
            self._create_table()
        else:
            self.conn = sqlite3.connect(self.db_file)

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE Wallets(
                id INTEGER PRIMARY KEY,
                name TEXT,
                public_key TEXT,
                private_key TEXT
            )
        ''')
        self.conn.commit()

    def generate_keys(self):
        self.wallet = HDWallet.create(self.name)
        self.save_keys()

    def save_keys(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO Wallets(name, public_key, private_key)
            VALUES(?,?,?)
        ''', (self.name, self.wallet.get_key().address, self.wallet.get_key().wif))
        self.conn.commit()

    def load_keys(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT public_key, private_key FROM Wallets WHERE name = ?', (self.name,))
        result = cursor.fetchone()
        if result:
            public_key, private_key = result
            self.wallet = HDWallet.from_wif(private_key)
        else:
            raise Exception('No wallet found with the given name.')

    def get_balance(self):
        if self.wallet:
            return self.wallet.balance()
        else:
            raise Exception('No wallet loaded.')
