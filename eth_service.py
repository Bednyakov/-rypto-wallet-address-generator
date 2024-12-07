from eth_account.messages import encode_defunct
from eth_utils import decode_hex
from eth_keys import keys
from web3 import Web3
from typing import Dict
import json


# Подключение к Ethereum ноде
infura_url = "https://mainnet.infura.io/v3/"
web3 = Web3(Web3.HTTPProvider(infura_url))

def check_balance(address):
    """
    Проверка баланса кошелька.
    """
    try:
        balance = web3.eth.get_balance(address)
        print(f"Баланс адреса {address}: {web3.from_wei(balance, 'ether')} ETH\n")
        return balance
    except Exception as e:
        print(f"Для проверки баланса добавьте провайдера в файле .env в директории проекта. Ошибка: {e}")


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



# ABI для стандартных контрактов ERC-20 (нужна для взаимодействия с контрактами)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
]

def check_all_balances(address: str, erc20_contracts: list[str], rpc_url: str) -> Dict[str, float]:
    """
    Проверяет баланс ETH и всех переданных ERC-20 токенов на заданном Ethereum-адресе.

    :param address: Адрес Ethereum (в формате 0x...).
    :param erc20_contracts: Список контрактных адресов токенов ERC-20.
    :param rpc_url: URL RPC для подключения к Ethereum сети.
    :return: Словарь с балансами в формате {"ETH": 1.23, "USDT": 100.5, ...}.
    """
    # Подключение к Ethereum сети через RPC
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Не удалось подключиться к Ethereum RPC.")

    balances = {}

    # Получение баланса ETH
    eth_balance = web3.eth.get_balance(address)
    balances["ETH"] = web3.from_wei(eth_balance, "ether")

    # Проверка балансов ERC-20 токенов
    for contract_address in erc20_contracts:
        try:
            contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI)

            # Получение символа токена
            symbol = contract.functions.symbol().call()

            # Получение числа десятичных знаков
            decimals = contract.functions.decimals().call()

            # Получение баланса
            token_balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
            balances[symbol] = token_balance / (10 ** decimals)
        except Exception as e:
            print(f"Не удалось получить баланс для контракта {contract_address}: {e}")

    return balances