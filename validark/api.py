from typing import Dict, List, Any


def validate(schema: Dict[str, Any], records: List[Dict[str, Any]]):
    result = []
    for record in records:
        item = {}
        for field, validator in schema.items():
            required, value = field[0] == '*', None
            field = field[1:] if required else field
            for key in reversed(field.split(':=')):
                value = record.get(key, value)

            if required and value is None:
                raise ValueError(f'The field "{key}" is required.')

            item[key] = validator(value)

        result.append(item)

    return result
