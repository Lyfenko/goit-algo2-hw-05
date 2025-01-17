import time
import random
from hyperloglog import HyperLogLog


def load_data(file_path):
    ip_addresses = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) > 0 and validate_ip(parts[0]):
                    ip_addresses.append(parts[0])
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
    return ip_addresses


def validate_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            return False
    return True


def exact_count(ip_addresses):
    unique_ips = set(ip_addresses)
    return len(unique_ips)


def hyperloglog_count(ip_addresses, error_rate=0.01):
    hll = HyperLogLog(error_rate)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


def compare_methods(ip_addresses):
    print("\nПорівняння продуктивності:")

    start_time = time.time()
    exact_result = exact_count(ip_addresses)
    exact_time = time.time() - start_time

    start_time = time.time()
    hll_result = hyperloglog_count(ip_addresses)
    hll_time = time.time() - start_time

    print(f"{'Метод':<20}{'Унікальні елементи':<25}{'Час виконання (сек.)':<20}")
    print(f"{'-' * 65}")
    print(f"{'Точний підрахунок':<20}{exact_result:<25}{exact_time:<20.5f}")
    print(f"{'HyperLogLog':<20}{hll_result:<25}{hll_time:<20.5f}")


if __name__ == "__main__":
    test_data_file = "lms-stage-access.log"
    try:
        ip_addresses = load_data(test_data_file)
        if not ip_addresses:
            raise ValueError("Дані для тестування відсутні.")
    except ValueError:
        print("Генерація випадкових даних для тестування.")
        ip_addresses = [f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}" for _ in range(100000)]

    compare_methods(ip_addresses)
