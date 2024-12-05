from eth_keys import keys
from eth_account.messages import encode_defunct
from eth_utils import decode_hex
from web3 import Web3
import os

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
            check_balance(address)
            return address, private_key



# Подключаемся к провайдеру (например, Infura)
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

def check_balance(address):
    """
    Проверка баланса кошелька.
    """
    balance = web3.eth.get_balance(address)
    print(f"Баланс адреса {address}: {web3.from_wei(balance, 'ether')} ETH\n")
    return balance


def send_ether(private_key, to_address, amount_in_ether):
    """
    Отправка транзакции с кошелька.
    """
    # Получаем адрес отправителя из приватного ключа
    sender_address = keys.PrivateKey(decode_hex(private_key)).public_key.to_checksum_address()

    # Создаем транзакцию
    transaction = {
        'to': to_address,
        'value': web3.to_wei(amount_in_ether, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('30', 'gwei'),
        'nonce': web3.eth.getTransactionCount(sender_address),
        'chainId': 1  # Mainnet
    }

    # Подписываем транзакцию приватным ключом
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Отправляем транзакцию
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"Транзакция отправлена! Хэш транзакции: {web3.to_hex(tx_hash)}")

def sign_message(private_key, message):
    """
    Подписание сообщений
    """
    message = encode_defunct(text=message)
    signed_message = web3.eth.account.sign_message(message, private_key)
    print(f"Подписанное сообщение: {signed_message.signature.hex()}")
    return signed_message



if __name__ == "__main__":

    # Проверяем баланс адреса
    address, private_key = generate_ethereum_address_with_pattern("a", "z")
    check_balance(address)

    # # Пример отправки 0.01 ETH
    # recipient_address = "0xАдресПолучателя"
    # send_ether(private_key.to_hex(), recipient_address, 0.01)

    # # Подпишем сообщение
    # sign_message(private_key.to_hex(), "Я подтверждаю владение этим адресом!")
