import os
import hashlib
import ecdsa
import base58
from Crypto.Hash import RIPEMD160


def ripemd160(data: bytes) -> bytes:
    """
    Вычисляет RIPEMD-160 хэш для данных с использованием pycryptodome.
    """
    h = RIPEMD160.new()
    h.update(data)
    return h.digest()


def generate_bitcoin_address_p2pkh(start_pattern: str="", end_pattern: str=""):
    """
    Генерирует Bitcoin-адрес формата P2PKH и соответствующий приватный ключ.

    :return: Кортеж из приватного ключа (hex) и Bitcoin-адреса (Base58)
    """
    while True:
        # Генерация случайного приватного ключа (32 байта)
        private_key = os.urandom(32)
        
        # Генерация публичного ключа на основе приватного ключа
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        public_key = b'\x04' + vk.to_string()  # Префикс \x04 для некомпрессированного публичного ключа

        # SHA-256 хеш публичного ключа
        sha256_bpk = hashlib.sha256(public_key).digest()

        # RIPEMD-160 хеш SHA-256 хеша публичного ключа
        ripemd160_bpk = ripemd160(sha256_bpk)

        # Добавление сетевого байта (0x00 для основной сети Bitcoin)
        network_byte = b'\x00'
        network_public_key = network_byte + ripemd160_bpk

        # Double SHA-256 для контрольной суммы
        sha256_nbpk = hashlib.sha256(network_public_key).digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk).digest()

        # Добавление первых 4 байт SHA-256 хеша в качестве контрольной суммы
        checksum = sha256_2_nbpk[:4]

        # Добавление контрольной суммы к сетевому публичному ключу
        binary_address = network_public_key + checksum

        # Конвертация бинарного адреса в формат Base58
        address = base58.b58encode(binary_address)
        print(f"Поиск по маске 1{start_pattern}...{end_pattern}: {address.decode()}", end='\r')

        if address.decode().startswith(f"1{start_pattern}") and address.decode().endswith(end_pattern):
            print(f"""\
===============================
Найден адрес: {address.decode()}

Приватный ключ (HEX): {private_key.hex()}
[!] Приватный ключ — это единственный способ получить доступ к вашему кошельку. Безопасное хранение ключа критически важно.
===============================
\n""")
            return address.decode(), private_key.hex()


if __name__ == "__main__":
    private_key, bitcoin_address = generate_bitcoin_address_p2pkh()

