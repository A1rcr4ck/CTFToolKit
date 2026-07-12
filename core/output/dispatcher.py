from .formatter import OutputFormat
from .table import print_table
from .json import print_json


def dispatch(output_format, table_data=None, json_data=None):

    if output_format == OutputFormat.TABLE.value:
        return print_table(*table_data)

    if output_format == OutputFormat.JSON.value:
        return print_json(json_data)

    raise NotImplementedError(output_format)