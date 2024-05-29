import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, HTTPException, Depends
import jwt
from utils.postgres_connector import PostgresConnector
import psycopg2
import hashlib

router = APIRouter()
connection = PostgresConnector(db_name="service_order_db")

security = HTTPBasic()
SECRET_KEY = "secret_key"


@router.get("/auth")
def auth(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = payload["user_id"]
    except:
        raise HTTPException(
            status_code=402, detail="<ERR> Invalid user data.")
    return {"user_id": current_user}


@router.get("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        if credentials.username and credentials.password:
            sql_query = f"SELECT user_id, user_password FROM users \n"
            sql_query += f"WHERE users.user_login = %s"
            cursor.execute(sql_query, (credentials.username,))
            result = cursor.fetchone()
            cursor.close()
            if not result:
                return []
            hashed_password: str = hashlib.sha256(
                credentials.password.encode()).hexdigest()
            token = jwt.encode({'user_id': result[0], 'exp': datetime.datetime.now(
            ) + datetime.timedelta(minutes=30)}, SECRET_KEY, algorithm="HS256")
            if hashed_password == result[1]:
                return {"token": token}
            else:
                return {"message": "<ERR> Bad password."}
        elif credentials.username:
            return {"message": "<ERR> Bad username."}
        else:
            return {"message": "<ERR> Bad password."}
    except:
        raise HTTPException(
            status_code=402, detail="<ERR> Invalid user data.")
