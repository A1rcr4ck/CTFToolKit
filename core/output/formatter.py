from enum import Enum


class OutputFormat(str, Enum):
    TABLE = "table"
    JSON = "json"
    CSV = "csv"
    YAML = "yaml"