import os
import json

# pip install psycopg2
import psycopg2

#pip install -U python-dotenv
from dotenv import load_dotenv
load_dotenv()

# pip install pyjwt
import jwt

from auth_payload import AuthPayload
from auth_response import AuthResponse

# Get environment variables
DBNAME = os.getenv('DBNAME')
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv("DBPASSWORD")
AUTHSECRET = os.getenv("AUTHSECRET")
EXPIRESSECONDS = os.getenv('EXPIRESSECONDS')


def authenticate(email: str, client_secret: str) -> bool:
    conn = None
    query = "select * from clients where \"Email\"='" + email + "' and \"ClientSecret\"='" + client_secret + "'"
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

        if cur.rowcount == 1:
            for row in rows:
                payload = AuthPayload(
                    id=row[0],
                    uuid=row[1],
                    email=row[3],
                    full_name=row[4],
                    position=row[5],
                    is_active=row[6],
                    role=row[7],
                )
                break

            encoded_jwt = jwt.encode(payload.__dict__, AUTHSECRET, algorithm='HS256')
            response = AuthResponse(token=encoded_jwt, expiresin=int(EXPIRESSECONDS))
            
            return response.__dict__
        else:
            return False
        
    except (Exception, psycopg2.DatabaseError) as error:
        
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def verify(token):
    try:
        is_blacklisted = check_blacklist(token)
        if is_blacklisted:
            return {"success": False}
        else:
            decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
            return decoded
    except (Exception) as error:
        print(error)
        return {"success": False}


def create(
    hashed_client_secret: str,
    uuid: str,
    email: str,
    full_name: str,
    position: str,
    is_active: bool,
    role: str,
) -> bool:
    conn = None
    query = (
        "insert into clients "
        "(\"ClientSecret\", \"Uuid\", \"Email\", \"FullName\", \"Position\", \"IsActive\", \"Role\") "
        "values(%s, %s, %s, %s, %s, %s, %s)"
    )

    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(
            query,
            (
                hashed_client_secret,
                uuid,
                email,
                full_name,
                position,
                is_active,
                role,
            ),
        )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def blacklist(token: str) -> bool:
    conn = None
    query = "insert into blacklist (\"token\") values(\'" + token +"\')"
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def check_blacklist(token: str) -> bool:
    conn = None
    query = "select count(*) from blacklist where token=\'" + token + "\'"
    print(query)
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result[0] == 1:
            return True
        else:
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return True
    finally:
        if conn is not None:
            cur.close()
            conn.close()
