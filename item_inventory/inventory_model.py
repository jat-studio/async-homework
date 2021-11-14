import json
import jwt
import sqlite3

from flask import session

from entities import Item, User


AUTHSECRET = 'Xu6thooquai8ceih2aiveel2peev3zeec2nai2ooxohr6eic8zeeph4aeXingie9'
DATABASE = './items.db'
DB = None


def get_db():
    global DB
    if DB is None:
        DB = sqlite3.connect(DATABASE)

    return DB


def verify(token):
    if not token and session.get("token"):
        token = session.get("token")

    print(token)
    user = None
    try:
        decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
        user = get_user(decoded["public_id"])
        print(user)
    except Exception:
        return False

    session["token"] = token
    return user


def get_user(public_id: str) -> dict:
    query = f"select * from users where PublicId='{public_id}'"

    cur = get_db().cursor()
    row = cur.execute(query).fetchone()

    return User(
        id=row[0],
        public_id=row[1],
        email=row[2],
        full_name=row[3],
        role=row[4],
    ).__dict__


def get_items(user: dict, w_all: bool = False):
    items = []
    condition = "" if w_all else f"where UserId='{user['id']}'"

    query = f"select * from items {condition}"

    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        items.append(
            Item(
                id=row[0],
                user_id=row[1],
                public_id=row[2],
                title=row[3],
                description=row[4],
                status=row[5],
                meta=json.loads(row[6])
            ).__dict__
        )

    return items


def get_item(public_id: str):
    query = f"select * from items where PublicId='{public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    row = cur.fetchone()

    return Item(
        id=row[0],
        user_id=row[1],
        public_id=row[2],
        title=row[3],
        description=row[4],
        status=row[5],
        meta=json.loads(row[6])
    ).__dict__


def add_item(
    public_id: str,
    title: str,
    description: str,
    status: str,
) -> dict:
    query = (
        "insert into items "
        "(PublicId, Title, Description, Status) values "
        f"('{public_id}', '{title}', '{description}', '{status}')"
    )

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()

    return get_item(public_id)


def add_user(
    public_id: str,
    email: str,
    full_name: str,
    role: str,
) -> None:
    query = (
        "insert into users "
        "(PublicId, Email, FullName, Role) values "
        f"('{public_id}', '{email}', '{full_name}', '{role}')"
    )

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()


def update_user(
    public_id: str,
    email: str,
    full_name: str,
) -> None:
    query = (
        "update users set "
        f"Email='{email}', FullName='{full_name}' where PublicId='{public_id}'"
    )

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()


def update_user_role(
    public_id: str,
    role: str,
) -> None:
    query = (
        "update users set "
        f"Role='{role}' where PublicId='{public_id}'"
    )

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()


def book_item(public_id: str) -> None:
    query = f"update items set Status='locked' where PublicId='{public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()


def unbook_item(public_id: str) -> None:
    query = f"update items set Status='free' where PublicId='{public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()


def broken_item(public_id: str) -> None:
    query = f"update items set Status='broken' where PublicId='{public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()
