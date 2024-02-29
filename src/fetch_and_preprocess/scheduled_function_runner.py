import schedule
import time
from datetime import datetime
from functools import partial
from typing import Callable, Any


def check_and_run_function(function: Callable, start_hour: int) -> None:
    """
    Checks the current time and runs the given function if the hour matches the specified start hour.

    Args:
        function: The function to be executed.
        start_hour: The hour at which the function should be executed.
    """
    current_time = datetime.now()
    if current_time.hour == start_hour and current_time.minute < 60:
        function()


def start(start_hour: int, function: Callable, *args: Any, **kwargs: Any) -> None:
    """
    Runs the function every minute starting at the specified hour.

    Args:
        start_hour: The hour at which to start running the function.
        function: The function to be executed for one hour with one minute pause.
        *args: Positional arguments to pass to the function.
        **kwargs: Key-value arguments to pass to the function.
    """
    func_with_args = partial(function, *args, **kwargs)

    schedule.every().minute.do(check_and_run_function, function=func_with_args, start_hour=start_hour)

    while True:
        schedule.run_pending()
        time.sleep(1)
