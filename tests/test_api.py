import validark


def test_validate_is_defined():
    assert validark.validate is not None


def test_validate_simple_data():
    schema = {
        "company": str,
        "city": str,
        "year": int
    }

    values = [
        {"company": "Knowark", "city": "Popayán", "year": 2015}
    ]

    [result] = validark.validate(schema, values)

    assert result == {"company": "Knowark", "city": "Popayán", "year": 2015}
