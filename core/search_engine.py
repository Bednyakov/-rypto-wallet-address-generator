from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Manager
import multiprocessing

from core.btc import generate_bitcoin_address_segwit
from core.eth import generate_ethereum_address_with_pattern


def wrapped_calculator(calculator, start_pattern, end_pattern, stop_event):
    """
    Обертка для функции генерации адресов.
    Проверяет, был ли установлен сигнал завершения.
    """
    if stop_event.is_set():
        return None
    result = calculator(start_pattern, end_pattern)
    stop_event.set()  # Устанавливаем флаг завершения при нахождении результата
    return result


def parallel_address_search(calculator, start_pattern="", end_pattern=""):
    """
    Запуск генерации адресов параллельно на всех доступных ядрах процессора.
    Завершает все потоки при нахождении результата.
    """
    num_cores = multiprocessing.cpu_count()
    print(f"\nИспользуется {num_cores} ядер для параллельного поиска...\n")

    # Разделяемый объект для определения завершения поиска
    with Manager() as manager:
        stop_event = manager.Event()

        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            # Передаем обертку как функцию с фиксированными аргументами
            futures = [
                executor.submit(wrapped_calculator, calculator, start_pattern, end_pattern, stop_event)
                for _ in range(num_cores)
            ]

            for future in as_completed(futures):
                result = future.result()
                if result:
                    # Возвращаем результат и автоматически завершаем остальные задачи
                    executor.shutdown(wait=False)
                    return result


            
if __name__ == "__main__":
    parallel_address_search(generate_ethereum_address_with_pattern, start_pattern="E4", end_pattern="e")