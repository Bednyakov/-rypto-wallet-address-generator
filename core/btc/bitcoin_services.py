
import requests
from bitcoinlib.keys import HDKey
from bitcoinlib.transactions import Transaction, Input, Output
from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service


def get_balance_bitcoin(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        balance_satoshi = int(response.text)
        balance_btc = balance_satoshi / 1e8
        print(f"Баланс {address}: {balance_btc} BTC\n")
        return balance_btc
    else:
        print("Ошибка при получении баланса\n")
        return None

def send_bitcoin(private_key, recipient_address, amount_btc):
    """
    Транзакция с созданием временного кошелька.
    
    Временный кошелек существует только в памяти во время выполнения функции:
    - Приватный ключ хранится внутри объекта Wallet и автоматически удаляется при завершении работы функции.
    - Удаление кошелька (wallet.delete()) предотвращает случайное сохранение ключей в локальном хранилище или кэше.
    """
    # Создаем временный кошелек с импортом приватного ключа
    wallet = Wallet.create("TempWallet", keys=private_key, network='bitcoin')

    # Создаем транзакцию и подписываем её
    tx = wallet.send_to(recipient_address, amount_btc, fee=1000)
    
    print(f"Транзакция отправлена! Хэш: {tx.txid}")
    wallet.delete()  # Удаляем временный кошелек для безопасности

def send_bitcoin_directly(private_key, recipient_address, amount_btc):
    service = Service(network='bitcoin')  # Подключение к сети Bitcoin

    # Получаем адрес и непотраченные выходы (UTXO)
    sender_key = HDKey(private_key)
    sender_address = sender_key.address()
    utxos = service.utxos(sender_address)

    # Создаем транзакцию
    tx = Transaction(network='bitcoin')

    # Добавляем все UTXO в качестве входов
    for utxo in utxos:
        tx.add_input(Input(utxo['txid'], utxo['output_index'], value=utxo['value']))

    # Добавляем выход на адрес получателя
    tx.add_output(Output.to_recipient(recipient_address, amount_btc * 1e8))

    # Подписываем транзакцию приватным ключом
    tx.sign(sender_key)

    # Отправляем транзакцию в сеть
    tx_id = tx.send()
    print(f"Транзакция отправлена! Хэш: {tx_id}")