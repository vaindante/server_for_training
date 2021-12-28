tags = [
    {'name': 'User', 'description': 'Методы для работы с пользователями '},
    {'name': 'Books', 'description': 'Методы для взаимодействия с пользовательскими книгами'}
]

users_responses = {200: {
    "description": "Success",
    "content": {
        "application/json": {
            "example": [
                {
                    "id": 2,
                    "email": "zoja_54@example.com",
                    "name": "Федосеева Анастасия Егоровна",
                    "created_at": "2021-12-28T09:45:11.870Z",
                    "is_active": True,
                    "created_by": 1
                }
            ],

        },
        'application/xml': {
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'item': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'int', 'example': 2},
                                'email': {'type': 'string', 'example': 'zoja_54@example.com'},
                                'name': {'type': 'string', 'example': 'Федосеева Анастасия Егоровна'},
                                'created_at': {'type': 'string', 'example': '2021-12-28T09:45:11.870Z'},
                                'is_active': {'type': 'boolean', 'example': True},
                                'created_by': {'type': 'int', 'example': 1}
                            }
                        }
                    },
                },
                'xml': {'name': 'Users'}
            }
        },
        'text/csv': {
            'example': """
id,email,name,created_at,is_active,created_by
2,zoja_54@example.com,Федосеева Анастасия Егоровна,2021-12-28T09:45:11.870,True,1
        """}
    }}}
