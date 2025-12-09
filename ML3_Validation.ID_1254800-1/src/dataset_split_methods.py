import numpy as np
import pandas as pd
from datetime import datetime

def _split_by_date(X, y, date_split, date_column, validation_size=None):
    """
    Helper function to split data by date threshold.
    
    Parameters:
    -----------
    X : array-like or pandas DataFrame
        Feature matrix
    y : array-like, optional
        Target vector
    date_split : str or datetime-like
        Date threshold for splitting
    date_column : int or str
        Column index or name containing dates
    validation_size : float, optional
        Ratio of validation set size (0 to 1) for the train set.
    
    Returns:
    --------
    If validation_size is None:
        X_train, X_test, y_train, y_test (if y provided) or X_train, X_test (if y is None)
    Else:
        X_train, X_val, X_test, y_train, y_val, y_test (if y provided) or X_train, X_val, X_test (if y is None)
    """
    
    # Convert date_split to datetime if it's a string
    if isinstance(date_split, str):
        date_split = pd.to_datetime(date_split)
    
    # Check if X is a pandas DataFrame
    is_dataframe = isinstance(X, pd.DataFrame)
    
    # --- 1. Разделение на train (< date_split) и test (>= date_split) ---
    if is_dataframe:
        # Extract dates from DataFrame
        if isinstance(date_column, str):
            dates = pd.to_datetime(X[date_column])
        else:
            dates = pd.to_datetime(X.iloc[:, date_column])
        
        # Create boolean mask
        train_test_mask = dates < date_split
        test_mask = dates >= date_split
        
        # Split data (initial train/test)
        X_train_temp = X[train_test_mask].reset_index(drop=True)
        X_test = X[test_mask].reset_index(drop=True)
        
    else:
        # Convert to numpy array
        X = np.array(X)
        
        # Extract dates column
        dates_col = X[:, date_column] if isinstance(date_column, int) else X[:, date_column]
        
        # Convert dates to datetime
        dates = pd.to_datetime(dates_col)
        
        # Create boolean mask
        train_test_mask = (dates < date_split).values
        test_mask = (dates >= date_split).values
        
        # Split data (initial train/test)
        X_train_temp = X[train_test_mask]
        X_test = X[test_mask]
    
    # Handle y if provided (initial train/test split for y)
    y_train_temp = None
    y_test = None
    if y is not None:
        y = np.array(y) if not isinstance(y, np.ndarray) else y
        y_train_temp = y[train_test_mask]
        y_test = y[test_mask]

    # --- 2. Разделение train на train и val (если validation_size предоставлен) ---
    if validation_size is not None:
        if not 0 < validation_size < 1:
            raise ValueError("validation_size must be between 0 and 1")
            
        n_train_temp = len(X_train_temp)
        
        # Считаем, сколько образцов пойдет в val set. 
        # Это validation_size от исходного train set (того, что меньше date_split)
        n_val = int(n_train_temp * validation_size) 
        
        if n_val == 0 and n_train_temp > 0:
             # Небольшой набор данных может привести к n_val = 0
             print("Warning: validation_size resulted in 0 samples for the validation set. Check the size of your training data.")

        # Оставляем n_val последних образцов для валидации, 
        # остальные (более ранние) для обучения.
        # Это имитирует временной срез внутри обучающей выборки.
        
        # Индексы для валидационного набора: n_val самых новых образцов в X_train_temp
        val_indices = np.arange(n_train_temp - n_val, n_train_temp)
        # Индексы для окончательного обучающего набора: все, кроме val_indices
        train_indices = np.arange(0, n_train_temp - n_val)
        
        # Разделяем X_train_temp
        X_train = X_train_temp[train_indices]
        X_val = X_train_temp[val_indices]
        
        # Разделяем y_train_temp
        if y is not None:
            y_train = y_train_temp[train_indices]
            y_val = y_train_temp[val_indices]
            return X_train, X_val, X_test, y_train, y_val, y_test
        else:
            return X_train, X_val, X_test
    
    # --- 3. Возврат без валидационного набора (если validation_size is None) ---
    else:
        # Если валидационный набор не требуется, возвращаем исходные train/test сплиты
        X_train = X_train_temp
        
        if y is not None:
            y_train = y_train_temp
            return X_train, X_test, y_train, y_test
        else:
            return X_train, X_test


def my_train_test_split(X, y=None, test_size=0.2, validation_size=None, random_state=None, date_split=None, date_column=None):
    """
    Split data into training, validation, and test sets randomly or by date.
    
    Parameters:
    -----------
    X : array-like, shape (n_samples, n_features)
        Feature matrix
    y : array-like, shape (n_samples,), optional
        Target vector
    test_size : float, default=0.2
        Ratio of test set size (0 to 1). Used only for random split.
    validation_size : float, optional
        Ratio of validation set size (0 to 1).
        Used only for random split.
    random_state : int, optional
        Seed for random number generator for reproducibility. Used only for random split.
    date_split : str or datetime-like, optional
        Date threshold for splitting data.
        Samples with date < date_split go to train, samples with date >= date_split go to test.
    date_column : int or str, optional
        Column index (int) or column name (str) containing dates in X.
        Required if date_split is provided. If X is a pandas DataFrame, can use column name.
    
    Returns:
    --------
    If date_split is provided (date-based split):
        If y is provided: X_train, X_test, y_train, y_test
        If y is None: X_train, X_test
    
    If date_split is None (random split):
        If validation_size is None:
            If y is provided: X_train, X_test, y_train, y_test
            If y is None: X_train, X_test
        
        If validation_size is provided:
            If y is provided: X_train, X_val, X_test, y_train, y_val, y_test
            If y is None: X_train, X_val, X_test
    """

    # Check if date_split is provided
    if date_split is not None:
        if date_column is None:
            raise ValueError("date_column must be provided when date_split is specified")
        
        # Проверка validation_size (только для date-based split, если не None)
        if validation_size is not None and not 0 < validation_size < 1:
            raise ValueError("validation_size must be between 0 and 1")
            
        # Perform date-based split
        return _split_by_date(X, y, date_split, date_column, validation_size) 
    
    # Continue with random split logic... (ОСТАЛЬНОЙ КОД БЕЗ ИЗМЕНЕНИЙ)
    # Validate test_size parameter
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    
    # Validate validation_size parameter if provided
    if validation_size is not None:
        if not 0 < validation_size < 1:
            raise ValueError("validation_size must be between 0 and 1")
        if test_size + validation_size >= 1:
            raise ValueError("test_size + validation_size must be less than 1")
    
    # Convert to numpy arrays if needed
    X = np.array(X)
    if y is not None:
        y = np.array(y)
        
        # Check if X and y have the same number of samples
        if len(X) != len(y):
            raise ValueError("X and y must have the same number of samples")
    
    # Get number of samples
    n_samples = len(X)
    
    # Calculate split sizes
    n_test = int(n_samples * test_size)
    
    if validation_size is not None:
        n_val = int(n_samples * validation_size)
        n_train = n_samples - n_test - n_val
    else:
        n_train = n_samples - n_test
        n_val = 0
    
    # Set random seed if provided
    if random_state is not None:
        np.random.seed(random_state)
    
    # Generate random indices
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    
    # Split indices
    test_indices = indices[:n_test]
    
    if validation_size is not None:
        val_indices = indices[n_test:n_test + n_val]
        train_indices = indices[n_test + n_val:]
    else:
        train_indices = indices[n_test:]
    
    # Split data
    X_train = X[train_indices]
    X_test = X[test_indices]
    
    if validation_size is not None:
        X_val = X[val_indices]
    
    # Return with or without y, and with or without validation set
    if y is not None:
        y_train = y[train_indices]
        y_test = y[test_indices]
        
        if validation_size is not None:
            y_val = y[val_indices]
            return X_train, X_val, X_test, y_train, y_val, y_test
        else:
            return X_train, X_test, y_train, y_test
    else:
        if validation_size is not None:
            return X_train, X_val, X_test
        else:
            return X_train, X_test