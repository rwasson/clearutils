"""
clearutils: Clear, modular helpers for testing, logging, formatting, and more.

- **Modular helpers** for testing, logging, formatting, and backup.
- Designed for clarity and quick setup—no advanced Python required.
- All helpers are available at the package level for easy import.

Main helpers:
    - logw, currency, percentage, backup_file, assert_log, assert_log_label,
      assert_log_exception, run_test_safely, run_all_tests_randomized, etc.

Quickstart:
    from clearutils import logw, currency, percentage, assert_log

    logw("Welcome to clearutils!")
    print(currency(1234.56))  # -> $1,235

See individual helper docstrings for details:
    help(clearutils.logw)
    help(clearutils.currency)
    help(clearutils.assert_log)
    ...and so on.

For installation, advanced usage, and full documentation, visit the README:
    https://github.com/rwasson/clearutils#readme

"""
__version__ = "0.1.0"
__author__ = "Renya Wasson"
__license__ = "MIT"

# Optional: Import top-level helpers for easy access
from clearutils.src.clearutils.log import setup_logging, logw, logw_traceback, flush_logs
from clearutils.src.clearutils.format import currency, percentage
from clearutils.backup_engine import backup_file
from clearutils.test_engine import (
    assert_log, assert_log_label, assert_log_exception,
    run_test_safely, run_all_tests_randomized
)

# Assign aliases
curr = currency
per = percentage


# Optionally, set __all__ to control what gets imported with "from clearutils import *"
__all__ = [
    "setup_logging", "logw", "logw_traceback", "flush_logs",
    "currency", "percentage",
    "backup_file",
    "assert_log", "assert_log_label", "assert_log_exception",
    "run_test_safely", "run_all_tests_randomized",
]