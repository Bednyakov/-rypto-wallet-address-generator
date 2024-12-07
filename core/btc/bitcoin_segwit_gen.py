import os
from bitcoinlib.keys import HDKey


def generate_bitcoin_address_segwit(start_pattern="", end_pattern=""):
    """
    Генерация сегментированного кошелька Native SegWit (Bech32): 
    Эти адреса представляют собой более эффективную версию, 
    которая использует меньше данных для транзакций 
    и имеет более низкие комиссии по сравнению 
    с более старыми форматами.
    Адреса SegWit начинаются с "bc1q"
    """
    while True:
        # Генерируем случайный приватный ключ
        private_key_bytes = os.urandom(32)  # Генерация 32 байт для приватного ключа
        wallet_key = HDKey(private_key_bytes)
        # wallet_key = HDKey.from_private_key(private_key_bytes, network='bitcoin')

        # Получаем адрес на основе приватного ключа
        address = wallet_key.address()
        print(f"Поиск по маске bc1q{start_pattern}...{end_pattern}: {address}", end='\r')

        # Проверяем, начинается ли адрес с заданного шаблона
        if address.startswith(f"bc1q{start_pattern}") and address.endswith(end_pattern):
            print(f"""\
===============================
Найден адрес: {address}

Приватный ключ (HEX): {private_key_bytes.hex()}
[!] Приватный ключ — это единственный способ получить доступ к вашему кошельку. Безопасное хранение ключа критически важно.
===============================
\n""")

            return address, private_key_bytes.hex()
        

if __name__ == "__main__":
    generate_bitcoin_address_segwit()
