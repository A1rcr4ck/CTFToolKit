import json
from dataclasses import asdict, is_dataclass


def to_json(obj):

    if is_dataclass(obj):
        return asdict(obj)

    if isinstance(obj, list):

        result = []

        for item in obj:

            if is_dataclass(item):
                result.append(asdict(item))
            else:
                result.append(item)

        return result

    return obj


def print_json(obj):

    print(
        json.dumps(
            to_json(obj),
            indent=4,
        )
    )