# Validark

Simple Data Validation Library

## Usage

Call the **validate** method with the required *schema* and the *records*
to be validated:

    from validark import validate

    schema = {
        "*name": str,
        "age": int
    }

    records = [{
        "name": "Pepito Pérez",
        "age": 64
    }]

    [result] = validate(schema, records)

    assert result == value


Schemas are just dictionaries whose keys are strings and whose records are
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
        records = [{"name": "John Doe", "age": 200}]
        [result] = validate(schema, records)
    except ValueError as e:
        message = str(e)

    assert message == "Invalid Age!"

Mandatory fields can be marked with an **asterix (*)** as key prefix:

    schema = {
        "title": str
        "*firstname": str,
        "*surname": str,
    }

Aliases can be delimited with **:=**. The final key will be the leftmost entry:

    schema = {
        "*first_name:=firstname:=firstName": str,
        "*last_name:=lastname:=lastName": str
    }

    records = [
        {"firstName": "Clark", "lastName": "Kent"},
        {"firstname": "Peter", "lastname": "Parker"},
        {"first_name": "Bruce", "last_name": "Wayne"}
    ]

    result = validate(schema, records)

    assert result == [
        {"first_name": "Clark", "last_name": "Kent"},
        {"first_name": "Peter", "last_name": "Parker"},
        {"first_name": "Bruce", "last_name": "Wayne"}
    ]

Extra keys in the records' entries are ignored and aliases definitions are
processed from right to left if there are multiple matches:

    schema = {
        "*name": str,
        "*player_id:=playerId": str,
        "*score:=totalScore:=points": int
    }

    records = [
        {"name": "James", "playerId": "007", "totalScore": 99, "points": 55}
    ]

    [result] = validate(schema, records)

    assert result == {
        "name": "James", "player_id": "007", "score": 99
    }
