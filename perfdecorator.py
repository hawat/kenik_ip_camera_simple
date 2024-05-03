import time
import functools
import logging

def time_execution(func):
    @functools.wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # High-precision timing
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger = logging.getLogger(__name__)
        logger.info(f"{func.__name__}() execution time: {elapsed_time:.6f} seconds")
        return result
    return wrapper
