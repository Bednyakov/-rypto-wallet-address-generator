import inquirer

from core.btc import generate_bitcoin_address_p2pkh
from core.btc import generate_bitcoin_address_p2sh
from core.btc import generate_bitcoin_address_segwit
from core.eth import  generate_ethereum_address_with_pattern
from core.tron import generate_tron_address_with_pattern

calculators: dict = {"P2PKH": generate_bitcoin_address_p2pkh,
                     "P2SH": generate_bitcoin_address_p2sh,
                     "SegWit": generate_bitcoin_address_segwit,
                     "Etherium": generate_ethereum_address_with_pattern,
                     "TRON": generate_tron_address_with_pattern}

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


options = ["Bitcoin P2PKH (Pay to Public Key Hash): 1...", "Bitcoin P2SH (Pay to Script Hash): 3...", "Bitcoin Bech32 (SegWit): bc1q...", "Etherium: 0x...", "TRON: T...", "Информация о типах адресов", "Выход"]


def enter_patterns():
    start_pattern = input("Введите префикс адреса и/или нажмите Enter: ")
    end_pattern = input("Введите суффикс адреса и/или нажмите Enter: ")
    return start_pattern, end_pattern