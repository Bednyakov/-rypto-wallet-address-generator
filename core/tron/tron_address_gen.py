import os
from tronpy.keys import PrivateKey

def generate_tron_address_with_pattern(start_pattern="", end_pattern=""):
    """
    Генерирует TRON-адрес с заданными паттернами в начале и конце.

    :param start_pattern: Паттерн в начале адреса (без учета 'T')
    :param end_pattern: Паттерн в конце адреса
    :return: Кортеж (адрес, приватный ключ)
    """
    while True:
        private_key_bytes = os.urandom(32)
        private_key = PrivateKey(private_key_bytes)
        

        address = private_key.public_key.to_base58check_address()
        

        if (address[1:].startswith(start_pattern) and address.endswith(end_pattern)):
            print(f"===============================\n"
                  f"Найден адрес: {address}\n"
                  f"Приватный ключ: {private_key}\n"
                  f"[!] Сохраните приватный ключ, он нужен для доступа к кошельку.\n"
                  f"===============================\n")
            return address, private_key


        print(f"Поиск адреса с паттерном T{start_pattern}...{end_pattern}: {address}", end='\r')

if __name__ == "__main__":
    address, private_key = generate_tron_address_with_pattern("abc", "xyz")
