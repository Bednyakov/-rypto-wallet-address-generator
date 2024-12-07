import inquirer

def select_option(options, message="Выберите блокчейн адреса кошелька"):
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

# Пример использования
if __name__ == "__main__":
    options = ["Bitcoin P2PKH (Pay to Public Key Hash): 1...", "Bitcoin P2SH (Pay to Script Hash): 3...", "Bitcoin Bech32 (SegWit): bc1q..."]
    selected = select_option(options)
    print(f"Вы выбрали: {selected}")

