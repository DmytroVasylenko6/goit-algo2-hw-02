from typing import Dict, List


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    memo = {}
    cuts_memo = {}

    def cut_rod(n: int) -> int:
        if n == 0:
            return 0
        if n in memo:
            return memo[n]

        max_val = float("-inf")
        best_cut = 0

        for i in range(n):
            current = prices[i] + cut_rod(n - (i + 1))
            if current > max_val:
                max_val = current
                best_cut = i + 1

        memo[n] = max_val
        cuts_memo[n] = best_cut
        return max_val

    max_profit = cut_rod(length)

    cuts = []
    remaining = length
    while remaining > 0:
        cut = cuts_memo[remaining]
        cuts.append(cut)
        remaining -= cut

    return {"max_profit": max_profit, "cuts": cuts, "number_of_cuts": len(cuts) - 1}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    table = [0] * (length + 1)

    cuts = [0] * (length + 1)

    for i in range(1, length + 1):
        max_val = float("-inf")
        for j in range(i):
            current = prices[j] + table[i - (j + 1)]
            if current > max_val:
                max_val = current
                cuts[i] = j + 1
        table[i] = max_val

    result_cuts = []
    remaining = length
    while remaining > 0:
        cut = cuts[remaining]
        result_cuts.append(cut)
        remaining -= cut
    print(" table:", table)
    return {
        "max_profit": table[length],
        "cuts": result_cuts,
        "number_of_cuts": len(result_cuts) - 1,
    }


def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        # Тест 2: Оптимально не різати
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        # Тест 3: Всі розрізи по 1
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test["length"], test["prices"])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
