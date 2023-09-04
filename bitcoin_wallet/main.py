from flask import Flask, render_template, request, redirect, url_for
from wallet import Wallet
from transaction import Transaction
from blockchain import Blockchain
from database import Database

app = Flask(__name__)
blockchain = Blockchain()
database = Database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/wallet', methods=['POST', 'GET'])
def wallet():
    if request.method == 'POST':
        name = request.form.get('name')
        wallet = Wallet(name)
        wallet.generate_keys()
        database.insert_wallet(wallet)
        return redirect(url_for('home'))
    return render_template('wallet.html')

@app.route('/send', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        sender = request.form.get('sender')
        recipient = request.form.get('recipient')
        amount = int(request.form.get('amount'))
        sender_wallet = Wallet(sender)
        sender_wallet.load_keys()
        transaction = Transaction(sender_wallet.wallet.get_key().address, recipient, amount)
        tx = transaction.create_transaction(sender_wallet.wallet)
        blockchain.add_transaction(tx)
        return redirect(url_for('home'))
    return render_template('send.html')

@app.route('/receive', methods=['POST', 'GET'])
def receive():
    if request.method == 'POST':
        name = request.form.get('name')
        wallet = Wallet(name)
        wallet.load_keys()
        balance = wallet.get_balance()
        return render_template('receive.html', balance=balance)
    return render_template('receive.html')

@app.route('/mine', methods=['POST'])
def mine():
    blockchain.mine_block()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
