"""
This modules defines some util decorators to handle exeptions and logging options

Contains:
    retry: Retry Function Decorator
"""

import time
from functools import wraps
from logging import Logger
from typing import Any, Callable, List, Optional, Type


def time_logger(
    func: Callable,
    logger: Optional[Logger] = None,
) -> Callable:
    """
    A decorator to log the execution time of a method.

    Args:
        logger (Optional[logging.Logger], optional): Logger
        instance for logging time. Defaults to None.

    Returns:
        Callable: The decorated function with time logging
        functionality added to its capability.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        try:
            t1 = time.time()
            if logger:
                logger.debug("--- %s minutes ---", round(time.time() - t1 / 60, 2))
            return func(self, *args, **kwargs)
        except Exception as exc:
            if logger:
                logger.exception(exc)
                logger.debug(
                    "--- Failed in %s minutes ---", round(time.time() - t1 / 60, 2)
                )
            raise exc

    return wrapper


def retry(
    exceptions: List[Type[Exception]],
    tries: int = 4,
    delay: int = 3,
    backoff: int = 2,
    logger: Optional[Logger] = None,
) -> Callable:
    """
    Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    Args:
        exceptions (List[Type[Exception]]): The exception type to check.
        tries (int, optional): retry times. Defaults to 4.
        delay (int, optional): delay of each retry. Defaults to 3.
        backoff (int, optional): time to increment each new delay. Defaults to 2.
        logger (Optional[logging.Logger], optional): Logger instance for logging retries. Defaults to None.

    Returns:
        Callable: The decorated function with retry capability.
    """

    def deco_retry(function: Callable) -> Callable:
        @wraps(function)
        def f_retry(*args: Any, **kwargs: Any) -> Any:
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return function(*args, **kwargs)
                except exceptions as exc:
                    msg = f"{str(exc)}, Retrying in {mdelay} seconds..."
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff

            return function(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def rate_limiter(max_calls: int, sleep_time: int):
    """
    A decorator to limit the rate of function calls.

    Args:
        max_calls (int): Number of calls before the sleep is triggered.
        sleep_time (int): Time in seconds to sleep after max_calls is reached.
    """

    def decorator(func: Callable) -> Callable:
        # This is the counter to keep track of the number of calls
        calls_count = {"count": 0}

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Increment the call count
            calls_count["count"] += 1

            # Call the actual function
            result = func(*args, **kwargs)

            # If the call count reaches the max_calls, reset the counter and sleep
            if calls_count["count"] >= max_calls:
                time.sleep(sleep_time)
                calls_count["count"] = 0

            return result

        return wrapper

    return decorator
