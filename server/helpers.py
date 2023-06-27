from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from web3 import Web3

from settings.app import Transaction
w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/0b09c1902b2f4811b0b6e964e9e604d8"))


def generate_wallet():
    # Generate english mnemonic words
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)

    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(mnemonic=MNEMONIC, language="english")
    bip44_hdwallet.clean_derivation()

    return bip44_hdwallet


def send_transaction(wallet, recipient_address, amount_eth):
    w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/0b09c1902b2f4811b0b6e964e9e604d8"))

    sender_address = wallet.address
    nonce = w3.eth.get_transaction_count(sender_address)

    tx_data = {
        "nonce": nonce,
        "to": recipient_address,
        "value": w3.to_wei(amount_eth, "ether"),
        "gas": 21000,
        "gasPrice": w3.to_wei(50, "gwei"),
    }

    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=wallet.private_key)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    transaction = Transaction(hash=tx_hash, currency='ETH', amount=amount_eth)
    transaction.insert()
    print(f"Transaction sent. Hash: {tx_hash.hex()}")

    wallet.bip44_hdwallet.clean_derivation()
