import os
import hashlib
import base58
from bitcoinlib.keys import HDKey

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

if __name__ == "__main__":
      generate_bitcoin_address_with_pattern(start_pattern="1abc", end_pattern="xyz")
