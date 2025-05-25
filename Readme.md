# clearutils

Clear, modular Python helpers for beautiful logging, testing, formatting, and more—without the boilerplate.

**Why Use clearutils?**
- **Modular helpers:** Plug-and-play testing, logging, and formatting—no setup required.
- **Short main script:** Keep your code clean and focused—just set options and run.
- **Clear results:** Well-formatted, non-interleaved logs and summary tables show what works, what fails, and include tracebacks for quick debugging.

---

### How clearutils organizes your tests and logs

- **Two log types for every test run:**
    - **Doc log:** Displays all tests (in the order you wrote them), including section labels, expected/actual results, and a summary table for full documentation.
    - **Run log:** Only shows failed tests (in random order, to catch order dependencies), along with tracebacks and debug info.

- **Comprehensive summary tables:** Track passes, failures, intentional and unintentional warnings (user/system), and exceptions—all at a glance.

- **Readable output:** Everything is well-formatted and non-interleaved, so you never have to sift through jumbled output.

See [Readme_test.md](Readme_test.md) for detailed test examples and more info!


### Helpers coming soon:
- **test** – Easy, modular testing with robust logging (randomized tests, summary tables, etc.)
- **log** – Flexible, readable logging helpers for your scripts (wraps output, logs warnings, etc.)
- **format** – Helpers for formatting currencies, percentages, and more (works with all data structures)
- **backup** – Saves backup of file (data or script) to specified location, with pruning of old backups beyond user set maximum.
---
### Install

**In Terminal:**
```bash
  pip install clearutils
  # or, copy the helpers directly into your project folder
```

**Note for users and advanced users:**
All files ending with _engine.py contain the core logic for each module in clearutils. You should not need to edit these files unless you are customizing advanced behaviors.
For most users, everything you need is available directly through the functions imported from clearutils.

**Running your own tests:**
To test your own code, edit the provided test runner file. An example mytest_runner.py is provided with installation. You can find it ...
Recommended: locate your mytests_runner in the top level of your project (next to your main script).
Simply add your test functions there, following the examples in the documentation in the demo file and in Readme_test.md.
There is no need to modify the internal test_engine.py file unless you wish to customize the core test-running logic.


## Import

```python
# Import only what you need (shortest, cleanest)
from clearutils.clearutils import logw
from clears import currency, percentage  # Full, descriptive names
from clearutils.clearutils import curr, per  # Short aliases (for less typing)

# Or import everything with an alias (avoids name conflicts)
from clearutils import clearutils as clu

clu.logw("Log something")
```


## Requirements
- Python 3.11 or later
- numpy, pandas

See requirements.txt for full dependencies.

### Usage Example

```python
# Recommended: Import just the helpers you need, directly from clearutils
# “curr” and “per” are the short aliases for “currency” and “percentage.”
from clearutils.clearutils import logw, backup_file, curr, per, set_currency_defaults
from clearutils.clearutils import assert_log, assert_log_label, assert_log_exception
from clearutils.clearutils import run_test_safely, run_all_tests_randomized

# ----- Logging -----
logw("Logging something very long")  # nicely formatted, wrapped text with indents

try:
  1 / 0
except Exception as e:
  logw_traceback(e)  # prints a clear, formatted traceback

# ----- Formatting -----
result1 = curr(12345.67)  # = $12,346  (default is round to nearest dollar)
set_currency_defaults(currency_symbol="EUR", use_euro_style=True)
result2 =  curr(9876.543, 2) # = "€9.876,54", with euro style comma/period
result3 = per(.13486, -1)  # = 10% (round to nearest 10th percentile)

# ------ Testing ------
# See the detailed test examples below or in Readme_test.md

# ----- Backup -----
# USER SETTINGS (set in your main script)
MODULE_NAME = "foo"
# ...other user metadata as needed

# Backup current test script (in __main__)
backup_file(
  src_path=__file__,
  prefix=f"tests/{MODULE_NAME}",
  version="v1.0.0",  # Use your own versioning scheme
)

# Backup the main module file
# mymod, MODULE_NAME and other config variables are defined in a block at top)

MAX_BACKUPS = 2                 # Number of clean backups to retain, Set in USER SECTION
BACKUP_ENABLED = True           # Set in USER SECTION

backup_file(
  src_path=mymod.__file__,
  prefix=f"modules/{MODULE_NAME}",
  version=getattr(mymod, "__version__", "NA"),
)


```

### See [Readme_test.md](Readme_test.md), [Readme_log.md](Readme_log.md),[Readme_format.md](Readme_format.md), [Readme_backup.md](Readme_backup.md) for more detailed examples


## Design Philosophy

When building clearutils, my top priority is **clarity and usability**—both for myself and for anyone who uses these helpers.

**My goal:** Powerful, modular scripts where the *only* things in your main file are the settings you might want to change and the actual commands you want to run. All the complex, never-changing code lives out of sight in clearutils modules.

You don’t need to learn object-oriented or “Pythonic” design patterns just to get stuff done. For most scripts, this approach is fast, robust, and readable.

Only import what you need, with intuitive names. All helpers are modular—designed for clarity, speed, and a smooth workflow.

For example, in `test.py`, all you need to specify are your file names, file locations, and the tests you want to run. You never have to peek at the code for long helpers like `assert_log`.


---

### Sample Comment Section in Script

```
# ========================================================================
# TEST FUNCTIONS
# ========================================================================
# To add a new test:
#   • Define a function whose name starts with 'test_'.
#   • These will be automatically discovered and executed by the test runner.
#
# ⚠️ WARNING:
#   • All test functions MUST begin with 'test_' to be picked up.
#   • Numbering tests in names/descriptions is not useful, as tests are run in random order for the run log.
# ------------------------------------------------------------------------

"""
Notes on Tests and Logging Output:

See Readme_test.md, Readme_log.md, Readme_ for detailed examples. Main test statements:
    - assert_log_label:      Log a group label above related tests.
    - assert_log:            Check if intended result matches actual result. Individual tests can have labels too.
    - assert_log_exception:  Test if module warnings are properly caught when intentionally triggered.
                             Counts both user and system warnings separately in the summary table.
    - warnings.warn:         Intentionally emit a warning so it appears in the log.

Each time you run test.py, two log files are generated:

- 'log_doc.txt':
    • Shows output from all tests in the order they appear in this file.
    • Custom formatted with group labels, all test results, and a summary table (including warnings/exceptions).
    • Serves as complete documentation of tests run and output of tested functions.

- 'log_run.txt':
    • Shows output only from failed tests, in randomized order (to catch order dependencies).
    • Custom formatted with test results, summary table (including warnings/exceptions), tracebacks, and debug info.

For more details and usage examples, see Readme_test.md.
"""
```


### Sample User Code
```
# ---------------------- Tests for Currency Formatting ----------------------
assert_log_label(description = "Tests for Currency Formatting ")

def test_us_basic(description="verify expected currency output from strings"):
    assert_log(mypack.us(1234.567, 2) == "$1,234.57", "Basic format 2 digits",
               'mypack.us(1234.567, 2) == "$1,234.57"')
    assert_log(mypack.us(1234.567) == "$1,235", "Default rounding",
               'mypack.us(1234.567) == "$1,235"')

def test_us_with_numpy_array(description="verify expected currency output from numpy arrays"):
    mypack.reset_currency_defaults()
    arr = np.array([1234.567, -89.5, 0.045])
    formatted_array = mypack.us(arr, 2)
    assert_log(formatted_array == ["$1,234.57", "-$89.50", "$0.04"],"handle numpy array",
               'formatted_array == ["$1,234.57", "-$89.50", "$0.04"]')
```


If you have suggestions or spot bugs, I’d love your input. But to keep things clean and reliable, I’ll be reviewing all contributions myself and will prioritize changes that fit this philosophy.

⸻

### For Advanced Users: Class-Based and Context Manager Helpers

Right now, almost all helpers in clearutils use a “flat” style—just functions and arguments, no classes or context managers. All “globals” (config, logger, paths, etc.) are passed as arguments to the flat-style helpers. This lets you keep the main script focused and short—just the things you need to set or care about. All the “heavy lifting” is hidden in helpers, which you usually never need to touch.

With this style, all dependencies are explicit—no hidden state. If a helper needs something, it’s right there in the argument list.
This also makes it easier for beginners to edit and customize any script in clearutils if they download the package, instead of pip installing it.

**But!**

I know that for larger projects and/or advanced users, class-based helpers and context managers can be really useful (for keeping state, custom behavior, or managing resources).

**One of my goals is to add a heavily commented “advanced” version of these helpers (util_adv.py), rewritten using classes and/or context managers, as a teaching tool for myself and others.**


⸻

**HELP WANTED!**
If you’re experienced with these patterns and want to contribute—or if you’d find this kind of side-by-side example helpful—I’d love to hear from you!


### License

clearutils is released under the [MIT License](LICENSE).