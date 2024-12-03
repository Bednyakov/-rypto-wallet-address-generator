from eth_keys import keys
from eth_utils import decode_hex

import os

def generate_ethereum_address_with_pattern(start_pattern="", end_pattern=""):
    while True:
        # Генерируем случайный приватный ключ
        private_key_bytes = os.urandom(32)
        private_key = keys.PrivateKey(private_key_bytes)

        # Получаем адрес на основе приватного ключа
        address = private_key.public_key.to_checksum_address()

        # Проверяем шаблон начала и конца
        if address[2:].startswith(start_pattern) and address[2:].endswith(end_pattern):
            print(f"Найден адрес: {address}")
            print(f"Приватный ключ: {private_key}")
            return address, private_key

if __name__ == "__main__":
    generate_ethereum_address_with_pattern(start_pattern="abc", end_pattern="xyz")
