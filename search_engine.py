from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

from bitcoin_segwit_gen import generate_bitcoin_address_segwit
from eth_address import generate_ethereum_address_with_pattern

def parallel_address_search(calculator, start_pattern="", end_pattern=""):
    """
    Запуск генерации адресов параллельно на всех доступных ядрах процессора.
    """
    num_cores = multiprocessing.cpu_count()
    print(f"Используется {num_cores} ядер для параллельного поиска...")

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Запускаем задачу на каждом ядре
        futures = [executor.submit(calculator, start_pattern, end_pattern) for _ in range(num_cores)]

        for future in as_completed(futures, timeout=1):
            result = future.result()
            if result:
                executor.shutdown(wait=False, cancel_futures=True)
                return result
            
if __name__ == "__main__":
    parallel_address_search(generate_ethereum_address_with_pattern, start_pattern="E4", end_pattern="e4")