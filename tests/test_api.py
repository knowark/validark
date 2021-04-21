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
