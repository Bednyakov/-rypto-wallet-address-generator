import hashlib
import base58
import random
from Crypto.Hash import RIPEMD160


def generate_litecoin_address(start: str, end: str) -> tuple[str, str]:
    """
    Генерирует адрес Litecoin, начинающийся с `start` и заканчивающийся на `end`,
    а также возвращает соответствующий приватный ключ.
    
    :param start: Начальная строка адреса (например, "L")
    :param end: Конечная строка адреса
    :return: Кортеж, содержащий адрес Litecoin и приватный ключ (в формате hex)
    """
    # if not start.startswith("L"):
    #     raise ValueError("Litecoin адрес должен начинаться с 'L'.")

    while True:
        # Генерация случайного приватного ключа
        private_key = random.randbytes(32)
        private_key_hex = private_key.hex()

        # SHA256 от приватного ключа для создания публичного ключа (упрощенно)
        public_key = hashlib.sha256(private_key).digest()

        # RIPEMD-160 хэш публичного ключа
        ripemd160 = RIPEMD160.new()
        ripemd160.update(public_key)
        public_key_hash = ripemd160.digest()

        # Добавляем префикс Litecoin (0x30 для P2PKH адресов)
        prefix = b"\x30"
        extended_public_key_hash = prefix + public_key_hash

        # Вычисление контрольной суммы (SHA256 дважды, затем первые 4 байта)
        checksum = hashlib.sha256(hashlib.sha256(extended_public_key_hash).digest()).digest()[:4]

        # Итоговый бинарный адрес
        binary_address = extended_public_key_hash + checksum

        # Кодируем адрес в Base58Check
        address = base58.b58encode(binary_address).decode()
        print(f"Поиск по маске L{start}...{end}: {address}", end='\r')

        # Проверяем соответствие началу и концу
        if address.startswith(f"L{start}") and address.endswith(end):
            print(f"""\
===============================
Найден адрес: {address}

Приватный ключ (HEX): {private_key_hex}
[!] Приватный ключ — это единственный способ получить доступ к вашему кошельку. Безопасное хранение ключа критически важно.
===============================
\n""")
            return address, private_key_hex


if __name__ == "__main__":
    start_pattern = ""
    end_pattern = "1A"
    address, private_key = generate_litecoin_address(start_pattern, end_pattern)

