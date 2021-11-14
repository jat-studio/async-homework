from typing import Optional

import jwt
import sqlite3

from flask import session

from entities import Task, User


AUTHSECRET = 'Xu6thooquai8ceih2aiveel2peev3zeec2nai2ooxohr6eic8zeeph4aeXingie9'
DATABASE = './tasks.db'
DB = None


def get_db():
    global DB
    if DB is None:
        DB = sqlite3.connect(DATABASE)

    return DB


def verify(token):
    if not token and session.get("token"):
        token = session.get("token")

    user = None
    try:
        decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
        user = get_user(decoded["public_id"])
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


def get_tasks(only_new: bool = False):
    condition = "where Status='new'" if only_new else ""
    query = f"select * from tasks {condition}"

    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()

    tasks = []
    for row in rows:
        tasks.append(
            Task(
                id=row[0],
                public_id=row[1],
                description=row[2],
                status=row[3],
                price=row[4],
                assign_to_public_id=row[5]
            ).__dict__
        )

    return tasks


def get_user_tasks(user_public_id: str):
    query = f"select * from tasks where AssignToPublicId='{user_public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()

    tasks = []
    for row in rows:
        tasks.append(
            Task(
                id=row[0],
                public_id=row[1],
                description=row[2],
                status=row[3],
                price=row[4],
                assign_to_public_id=row[5]
            ).__dict__
        )

    return tasks


def get_task(public_id: str):
    query = f"select * from tasks where PublicId='{public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    row = cur.fetchone()

    return Task(
        id=row[0],
        public_id=row[1],
        description=row[2],
        status=row[3],
        price=row[4],
        assign_to_public_id=row[5]
    ).__dict__


def add_task(
    public_id: str,
    description: str,
    status: str,
    price: str,
    assign_to_public_id: Optional[str],
) -> dict:
    query = (
        "insert into tasks "
        "(PublicId, Description, Status, Price, AssignToPublicId) values "
        f"('{public_id}', '{description}', '{status}', '{price}', '{assign_to_public_id}')"
    )

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()

    return get_task(public_id)


def complete_task(public_id: str):
    query = f"update tasks set status='completed' where PublicId='{public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()

    return get_task(public_id)


def assign_task(task_public_id: str, user_public_id: str):
    query = f"update tasks set AssignToPublicId='{user_public_id}' where PublicId='{task_public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()

    return get_task(task_public_id)


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


def get_users():
    query = "select * from users"

    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()

    users = []
    for row in rows:
        users.append(
            User(
                id=row[0],
                public_id=row[1],
                email=row[2],
                full_name=row[3],
                role=row[4],
            ).__dict__
        )

    return users
