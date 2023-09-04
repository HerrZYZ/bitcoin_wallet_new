import sqlite3

class Database:
    def __init__(self, db_file: str = 'wallet.db'):
        self.db_file = db_file
        self.conn = self._connect_db()

    def _connect_db(self):
        return sqlite3.connect(self.db_file)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Wallets(
                id INTEGER PRIMARY KEY,
                name TEXT,
                public_key TEXT,
                private_key TEXT
            )
        ''')
        self.conn.commit()

    def insert_wallet(self, wallet):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO Wallets(name, public_key, private_key)
            VALUES(?,?,?)
        ''', (wallet.name, wallet.wallet.get_key().address, wallet.wallet.get_key().wif))
        self.conn.commit()

    def get_wallet(self, name: str):
        cursor = self.conn.cursor()
        cursor.execute('SELECT public_key, private_key FROM Wallets WHERE name = ?', (name,))
        result = cursor.fetchone()
        if result:
            public_key, private_key = result
            return public_key, private_key
        else:
            return None
