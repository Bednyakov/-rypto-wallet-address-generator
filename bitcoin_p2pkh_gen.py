import os
import ecdsa
import hashlib
import base58

def generate_bitcoin_address_p2pkh():
    # Генерация случайного приватного ключа
    private_key = os.urandom(32)
    
    # Генерация публичного ключа на основе приватного
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = b'\x04' + vk.to_string()

    # SHA-256 хеш публичного ключа
    sha256_bpk = hashlib.sha256(public_key).digest()

    # RIPEMD-160 хеш SHA-256 хеша публичного ключа
    ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()

    # Добавление сети байта (0x00 для основной сети Bitcoin)
    network_byte = b'\x00'
    network_public_key = network_byte + ripemd160_bpk

    # SHA-256 дважды (Double SHA-256)
    sha256_nbpk = hashlib.sha256(network_public_key).digest()
    sha256_2_nbpk = hashlib.sha256(sha256_nbpk).digest()

    # Добавление первых 4 байт SHA-256 хеша в качестве контрольной суммы
    checksum = sha256_2_nbpk[:4]

    # Добавление контрольной суммы к сетевому публичному ключу
    binary_address = network_public_key + checksum

    # Конвертация бинарного адреса в формат Base58
    address = base58.b58encode(binary_address)
    
    return private_key.hex(), address.decode()

# Пример использования функции
private_key, address = generate_bitcoin_address_p2pkh()
print(f"Приватный ключ: {private_key}")
print(f"Адрес Bitcoin: {address}")
