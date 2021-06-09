from pytest import raises
import validark


def test_validate_is_defined():
    assert validark.validate is not None


def test_validate_simple_data():
    schema = {
        "company": str,
        "city": str,
        "year": int
    }

    records = [
        {"company": "Knowark", "city": "Popayán", "year": 2015}
    ]

    [result] = validark.validate(schema, records)

    assert result == {"company": "Knowark", "city": "Popayán", "year": 2015}


def test_validate_required_fields():
    schema = {
        "*name": str,
        "age": float
    }

    records = [
        {"age": 15.5}
    ]

    with raises(ValueError) as e:
        [result] = validark.validate(schema, records)

    assert str(e.value) == 'The field "name" is required.'


def test_validate_validator_functions():
    schema = {
        "product": str,
        "quantity": int,
        "price": float
    }

    records = [
        {"product": "Manimoto", "quantity": 5.5, "price": 4700}
    ]

    [result] = validark.validate(schema, records)

    assert result == {
        "product": "Manimoto", "quantity": 5, "price": 4700.0
    }


def test_validate_lambda_functions():
    schema = {
        "*place": str,
        "year": lambda v: 1920 < v < 2030 and v or 1970
    }

    records = [
        {"place": "England", "year": 2021},
        {"place": "Japan", "year": 2050}
    ]

    result = validark.validate(schema, records)

    assert result == [
        {"place": "England", "year": 2021},
        {"place": "Japan", "year": 1970}
    ]


def test_validate_aliases():
    schema = {
        "*first_name:=firstName": str,
        "*last_name:=lastName": str
    }

    records = [
        {"first_name": "Donald", "last_name": "Trump"},
        {"firstName": "Joseph", "lastName": "Biden"}
    ]

    result = validark.validate(schema, records)

    assert result == [
        {"first_name": "Donald", "last_name": "Trump"},
        {"first_name": "Joseph", "last_name": "Biden"}
    ]


def test_validate_multiple_aliases():
    schema = {
        "*first_name:=name:=firstName": str,
        "*last_name:=surName:=lastName": str
    }

    records = [
        {"first_name": "Donald", "name": "John", "surName": "Trump"},
        {"firstName": "Joseph", "name": "Robinette", "lastName": "Biden"}
    ]

    result = validark.validate(schema, records)

    assert result == [
        {"first_name": "Donald", "last_name": "Trump"},
        {"first_name": "Robinette", "last_name": "Biden"}
    ]


def test_validate_nested_dicts():
    schema = {
        "*color": str,
        "width": int,
        "height": int,
        "weight": float,
        "duration": lambda v: 0 <= v <= 59 and v or 0,
        "*contact": {
            "*phone": str,
            "email": lambda v: '@' in v and v or ''
        }
    }

    records = [{
        "color": "red",
        "width": 100,
        "height": 300,
        "duration": 50,
        "contact": {
            "phone": 3456789,
            "email": "info@example.com"
        }
    }, {
        "color": "blue",
        "duration": 99,
        "contact": {
            "phone": 987654,
            "email": "blablabla"
        }
    }]

    result = validark.validate(schema, records)

    assert result == [{
        "color": "red",
        "width": 100,
        "height": 300,
        "duration": 50,
        "contact": {
            "phone": "3456789",
            "email": "info@example.com"
        }
    }, {
        "color": "blue",
        "duration": 0,
        "contact": {
            "phone": "987654",
            "email": ""
        }
    }]


def test_validate_list_schema_values():
    schema = {
        "levels": [str],
        "addresses": [
            {'*street': str, 'city': str}
        ]
    }

    records = [{
        "levels": [1, 2, 3],
        "addresses": [
            {"street": '5th Ave 45', "city": "Popeland"},
            {"street": '7th Street 67', "city": "Churchland"}
        ]
    }]

    [result] = validark.validate(schema, records)

    assert result == {
        "levels": ["1", "2", "3"],
        "addresses": [
            {"street": '5th Ave 45', "city": "Popeland"},
            {"street": '7th Street 67', "city": "Churchland"}
        ]
    }


def test_validate_exception_object():
    schema = {
        "*duration": lambda v: 0 <= v <= 59 and v or 0,
        "*contact": {
            "*phone": str,
            "email": lambda v: '@' in v and v or ValueError(
                f'Invalid email: "{v}"')
        }
    }

    records = [{
        "duration": 50,
        "contact": {
            "phone": 3456789,
            "email": "blablabla"
        }
    }]

    with raises(ValueError) as e:
        [result] = validark.validate(schema, records)

    assert str(e.value) == 'Invalid email: "blablabla"'


def test_validate_single_dictionary():
    schema = {
        "records": [{
            "*duration": lambda v: 0 <= v <= 59 and v or 0,
            "*contact": {
                "*phone": str,
                "email": lambda v: '@' in v and v or ''
            }
        }]
    }

    request = {
        "records": [{
            "duration": 50,
            "contact": {
                "phone": 3456789,
                "email": "info@example.com"
            }
        }, {
            "duration": 99,
            "contact": {
                "phone": 987654,
                "email": "blablabla"
            }
        }]
    }

    result = validark.validate(schema, request)

    assert result == {
        'records': [{
            "duration": 50,
            "contact": {
                "phone": "3456789",
                "email": "info@example.com"
            }
        }, {
            "duration": 0,
            "contact": {
                "phone": "987654",
                "email": ""
            }
        }]
    }
