"""
format_engine.py — Formatting utilities for currency and percentages
Version: 01.1_dev
Author: Renya Wasson
License: MIT
"""

__version__ = "01_1_dev"
__author__ = "Renya Wasson"
__license__ = "MIT"
__updated__ = "2025-05-13"

import numpy as np
import pandas as pd
import warnings

# --------------------------- Settings ---------------------------
_default_currency_symbol = "$"
_use_euro_style = False


def set_currency_defaults(currency_symbol="USD", use_euro_style=False):
    """
    Set the default currency formatting options.

    Parameters:
        currency_symbol (str): ISO code or symbol to use.
        use_euro_style (bool): Whether to use European style (comma as decimal).
    """
    global _default_currency_symbol, _use_euro_style
    _default_currency_symbol = currency_symbol
    _use_euro_style = use_euro_style


def reset_currency_defaults():
    """Reset currency defaults to USD and non-European style formatting."""
    global _default_currency_symbol, _use_euro_style
    _default_currency_symbol = "$"
    _use_euro_style = False


def get_supported_currency_symbols():
    """Returns a dictionary of supported ISO currency codes and their symbols."""
    return {
        "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "CNY": "¥", "INR": "₹", "RUB": "₽", "KRW": "₩",
        "BRL": "R$", "AUD": "A$", "CAD": "C$", "CHF": "CHF", "SEK": "kr", "NOK": "kr", "DKK": "kr",
        "ZAR": "R", "PLN": "zł", "MXN": "$", "IDR": "Rp", "THB": "฿", "MYR": "RM", "PHP": "₱", "VND": "₫",
        "ILS": "₪", "TRY": "₺", "HUF": "Ft", "CZK": "Kč", "AED": "د.إ", "SAR": "ر.س", "EGP": "ج.م",
        "NGN": "₦", "PKR": "₨", "BDT": "৳", "UAH": "₴", "KZT": "₸", "CLP": "$", "COP": "$", "PEN": "S/."
    }


def format_currency(amount=None, digit=0, currency_symbol=None):
    """
    Format a number or collection of numbers as currency.

    Parameters:
        amount: A numeric value or list/array/Series/DataFrame of values.
        digit (int): Number of decimal places to round to.
                     Can be negative to round to tens, hundreds, etc.
        currency_symbol (str, optional): ISO code (e.g., "EUR", "JPY") or symbol (e.g., "$", "€").
                                         If None, defaults to USD or user-set default.

    Returns:
        A string or collection of strings with the formatted currency.

    Examples:
        >>> format_currency(1234.567, 2)
        '$1,234.57'

        >>> format_currency(-9876.543, 0, currency_symbol='EUR')
        '-€9,877'

        >>> format_currency([5.5, 2.5], 0)
        ['$6', '$2']

        >>> format_currency(12345.67, -2)
        '$12,300'

        >>> format_currency(98765.4321, -3)
        '$99,000'
    """
    if amount is None:
        raise TypeError("Missing required numeric input (e.g., amount to format as currency)")

    if not isinstance(digit, int):
        raise TypeError(
            "The 'digit' argument (for rounding) must be an integer (default is 0). "
            "If you intended to specify a currency (e.g., 'EUR' or 'YEN'), use the keyword argument "
            "'currency_symbol=...'. The default symbol is $ for 'USD', unless changed by the user.")

    symbols = get_supported_currency_symbols()
    symbol = currency_symbol or _default_currency_symbol
    prefix = symbols.get(symbol.upper(), symbol)

    use_euro = _use_euro_style
    thousands_sep = "." if use_euro else ","
    decimal_sep = "," if use_euro else "."

    def format_single(val):
        if not isinstance(val, (int, float, np.number)) or pd.isna(val):
            return val
        rounded = round(val, digit)
        int_part, _, frac_part = f"{abs(rounded):.{abs(digit)}f}".partition(".")
        int_part = f"{int(int_part):,}".replace(",", thousands_sep)
        formatted = int_part
        if digit > 0:
            formatted += decimal_sep + frac_part
        elif digit < 0:
            formatted = f"{int(round(rounded, digit)):,}".replace(",", thousands_sep)
        sign = "-" if val < 0 else ""
        return f"{sign}{prefix}{formatted}"


    if isinstance(amount, (list, tuple, np.ndarray, pd.Series)):
        return [format_single(x) for x in amount]
    elif isinstance(amount, pd.DataFrame):
        return amount.apply(lambda col: col.map(format_single))
    else:
        return format_single(amount)


def format_percent(value=None, digit=1):
    """
    Format a number or collection of numbers as a percentage string.

    Parameters:
        value: A numeric value or list/array/Series/DataFrame of values.
        digit (int): Number of decimal places to round to.
                     Can be negative to round to tens, hundreds, etc.

    Returns:
        A string or collection of strings with the formatted percentage.

    Examples:
        >>> format_percent(0.1234, 2)
        '12.34%'

        >>> format_percent(0.9876)
        '98.8%'

        >>> format_percent([-0.12345, 0.05432], 1)
        ['-12.3%', '5.4%']

        >>> format_percent(.12345, -1)
        '10%'

        >>> format_percent(0.6789, -2)
        '100%'
    """
    if value is None:
        raise TypeError("Missing required numeric input (e.g., amount to format as percentage)")

    if not isinstance(digit, int):
        raise TypeError("The 'digit' argument must be an integer")

    # Note on rounding behavior:
    # Python's built-in round() uses "bankers rounding" (round half to even).
    # This means that numbers exactly halfway between two values
    # are rounded to the nearest even number to reduce cumulative bias,
    # which is preferred for financial and statistical calculations.
    #
    # For example:
    #   round(2.5) == 2  (rounded down to even)
    #   round(3.5) == 4  (rounded up to even)
    #
    # If you prefer traditional rounding (always round .5 up),
    # consider using the Decimal module with ROUND_HALF_UP.
    #
    # For large datasets or Monte Carlo simulations,
    # bankers rounding usually yields more accurate aggregate results,
    # but individual rounding results may sometimes feel unintuitive.

    def format_single(v):
        if not isinstance(v, (int, float, np.number)) or pd.isna(v):
            return v
        pct = v * 100
        rounded = round(pct, digit)
        if digit < 0:
            formatted = f"{int(round(rounded, digit)):,}"
        else:
            formatted = f"{rounded:,.{digit}f}"
        return formatted + "%"

    if isinstance(value, (list, tuple, np.ndarray, pd.Series)):
        return [format_single(x) for x in value]
    elif isinstance(value, pd.DataFrame):
        return value.apply(lambda col: col.map(format_single))
    else:
        return format_single(value)

# ------------------ Aliases ------------------
us = format_currency
curr = format_currency
currency = format_currency
per = format_percent
