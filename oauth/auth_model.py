import jwt
import sqlite3

from flask import g

from auth_payload import AuthPayload
from auth_response import AuthResponse

AUTHSECRET = 'Xu6thooquai8ceih2aiveel2peev3zeec2nai2ooxohr6eic8zeeph4aeXingie9'
DATABASE = './users.db'
EXPIRESSECONDS = 10


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db


def authenticate(email: str, client_secret: str) -> bool:
    query = f"select * from users where Email='{email}' and ClientSecret='{client_secret}'"

    cur = get_db().cursor()
    cur.execute(query)
    row = cur.fetchone()

    if row:
        payload = AuthPayload(
            id=row[0],
            public_id=row[1],
            email=row[3],
            full_name=row[4],
            position=row[5],
            is_active=row[6],
            role=row[7],
        )

        encoded_jwt = jwt.encode(payload.__dict__, AUTHSECRET, algorithm='HS256')
        return AuthResponse(token=encoded_jwt, expiresin=int(EXPIRESSECONDS)).__dict__
    else:
        return False


def verify(token):
    try:
        decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
        return decoded
    except Exception:
        return {"success": False}


def create(
    hashed_client_secret: str,
    public_id: str,
    email: str,
    full_name: str,
    position: str,
    is_active: bool,
    role: str,
) -> dict:
    query = (
        "insert into users "
        "(ClientSecret, PublicId, Email, FullName, Position, IsActive, Role) "
        f"values ('{hashed_client_secret}', '{public_id}', '{email}', '{full_name}', '{position}', '{is_active}', '{role}')"
    )

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()

    return get_user(public_id)


def update_user(
    public_id: str,
    email: str,
    full_name: str,
    position: str,
    is_active: bool,
    role: str,
) -> tuple:
    user = get_user(public_id)

    is_role_changed = True if user["role"] != role else False

    query = (
        "update users set "
        f"Email='{email}', FullName='{full_name}', Position='{position}', IsActive='{is_active}', Role='{role}'"
        f"where PublicId='{public_id}'"
    )

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()

    return get_user(public_id), is_role_changed


def get_users() -> list:
    users = []
    query = "select * from users"

    cur = get_db().cursor()
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        users.append(
            AuthPayload(
                id=row[0],
                public_id=row[2],
                email=row[3],
                full_name=row[4],
                position=row[5],
                is_active=row[6],
                role=row[7],
            ).__dict__
        )

    return users


def delete(public_id: str) -> None:
    query = f"delete from users where PublicId='{public_id}'"

    cur = get_db().cursor()
    cur.execute(query)
    get_db().commit()


def get_user(public_id: str) -> dict:
    query = f"select * from users where PublicId='{public_id}'"

    cur = get_db().cursor()
    row = cur.execute(query).fetchone()

    return AuthPayload(
        id=row[0],
        public_id=row[2],
        email=row[3],
        full_name=row[4],
        position=row[5],
        is_active=row[6],
        role=row[7],
    ).__dict__
