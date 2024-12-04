import os
import requests
from bitcoinlib.keys import HDKey
from bitcoinlib.transactions import Transaction, Input, Output
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service


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
        print(address)

        # Проверяем, начинается ли адрес с заданного шаблона
        if address.startswith(f"bc1q{start_pattern}") and address.endswith(end_pattern):
            print(f"Найден адрес: {address}")
            print(f"Приватный ключ (HEX): {private_key_bytes.hex()}")
            return address, private_key_bytes.hex()
        

def parallel_address_search(start_pattern="", end_pattern=""):
    """
    Запуск генерации адресов параллельно на всех доступных ядрах процессора.
    """
    num_cores = multiprocessing.cpu_count()  # Количество доступных ядер
    print(f"Используется {num_cores} ядер для параллельного поиска...")

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Запускаем задачу на каждом ядре
        futures = [executor.submit(generate_bitcoin_address_segwit, start_pattern, end_pattern) for _ in range(num_cores)]

        # Ждем завершения любой из задач
        for future in as_completed(futures):
            if future.result():
                # Если одна из задач завершилась успешно, отменяем остальные
                executor.shutdown(wait=False, cancel_futures=True)
                print("Адрес найден!")
                return future.result()


def get_balance_bitcoin(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        balance_satoshi = int(response.text)
        balance_btc = balance_satoshi / 1e8
        print(f"Баланс {address}: {balance_btc} BTC")
        return balance_btc
    else:
        print("Ошибка при получении баланса")
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

if __name__ == "__main__":
    result = parallel_address_search(start_pattern="", end_pattern="artem")
    if result:
        address, private_key = result
    print(f"Найденный адрес: {address}")
    print(f"Приватный ключ: {private_key}")
#   address, private_key = generate_bitcoin_address_segwit(start_pattern="", end_pattern="artem")
    get_balance_bitcoin(address)
