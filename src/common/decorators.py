import time
import logging
import functools

logger = logging.getLogger(__name__)

def measure_time(step_name: str):
    def decorator(func):
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()

            try:
                result = func(*args, **kwargs)

                elapsed = time.perf_counter() - start

                logger.info(
                    "event=pipeline_step step=%s function=%s duration_seconds=%.2f",
                    step_name,
                    func.__name__,
                    elapsed
                )

                return result

            except Exception:
                elapsed = time.perf_counter() - start

                logger.exception(
                    "event=pipeline_step step=%s function=%s duration_seconds=%.2f",
                    step_name,
                    func.__name__,
                    elapsed
                )
                raise
        
        return wrapper
    
    return decorator