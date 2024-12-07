from sys import exit as exit_the_program
import time

from core.menu import select_option, options, enter_patterns, calculators
from core.wallet_info import btc_text, eth_text
from core.search_engine import parallel_address_search


def main():
    while True:
        selected = select_option(options)
        if "Выход" in selected:
                exit_the_program()

        elif "Информация" in selected:
            print(btc_text)
            print(eth_text)
            time.sleep(1)

        for key, value in calculators.items():
            if key in selected:
                print("Учитывайте, чем больше символов в начале или конце адреса, тем дольше будет идти генерация.\n")
                start_pattern, end_pattern = enter_patterns()
                if parallel_address_search(value, start_pattern, end_pattern):
                    exit_the_program()


if __name__ == "__main__":
    main()