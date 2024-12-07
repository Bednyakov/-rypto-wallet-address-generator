from eth_keys import keys
from dotenv import load_dotenv
import os

from eth_service import check_balance, send_ether, sign_message, check_all_balances
from eth_contracts import token_contracts

load_dotenv()
rpc_url = os.getenv("RPC_URL")

def generate_ethereum_address_with_pattern(start_pattern="", end_pattern=""):
    while True:
        # Генерируем случайный приватный ключ
        private_key_bytes = os.urandom(32)
        private_key = keys.PrivateKey(private_key_bytes)

        # Получаем адрес на основе приватного ключа
        address = private_key.public_key.to_checksum_address()
        print(address, end='\r')

        # Проверяем шаблон начала и конца
        if address[2:].startswith(start_pattern) and address[2:].endswith(end_pattern):
            print(f"Найден адрес: {address}")
            print(f"Приватный ключ: {private_key}")
            return address, private_key


def all_balances(eth_address: str, token_contracts: list, rpc_url: str) -> None:

    balances = check_all_balances(eth_address, token_contracts, rpc_url)
    for token, balance in balances.items():
        print(f"{token}: {balance}")


def calculator(start_pattern: str, end_pattern: str):
    address, private_key = generate_ethereum_address_with_pattern()
    if rpc_url:
        all_balances(eth_address=address, token_contracts=token_contracts, rpc_url=rpc_url)
        return address, private_key
    print("Для проверки баланса добавьте в .env провайдера в виде: RPC_URL=https://mainnet.infura.io/v3/... ")
    return address, private_key


if __name__ == "__main__":
    calculator("", "")


    # Проверяем баланс адреса
    # address, private_key = generate_ethereum_address_with_pattern("", "")

    # # Пример отправки 0.01 ETH
    # recipient_address = "0xАдресПолучателя"
    # send_ether(private_key.to_hex(), recipient_address, 0.01)
    # sign_message(private_key.to_hex(), "Я подтверждаю владение этим адресом!")


