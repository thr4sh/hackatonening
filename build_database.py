import os
from datetime import datetime
from config import db
from models import Person, Note

# Данные для инициализации базы данных
PEOPLE = [
    {
        "fname": "Doug",
        "lname": "Farrell",
        "notes": [
            ("Круто, приложение для мини-блогов!", "2019-01-06 22:17:54"),
            ("Это может быть полезно", "2019-01-08 22:17:54"),
            ("Ну вроде полезно", "2019-03-06 22:17:54"),
        ],
    },
    {
        "fname": "Kent",
        "lname": "Brockman",
        "notes": [
            (
                "Я собираюсь сделать действительно глубокие наблюдения",
                "2019-01-07 22:17:54",
            ),
            (
                "Может быть, они будут более очевидными, чем я думал",
                "2019-02-06 22:17:54",
            ),
        ],
    },
    {
        "fname": "Bunny",
        "lname": "Easter",
        "notes": [
            ("Кто-нибудь видел мои пасхальные яйца?", "2019-01-07 22:47:54"),
            ("Я действительно опоздал с доставкой!", "2019-04-06 22:17:54"),
        ],
    },
]

# Удалите файл базы данных, если он существует в данный момент
if os.path.exists("people.db"):
    os.remove("people.db")

# Создание базы данных
db.create_all()

# Выполните итерацию по структуре людей и заполните базу данных
for person in PEOPLE:
    p = Person(lname=person.get("lname"), fname=person.get("fname"))

    # Добавьте заметки для этого человека
    for note in person.get("notes"):
        content, timestamp = note
        p.notes.append(
            Note(
                content=content,
                timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
            )
        )
    db.session.add(p)

db.session.commit()