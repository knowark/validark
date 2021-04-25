from validark import camel_to_snake, snake_to_camel, normalize


def test_camel_to_snake():
    assert camel_to_snake('theBrownFox') == 'the_brown_fox'
    assert camel_to_snake('TheBrownFox') == 'the_brown_fox'
    assert camel_to_snake('the_brown_fox') == 'the_brown_fox'


def test_snake_to_camel():
    assert snake_to_camel('the_brown_fox') == 'theBrownFox'
    assert snake_to_camel('the_Brown_fox') == 'theBrownFox'
    assert snake_to_camel('The_Brown_Fox') == 'theBrownFox'
    assert snake_to_camel('theBrownFox') == 'theBrownFox'


def test_snake_normalize_simple():
    snake_data = normalize({
        'userId': '001',
        'name': 'Jhon Doe',
        'accountId': '7890'
    }, 'snake')

    assert snake_data == {
        'user_id': '001',
        'name': 'Jhon Doe',
        'account_id': '7890'
    }


def test_snake_normalize_nested():
    snake_data = normalize({
        'userId': '001',
        'address': {
            'city': 'Popayán',
            'zipCode': 190002
        },
        'name': 'Jhon Doe',
        'accountId': '7890'
    }, 'snake')

    assert snake_data == {
        'user_id': '001',
        'address': {
            'city': 'Popayán',
            'zip_code': 190002
        },
        'name': 'Jhon Doe',
        'account_id': '7890'
    }


def test_snake_normalize_deep_nested():
    snake_data = normalize({
        'userId': '001',
        'address': {
            'city': 'Popayán',
            'zipCode': 190002,
            'neighborhood': {
                'zone': 'A',
                'hubLocality': 'Lake Ville'
            }

        },
        'name': 'Jhon Doe',
        'accountId': '7890'
    }, 'snake')

    assert snake_data == {
        'user_id': '001',
        'address': {
            'city': 'Popayán',
            'zip_code': 190002,
            'neighborhood': {
                'zone': 'A',
                'hub_locality': 'Lake Ville'
            }
        },
        'name': 'Jhon Doe',
        'account_id': '7890'
    }


def test_snake_normalize_list():
    snake_data = normalize({
        'userId': '001',
        'name': 'Jhon Doe',
        'accountId': '7890',
        'contacts': [
            {'userId': '002', 'name': 'Mark', 'phoneNumber': '2222'},
            {'userId': '003', 'name': 'Brad', 'phoneNumber': '3333'},
            {'userId': '004', 'name': 'Carl', 'phoneNumber': '4444'},
        ]
    }, 'snake')

    assert snake_data == {
        'user_id': '001',
        'name': 'Jhon Doe',
        'account_id': '7890',
        'contacts': [
            {'user_id': '002', 'name': 'Mark', 'phone_number': '2222'},
            {'user_id': '003', 'name': 'Brad', 'phone_number': '3333'},
            {'user_id': '004', 'name': 'Carl', 'phone_number': '4444'}
        ]
    }


def test_camel_normalize_complex():
    camel_data = normalize({
        'user_id': '001',
        'name': 'Jhon Doe',
        'account_id': '7890',
        'contacts': [
            {'user_id': '002', 'name': 'Mark', 'phone_number': '2222'},
            {'user_id': '003', 'name': 'Brad', 'phone_number': '3333'},
            {'user_id': '004', 'name': 'Carl', 'phone_number': '4444'}
        ]
    })

    assert camel_data == {
        'userId': '001',
        'name': 'Jhon Doe',
        'accountId': '7890',
        'contacts': [
            {'userId': '002', 'name': 'Mark', 'phoneNumber': '2222'},
            {'userId': '003', 'name': 'Brad', 'phoneNumber': '3333'},
            {'userId': '004', 'name': 'Carl', 'phoneNumber': '4444'}
        ]
    }


def test_camel_normalize_list():
    camel_data = normalize([
        {'user_id': '002', 'name': 'Mark', 'phone_number': '2222'},
        {'user_id': '003', 'name': 'Brad', 'phone_number': '3333'},
        {'user_id': '004', 'name': 'Carl', 'phone_number': '4444'}
    ])

    assert camel_data == [
        {'userId': '002', 'name': 'Mark', 'phoneNumber': '2222'},
        {'userId': '003', 'name': 'Brad', 'phoneNumber': '3333'},
        {'userId': '004', 'name': 'Carl', 'phoneNumber': '4444'}
    ]


def test_camel_normalize_primitives():
    camel_data = normalize([
        {'user_id': '002', 'name': 'Mark', 'phone_number': '2222'},
        "admin",
        5
    ])

    assert camel_data == [
        {'userId': '002', 'name': 'Mark', 'phoneNumber': '2222'},
        "admin",
        5
    ]


def test_camel_normalize_none():
    camel_data = normalize(None)

    assert camel_data is None
