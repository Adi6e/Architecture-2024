from fastapi import APIRouter, Depends, HTTPException
from utils.postgres_connector import PostgresConnector
import psycopg2
from models.user_model import NewUserModel, UpdateUserModel
import hashlib
from routers.login_router import auth
router = APIRouter()

connection = PostgresConnector(db_name="service_order_db")


@router.get("/find_by_name")
async def find_by_prefix(name: str, surname: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_command = "SELECT user_id, user_login, user_name, user_surname from users " + "\n"
    where_command = ""
    if name and surname:
        where_command = f"WHERE user_name LIKE '{name}%' AND user_surname LIKE '{surname}%'"
    elif name:
        where_command = f"WHERE user_name LIKE '{name}%'"
    elif surname:
        where_command = f"WHERE user_surname LIKE '{surname}%'"
    sql_command += where_command
    print(sql_command)
    cursor.execute(sql_command)
    result = cursor.fetchall()
    cursor.close()
    return result


@router.get("/find_by_login")
async def find_by_prefix(login, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        sql_command = f"SELECT user_id, user_login, user_name, user_surname from users WHERE user_login LIKE '{
            login}%'"
        cursor.execute(sql_command)
        result = cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
        raise HTTPException(status_code=400, detail="<ERR> Некорректный ввод данных.")
    return result


@router.get("/info")
async def find_by_prefix(id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        sql_command = \
            f"SELECT user_id, user_login, user_name, user_surname from users "\
            f"WHERE user_id = {id}"
        print(sql_command)
        cursor.execute(sql_command)
        result = cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
        raise HTTPException(status_code=400, detail="<ERR> Некорректный ввод данных.")
    return result


@router.post("/new_user")
async def new_user(new_user: NewUserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        sql_command: str = "INSERT INTO users (user_login, user_name, user_surname, user_password) VALUES (%s, %s, %s, %s)"
        hashed_password: str = hashlib.sha256(
            new_user.user_password.encode()).hexdigest()
        data: tuple = (new_user.user_login, new_user.user_name,
                       new_user.user_surname, hashed_password)
        cursor.execute(sql_command, data)
        cursor.connection.commit()
        cursor.close()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="<ERR> User not created.")
    return {"message": "User created successfully"}


@router.delete("/delete")
async def delete_user(id: int, token: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        user_info = auth(token=token)
        print(user_info)
        if "user_id" in user_info and user_info["user_id"] == id:
            tuple_id: tuple = (id,)
            sql_command = "DELETE FROM users WHERE user_id=%s"
            cursor.execute(sql_command, tuple_id)
            cursor.connection.commit()
            cursor.close()
        else:
            return HTTPException(status_code=402, detail="<ERR> Invalid authentication credentials.")
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="<ERR> User deleted unsuccessfully.")
    return {"message": "User deleted successfully or was deleted earlier"}


@router.put("/update")
async def find_by_prefix(updated_user: UpdateUserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        user_id = updated_user.user_id
        if updated_user.user_password:
            updated_user.user_password = hashlib.sha256(
                updated_user.user_password.encode()).hexdigest()

        updated_user_dict = UpdateUserModel.model_dump(
            updated_user, exclude_none=True, exclude=["user_id"])

        columns_to_update = ', '.join(
            [f"{key} = %s" for key in updated_user_dict.keys()])
        sql = f"UPDATE users SET {
            columns_to_update} WHERE user_id = %s RETURNING user_id"
        values = list(updated_user_dict.values())
        cursor.execute(sql, values + [user_id])
        if cursor.fetchone():
            return {"message": "User updated successfully"}
        else:
            raise Exception
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="<ERR> User not updated.")
