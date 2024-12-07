import os
import ecdsa
import hashlib
import base58
from Crypto.Hash import RIPEMD160


def ripemd160(data: bytes) -> bytes:
    """
    Вычисляет RIPEMD-160 хэш для данных с использованием pycryptodome.
    """
    h = RIPEMD160.new()
    h.update(data)
    return h.digest()


def generate_bitcoin_address_p2sh(start_pattern: str = "", end_pattern: str = ""):
    """
    Генерирует Bitcoin-адрес формата P2SH и соответствующий приватный ключ.

    :param start_pattern: Опциональный начальный паттерн адреса.
    :param end_pattern: Опциональный конечный паттерн адреса.
    :return: Кортеж из приватного ключа (hex) и Bitcoin-адреса (Base58).
    """
    while True:
        # Генерация случайного приватного ключа
        private_key = os.urandom(32)

        # Генерация публичного ключа на основе приватного
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        public_key = b'\x04' + vk.to_string()

        # SHA-256 хеш публичного ключа
        sha256_bpk = hashlib.sha256(public_key).digest()

        # RIPEMD-160 хеш SHA-256 хеша публичного ключа
        ripemd160_bpk = ripemd160(sha256_bpk)

        # Создание Redeem Script: P2PKH скрипт
        redeem_script = b'\x00\x14' + ripemd160_bpk  # OP_0 <20-byte RIPEMD-160 hash>

        # SHA-256 хеш Redeem Script
        sha256_redeem = hashlib.sha256(redeem_script).digest()

        # RIPEMD-160 хеш SHA-256 хеша Redeem Script
        ripemd160_redeem = ripemd160(sha256_redeem)

        # Добавление сети байта (0x05 для P2SH)
        network_byte = b'\x05'
        network_redeem = network_byte + ripemd160_redeem

        # SHA-256 дважды (Double SHA-256)
        sha256_nbpk = hashlib.sha256(network_redeem).digest()
        sha256_2_nbpk = hashlib.sha256(sha256_nbpk).digest()

        # Добавление первых 4 байт SHA-256 хеша в качестве контрольной суммы
        checksum = sha256_2_nbpk[:4]

        # Добавление контрольной суммы к сетевому публичному ключу
        binary_address = network_redeem + checksum

        # Конвертация бинарного адреса в формат Base58
        address = base58.b58encode(binary_address)
        print(f"Поиск по маске 3{start_pattern}...{end_pattern}: {address.decode()}", end='\r')

        if address.decode().startswith(f"3{start_pattern}") and address.decode().endswith(end_pattern):
            print(f"""\
===============================
Найден адрес: {address.decode()}

Приватный ключ (HEX): {private_key.hex()}
[!] Приватный ключ — это единственный способ получить доступ к вашему кошельку. Безопасное хранение ключа критически важно.
===============================
\n""")
            return address.decode(), private_key.hex()



if __name__ == "__main__":
    address, private_key = generate_bitcoin_address_p2sh()
