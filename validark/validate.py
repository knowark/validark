from typing import Dict, List, Union, Any


Schema = Dict[str, Any]


Value = Union[List[Dict[str, Any]], Dict[str, Any]]


Result = Union[List[Dict[str, Any]], Dict[str, Any]]


def validate(schema: Schema, value: Value) -> Result:
    single = not isinstance(value, list)
    records = single and [value] or value

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

            if value is not None:
                if isinstance(validator, dict):
                    item[key] = next(iter(
                        validate(validator, [value])))
                    continue
                elif isinstance(validator, list):
                    validator = validator.pop()
                    if isinstance(validator, dict):
                        item[key] = validate(validator, value)
                    else:
                        item[key] = [validator(item) for item in value]
                    continue

                outcome = validator(value)
                if isinstance(outcome, Exception):
                    raise outcome

                item[key] = outcome

        result.append(item)

    return single and next(iter(result)) or result
