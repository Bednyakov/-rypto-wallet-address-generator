from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

from bitcoin_segwit_gen import generate_bitcoin_address_segwit

def parallel_address_search(start_pattern="", end_pattern=""):
    """
    Запуск генерации адресов параллельно на всех доступных ядрах процессора.
    """
    num_cores = multiprocessing.cpu_count()
    print(f"Используется {num_cores} ядер для параллельного поиска...")

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        # Запускаем задачу на каждом ядре
        futures = [executor.submit(generate_bitcoin_address_segwit, start_pattern, end_pattern) for _ in range(num_cores)]

        for future in as_completed(futures, timeout=1):
            result = future.result()
            if result:
                executor.shutdown(wait=False, cancel_futures=True)
                return result
            
if __name__ == "__main__":
    parallel_address_search(start_pattern="", end_pattern="ema")