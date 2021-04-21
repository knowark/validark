from typing import Dict, List, Any


def validate(schema: Dict[str, Any], records: List[Dict[str, Any]]):
    result = []
    for record in records:
        item = {}
        for key, validator in schema.items():
            value = record.get(key)

            if key[0] == "*":
                key = key[1:]
                value = record[key]

            item[key] = value

        result.append(item)

    return result
