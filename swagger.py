from tkinter.scrolledtext import example

tags = [
    {'name': 'User', 'description': 'Методы для работы с пользователями '},
    {'name': 'Books', 'description': 'Методы для взаимодействия с пользовательскими книгами'}
]
import xml.etree.ElementTree as et

# Создаем корневой элемент
payee = et.Element('Users')
user = et.SubElement(payee, 'item', attrib={'type': 'dict'})

id_ = et.SubElement(user, 'id', attrib={'type': 'int'})
id_.text = '1'
email = et.SubElement(user, 'email', attrib={'type': 'str'})
email.text = 'zoja_54@example.com'
name = et.SubElement(user, 'name', attrib={'type': 'str'})
name.text = 'Федосеева Анастасия Егоровна'
created_at = et.SubElement(user, 'created_at', attrib={'type': 'str'})
created_at.text = '2021-04-27 00:00:00'

is_active = et.SubElement(user, 'is_active', attrib={'type': 'bool'})
is_active.text = 'True'

created_by = et.SubElement(user, 'created_by', attrib={'type': 'int'})
created_by.text = '1'
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
