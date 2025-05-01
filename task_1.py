from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    print("\nПочаток оптимізації друку:")
    print(f"Отримано {len(print_jobs)} завдань")
    print(
        f"Обмеження принтера: максимальний об'єм = {constraints['max_volume']}, максимум предметів = {constraints['max_items']}"
    )

    jobs = [PrintJob(**job) for job in print_jobs]
    printer_constraints = PrinterConstraints(**constraints)

    jobs.sort(key=lambda x: x.priority)
    print("\nЗавдання відсортовані за пріоритетом:")
    for job in jobs:
        print(
            f"ID: {job.id}, Пріоритет: {job.priority}, Об'єм: {job.volume}, Час друку: {job.print_time}"
        )

    print_groups = []
    current_group = []
    current_volume = 0
    total_time = 0

    print("\nФормування груп для друку:")
    for job in jobs:
        print(f"\nОбробка завдання {job.id}:")
        if (
            current_volume + job.volume <= printer_constraints.max_volume
            and len(current_group) < printer_constraints.max_items
        ):
            current_group.append(job)
            current_volume += job.volume
            print(f"Додано до поточної групи. Поточний об'єм: {current_volume}")
        else:
            print(
                f"Неможливо додати до поточної групи (об'єм: {current_volume + job.volume}, кількість: {len(current_group) + 1})"
            )
            if current_group:
                print_groups.append(current_group)
                group_time = max(j.print_time for j in current_group)
                total_time += group_time
                print(f"Збережено групу. Час друку групи: {group_time}")
            current_group = [job]
            current_volume = job.volume
            print(f"Створено нову групу з завданням {job.id}")

    if current_group:
        print_groups.append(current_group)
        group_time = max(j.print_time for j in current_group)
        total_time += group_time
        print(f"\nДодано останню групу. Час друку групи: {group_time}")

    print_order = []
    print(print_groups)
    for group in print_groups:
        print_order.extend([job.id for job in group])

    print("\nРезультат оптимізації:")

    return {"print_order": print_order, "total_time": total_time}


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
        {"id": "M4", "volume": 220, "priority": 1, "print_time": 250},
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150,
        },  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
