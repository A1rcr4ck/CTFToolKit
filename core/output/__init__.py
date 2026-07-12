# from enum import Enum


# class OutputFormat(str, Enum):
#     TABLE = "table"
#     JSON = "json"
#     YAML = "yaml"
#     CSV = "csv"


# from .dispatcher import dispatch

from .formatter import OutputFormat
from .dispatcher import dispatch

__all__ = [
    "OutputFormat",
    "dispatch",
]