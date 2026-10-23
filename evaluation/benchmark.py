"""
benchmark.py
==============
Simple wall-clock benchmarking utility for measuring pipeline stage
performance, useful for capacity planning before production deployment.
"""

import time
import logging
from contextlib import contextmanager

logger = logging.getLogger("ai_interview_analyzer.benchmark")


@contextmanager
def timed_stage(stage_name: str, results: dict = None):
    """
    Context manager that measures elapsed wall-clock time for a code block.

    Usage:
        results = {}
        with timed_stage("transcription", results):
            do_work()
        print(results["transcription"])
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = round(time.perf_counter() - start, 4)
        logger.info("Stage '%s' took %.4fs", stage_name, elapsed)
        if results is not None:
            results[stage_name] = elapsed


def benchmark_pipeline_stages(stage_callables: dict) -> dict:
    """
    Args:
        stage_callables: dict mapping stage name -> zero-arg callable to run.

    Returns:
        dict mapping stage name -> elapsed seconds.
    """
    results = {}
    for name, fn in stage_callables.items():
        with timed_stage(name, results):
            fn()
    return results
