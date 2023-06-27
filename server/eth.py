from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from web3 import Web3
from flask_restful import Resource

from settings.app import Wallet, Transaction
from server.helpers import generate_wallet, send_transaction

w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/0b09c1902b2f4811b0b6e964e9e604d8"))

bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)


class GenerateWalletResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        print(user_id)
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if wallet:
            return {'message': 'Wallet already generated for the user.'}, 400

        # Generate wallet
        bip44_hdwallet = generate_wallet()

        bip44_derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=0
        )
        bip44_hdwallet.from_path(path=bip44_derivation)
        address = bip44_hdwallet.address()
        private_key = bip44_hdwallet.private_key()

        wallet = Wallet(address=address, private_key=private_key, user_id=user_id)
        wallet.insert()

        return {'message': 'Wallet generated successfully.'}, 201


class TransactionResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        recipient_address = data.get('recipient_address')
        amount_eth = data.get('amount_eth')

        user_id = get_jwt_identity()

        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return {'message': 'Wallet not found for the user.'}, 404

        # Send transaction
        send_transaction(wallet, recipient_address, amount_eth)

        return {'message': 'Transaction sent successfully.'}, 200


class TransactionFilterResource(Resource):
    def get(self):
        data = request.get_json()
        currency = data.get('currency')
        amount = data.get('amount')
        tx_hash = data.get('tx_hash')
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)

        transactions = Transaction.get_transactions(currency=currency, amount=amount, tx_hash=tx_hash,
                                                    page=page, per_page=per_page)

        return {'transactions': transactions}, 200
