# Validark

Simple Data Validation Library

## Usage

Call the **validate** method with the required *schema* and the *values*
to be validated:

    from validark import validate

    schema = {
        "*name": str,
        "age": int
    }

    values = [{
        "name": "Pepito Pérez",
        "age": 64
    }]

    [result] = validate(schema, values)

    assert result == value


Schemas are just dictionaries whose keys are strings and whose values are
validation callables, dictionaries or lists. e.g.:

    schema = {
        "color": str,
        "width": int,
        "height": int,
        "weight": float,
        "duration": lambda v: 0 < v <= 50 and v
        "contact": {
            "phone": str,
            "email": lambda v: '@' in v and v
        }
    }

**Validation callables** must receive their keys' corresponding input value and
return the final value that will be assigned to such key. If an **Exception**
is received, it will be raised:

    schema = {
        "name": str,
        "age": lambda v: 0 < v < 130 and v or ValueError("Invalid Age!")
    }

    message = None

    try:
        values = [{"name": "John Doe", "age": 200}]
        [result] = validate(schema, values)
    except ValueError as e:
        message = str(e)

    assert message == "Invalid Age!"

Mandatory fields can be marked with an **asterix (*)** as key prefix:

    schema = {
        "title": str
        "*firstname": str,
        "*surname": str,
    }
