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

    with raises(KeyError):
        [result] = validark.validate(schema, records)


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
