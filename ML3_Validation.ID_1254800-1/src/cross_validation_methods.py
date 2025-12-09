import numpy as np
from typing import List, Tuple, Union
from collections import Counter

def my_KFold(X, k: int = 5, shuffle: bool = True, random_state: int = 21) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Реализация K-Fold кросс-валидации.
    
    Параметры:
    ----------
    X : array-like
        Данные для разбиения. Может быть numpy array, list, или любой объект с len()
    k : int, default=5
        Количество фолдов (частей, на которые разбиваются данные)
    shuffle : bool, default=True
        Перемешивать ли индексы перед разбиением
    random_state : int, optional
        Seed для генератора случайных чисел (для воспроизводимости)
    
    Возвращает:
    -----------
    List[Tuple[np.ndarray, np.ndarray]]
        Список из k кортежей, где каждый кортеж содержит:
        - train_indices: индексы для обучения
        - test_indices: индексы для тестирования
    """
    
    # Получаем количество сэмплов
    n_samples = len(X)
    
    if k <= 1:
        raise ValueError(f"k должно быть больше 1, получено k={k}")
    
    if k > n_samples:
        raise ValueError(f"k={k} не может быть больше количества сэмплов n_samples={n_samples}")
    
    # Создаем массив индексов
    indices = np.arange(n_samples)
    
    # Перемешиваем индексы, если нужно
    if shuffle:
        if random_state is not None:
            np.random.seed(random_state)
        np.random.shuffle(indices)
    
    # Вычисляем размер каждого фолда
    fold_sizes = np.full(k, n_samples // k, dtype=int)
    # Распределяем оставшиеся сэмплы по первым фолдам
    fold_sizes[:n_samples % k] += 1
    
    # Список для хранения результатов
    splits = []
    
    # Текущая позиция в массиве индексов
    current = 0
    
    # Создаем границы фолдов
    fold_boundaries = []
    for fold_size in fold_sizes:
        fold_boundaries.append((current, current + fold_size))
        current += fold_size
    
    # Для каждого фолда создаем train и test индексы
    for i in range(k):
        # Текущий фолд используется как test
        test_start, test_end = fold_boundaries[i]
        test_indices = indices[test_start:test_end]
        
        # Все остальные фолды используются как train
        train_indices = np.concatenate([
            indices[start:end] 
            for j, (start, end) in enumerate(fold_boundaries) 
            if j != i
        ])
        
        splits.append((train_indices, test_indices))
    
    return splits


def my_GroupKFold(X, groups, k: int = 5, shuffle: bool = True, random_state: int = 21) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Реализация Grouped K-Fold кросс-валидации.
    
    Гарантирует, что все сэмплы из одной группы попадут либо в train, либо в test,
    но никогда не будут разделены между ними. Это предотвращает утечку данных
    когда у нас есть связанные сэмплы (например, несколько измерений от одного субъекта).
    
    Параметры:
    ----------
    X : array-like
        Данные для разбиения
    groups : array-like
        Метки групп для каждого сэмпла. Должен иметь ту же длину, что и X.
        Сэмплы с одинаковым значением группы всегда будут в одном фолде.
    k : int, default=5
        Количество фолдов
    shuffle : bool, default=True
        Перемешивать ли группы перед разбиением
    random_state : int, optional
        Seed для генератора случайных чисел
    
    Возвращает:
    -----------
    List[Tuple[np.ndarray, np.ndarray]]
        Список из k кортежей (train_indices, test_indices)
    """
    
    n_samples = len(X)
    groups = np.array(groups)
    
    if len(groups) != n_samples:
        raise ValueError(f"Длина groups ({len(groups)}) должна совпадать с длиной X ({n_samples})")
    
    if k <= 1:
        raise ValueError(f"k должно быть больше 1, получено k={k}")
    
    # Получаем уникальные группы
    unique_groups = np.unique(groups)
    n_groups = len(unique_groups)
    
    if k > n_groups:
        raise ValueError(f"k={k} не может быть больше количества уникальных групп n_groups={n_groups}")
    
    # Подсчитываем количество сэмплов в каждой группе
    group_counts = {}
    for group in unique_groups:
        group_counts[group] = np.sum(groups == group)
    
    # Создаем массив групп для разбиения
    groups_array = unique_groups.copy()
    
    # Перемешиваем группы, если нужно
    if shuffle:
        if random_state is not None:
            np.random.seed(random_state)
        np.random.shuffle(groups_array)
    
    # Пытаемся распределить группы по фолдам максимально равномерно
    # по количеству сэмплов (а не по количеству групп)
    fold_groups = [[] for _ in range(k)]
    fold_sample_counts = np.zeros(k, dtype=int)
    
    # Сортируем группы по размеру (от большей к меньшей) для лучшего баланса
    groups_with_counts = [(g, group_counts[g]) for g in groups_array]
    groups_with_counts.sort(key=lambda x: x[1], reverse=True)
    
    # Жадно распределяем группы: каждую группу кладем в фолд с наименьшим
    # текущим количеством сэмплов
    for group, count in groups_with_counts:
        # Находим фолд с минимальным количеством сэмплов
        min_fold_idx = np.argmin(fold_sample_counts)
        fold_groups[min_fold_idx].append(group)
        fold_sample_counts[min_fold_idx] += count
    
    # Создаем splits
    splits = []
    
    for i in range(k):
        # Текущий фолд используется как test
        test_groups = set(fold_groups[i])
        test_mask = np.isin(groups, list(test_groups))
        test_indices = np.where(test_mask)[0]
        
        # Все остальные фолды используются как train
        train_groups = set()
        for j in range(k):
            if j != i:
                train_groups.update(fold_groups[j])
        train_mask = np.isin(groups, list(train_groups))
        train_indices = np.where(train_mask)[0]
        
        splits.append((train_indices, test_indices))
    
    return splits


def my_StratifiedKFold(X, y, k: int = 5, shuffle: bool = True, random_state: int = 21) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Реализация Stratified K-Fold кросс-валидации.
    
    Сохраняет пропорции классов в каждом фолде. Это особенно важно для
    несбалансированных датасетов, где один класс значительно преобладает над другими.
    
    Параметры:
    ----------
    X : array-like
        Данные для разбиения
    y : array-like
        Метки классов для каждого сэмпла. Должен иметь ту же длину, что и X.
    k : int, default=5
        Количество фолдов
    shuffle : bool, default=True
        Перемешивать ли индексы внутри каждого класса перед разбиением
    random_state : int, optional
        Seed для генератора случайных чисел 
    """
    
    n_samples = len(X)
    y = np.array(y)
    
    if len(y) != n_samples:
        raise ValueError(f"Длина y ({len(y)}) должна совпадать с длиной X ({n_samples})")
    
    if k <= 1:
        raise ValueError(f"k должно быть больше 1, получено k={k}")
    
    # Получаем уникальные классы и их количество
    unique_classes = np.unique(y)
    n_classes = len(unique_classes)
    
    # Проверяем, что в каждом классе достаточно сэмплов для k фолдов
    class_counts = Counter(y)
    for cls, count in class_counts.items():
        if count < k:
            raise ValueError(
                f"Класс {cls} имеет только {count} сэмплов, "
                f"что меньше k={k}. Невозможно создать {k} фолдов."
            )
    
    # Инициализируем random state если нужно
    if shuffle and random_state is not None:
        np.random.seed(random_state)
    
    # Для каждого класса получаем его индексы и разбиваем на k частей
    class_fold_indices = {cls: [[] for _ in range(k)] for cls in unique_classes}
    
    for cls in unique_classes:
        # Получаем все индексы этого класса
        cls_indices = np.where(y == cls)[0]
        
        # Перемешиваем индексы класса, если нужно
        if shuffle:
            np.random.shuffle(cls_indices)
        
        # Вычисляем размер каждого фолда для этого класса
        n_samples_cls = len(cls_indices)
        fold_sizes = np.full(k, n_samples_cls // k, dtype=int)
        fold_sizes[:n_samples_cls % k] += 1
        
        # Распределяем индексы по фолдам
        current = 0
        for fold_idx in range(k):
            start = current
            end = current + fold_sizes[fold_idx]
            class_fold_indices[cls][fold_idx] = cls_indices[start:end]
            current = end
    
    # Создаем финальные splits
    splits = []
    
    for i in range(k):
        # Собираем test индексы из i-го фолда каждого класса
        test_indices = []
        for cls in unique_classes:
            test_indices.extend(class_fold_indices[cls][i])
        test_indices = np.array(test_indices)
        
        # Собираем train индексы из всех остальных фолдов
        train_indices = []
        for j in range(k):
            if j != i:
                for cls in unique_classes:
                    train_indices.extend(class_fold_indices[cls][j])
        train_indices = np.array(train_indices)
        
        # Перемешиваем train и test индексы для разнообразия
        if shuffle:
            np.random.shuffle(train_indices)
            np.random.shuffle(test_indices)
        
        splits.append((train_indices, test_indices))
    
    return splits


def my_TimeSeriesSplit(X, dates, k: int = 5) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Реализация Time Series Split кросс-валидации.
    
    Создает k последовательных разбиений данных, где каждое следующее разбиение
    использует больше данных для обучения. Это предотвращает утечку информации
    из будущего в прошлое, что критично для временных рядов.
    
    Важно: train всегда идет ДО test по времени, никогда не после!
    
    Параметры:
    ----------
    X : array-like
        Данные для разбиения
    dates : array-like
        Временные метки для каждого сэмпла. Может быть:
        - datetime объекты
        - строки в формате даты
        - числовые значения (timestamp, индексы)
        Должен иметь ту же длину, что и X.
    k : int, default=5
        Количество разбиений (splits)
    
    Возвращает:
    -----------
    List[Tuple[np.ndarray, np.ndarray]]
        Список из k кортежей (train_indices, test_indices)
    """
    
    n_samples = len(X)
    dates = np.array(dates)
    
    if len(dates) != n_samples:
        raise ValueError(f"Длина dates ({len(dates)}) должна совпадать с длиной X ({n_samples})")
    
    if k <= 1:
        raise ValueError(f"k должно быть больше 1, получено k={k}")
    
    if k >= n_samples:
        raise ValueError(f"k={k} должно быть меньше количества сэмплов n_samples={n_samples}")
    
    # Получаем индексы, отсортированные по датам
    sorted_indices = np.argsort(dates)
    
    # Вычисляем размер test фолда
    # Мы хотим, чтобы каждый test фолд был примерно одинакового размера
    test_size = n_samples // (k + 1)
    
    if test_size < 1:
        raise ValueError(f"Недостаточно данных для создания {k} splits. "
                        f"Нужно минимум {k + 1} сэмплов.")
    
    splits = []
    
    # Создаем k разбиений
    for i in range(k):
        # Вычисляем границы для текущего split
        # Train: от начала до определенной точки
        # Test: следующий блок данных после train
        
        # Конец train данных (включительно)
        train_end = test_size * (i + 1)
        
        # Начало и конец test данных
        test_start = train_end
        test_end = test_start + test_size
        
        # Для последнего split используем все оставшиеся данные
        if i == k - 1:
            test_end = n_samples
        
        # Получаем индексы для train и test
        train_indices = sorted_indices[:train_end]
        test_indices = sorted_indices[test_start:test_end]
        
        splits.append((train_indices, test_indices))
    
    return splits