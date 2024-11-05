from web3 import Web3
import time
import os
import random
from dotenv import load_dotenv
from colorama import Fore, Style, init
from config import CHAIN_PROVIDER_URL  # Impor URL provider dari config.py

init(autoreset=True)

CROSS_MARK = Fore.RED + "❌" + Style.RESET_ALL

load_dotenv()

# Gunakan URL provider dari config.py
web3 = Web3(Web3.HTTPProvider(CHAIN_PROVIDER_URL))

if web3.is_connected():
    print(Fore.GREEN + "Terkoneksi dengan jaringan Ethereum")
else:
    print(Fore.RED + f"Gagal terhubung ke jaringan Ethereum {CROSS_MARK}")
    raise Exception("Gagal terhubung ke jaringan Ethereum")

# Pastikan sender_address dalam format checksum
sender_address = Web3.to_checksum_address(os.getenv('SENDER_ADDRESS'))
private_key = os.getenv('PRIVATE_KEY')

if not sender_address or not private_key:
    raise Exception(f"{CROSS_MARK} Harap isi SENDER_ADDRESS dan PRIVATE_KEY di file .env")

def get_balance(address):
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')

def get_nonce():
    return web3.eth.get_transaction_count(sender_address)

def get_gas_price():
    return web3.eth.gas_price

def send_transaction(receiver_address, amount, gas_price):
    nonce = get_nonce()
    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': 1301
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.CYAN + f"Transaksi berhasil ke {receiver_address}")
    except Exception as e:
        print(Fore.RED + f"Gagal mengirim transaksi: {str(e)} {CROSS_MARK}")

# Minta jumlah transaksi dari pengguna
try:
    num_transactions = int(input("Masukkan jumlah transaksi yang ingin dilakukan: "))
except ValueError:
    print(Fore.RED + "Input tidak valid. Masukkan angka.")
    raise SystemExit(1)

for i in range(num_transactions):
    # Pastikan receiver dalam format checksum
    receiver = Web3.to_checksum_address('0x' + ''.join(random.choices('0123456789abcdef', k=40)))
    random_amount = random.uniform(0.000000001, 0.00000002)
    gas_price = get_gas_price()
    send_transaction(receiver, random_amount, gas_price)
    time.sleep(3)  # jeda 3 detik sebelum transaksi berikutnya

print(Fore.GREEN + f"Jumlah transaksi yang diminta ({num_transactions}) telah selesai dilakukan.")
