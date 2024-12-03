import os
import hashlib
import base58
import requests
from bitcoinlib.keys import HDKey
from bitcoinlib.transactions import Transaction
from bitcoinlib.wallets import Wallet

def generate_bitcoin_address_with_pattern(start_pattern="", end_pattern=""):
    while True:
        # Генерируем случайный приватный ключ
        private_key = HDKey().private_byte.hex()

        # Получаем адрес на основе приватного ключа
        wallet = HDKey.from_private_key(private_key)
        address = wallet.address()

        # Проверяем, начинается ли адрес с заданного шаблона
        if address.startswith(start_pattern) and address.endswith(end_pattern):
            print(f"Найден адрес: {address}")
            print(f"Приватный ключ: {private_key}")
            return address, private_key

def get_balance_bitcoin(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        balance_satoshi = int(response.text)
        balance_btc = balance_satoshi / 1e8
        print(f"Баланс {address}: {balance_btc} BTC")
        return balance_btc
    else:
        print("Ошибка при получении баланса")
        return None

def send_bitcoin(private_key, recipient_address, amount_btc):
    # Создаем временный кошелек с импортом приватного ключа
    wallet = Wallet.create("TempWallet", keys=private_key, network='bitcoin')

    # Создаем транзакцию и подписываем её
    tx = wallet.send_to(recipient_address, amount_btc, fee=1000)
    
    print(f"Транзакция отправлена! Хэш: {tx.txid}")
    wallet.delete()  # Удаляем временный кошелек для безопасности

if __name__ == "__main__":
      generate_bitcoin_address_with_pattern(start_pattern="1abc", end_pattern="xyz")
