import inquirer

from core.wallet_info import btc_text, eth_text, tron_text, litecoin_text
from core.btc import generate_bitcoin_address_p2pkh
from core.btc import generate_bitcoin_address_p2sh
from core.btc import generate_bitcoin_address_segwit
from core.eth import  generate_ethereum_address_with_pattern
from core.tron import generate_tron_address_with_pattern
from core.litecoin import generate_litecoin_address, generate_segwit_litecoin_address

calculators: dict = {"1...": generate_bitcoin_address_p2pkh,
                     "2...": generate_bitcoin_address_p2sh,
                     "bc1q...": generate_bitcoin_address_segwit,
                     "0x...": generate_ethereum_address_with_pattern,
                     "T...": generate_tron_address_with_pattern,
                     "L...": generate_litecoin_address,
                     "ltc1...": generate_segwit_litecoin_address}

def select_option(options, message="Выберите блокчейн и тип кошелька"):
    """
    Отображает интерактивное меню выбора в CLI.

    :param options: Список доступных вариантов
    :param message: Сообщение для пользователя
    :return: Выбранный вариант
    """
    questions = [
        inquirer.List(
            'selection',
            message=message,
            choices=options,
        )
    ]

    answers = inquirer.prompt(questions)
    return answers['selection']


options = ["Bitcoin P2PKH (Pay to Public Key Hash): 1...", "Bitcoin P2SH (Pay to Script Hash): 3...", "Bitcoin Bech32 (SegWit): bc1q...", "Etherium: 0x...", "TRON: T...", "Litecoin: L...", "Litecoin (SegWit): ltc1...", "Информация о типах адресов", "Выход"]


def enter_patterns():
    start_pattern = input("Введите префикс адреса и/или нажмите Enter: ")
    end_pattern = input("Введите суффикс адреса и/или нажмите Enter: ")
    return start_pattern, end_pattern

def addresses_info():
    print(btc_text)
    print(eth_text)
    print(tron_text)
    print(litecoin_text)