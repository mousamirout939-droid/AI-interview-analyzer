"""
performance.py
=================
Lightweight system/application performance snapshot utilities (memory
usage, process uptime) exposed on an internal health/metrics endpoint.
"""

import os
import time
import logging

logger = logging.getLogger("ai_interview_analyzer.performance")

_PROCESS_START_TIME = time.time()


def get_uptime_seconds() -> float:
    return round(time.time() - _PROCESS_START_TIME, 2)


def get_memory_usage_mb() -> float:
    """Return current process RSS memory usage in MB (best-effort, no psutil dependency)."""
    try:
        with open(f"/proc/{os.getpid()}/status", "r") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    kb = int(line.split()[1])
                    return round(kb / 1024, 2)
    except Exception:
        pass
    return 0.0


def get_performance_snapshot() -> dict:
    return {
        "uptime_seconds": get_uptime_seconds(),
        "memory_usage_mb": get_memory_usage_mb(),
    }
