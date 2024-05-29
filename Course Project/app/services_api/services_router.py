from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from service_service.servicer import ServiceService
import redis
import json
import requests
import jwt

app = FastAPI()
service_service = ServiceService()
r = redis.Redis(host='redis', port=6379, db=0)
SECRET_KEY = "secret_key"
security = HTTPBearer()


class Service(BaseModel):
    title: str
    description: str
    creator_id: int


def auth(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = payload["user_id"]
    except:
        raise HTTPException(
            status_code=401, detail="Invalid user data")
    return {"user_id": current_user}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        if error["msg"] == "Field required":
            modified_details.append(
                {
                    "message": f"The field {error["loc"][1]} absent in your request",
                }
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


@app.get("/user_services")
def read_user_services(user_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        creator_id = auth(credentials.credentials)['user_id']
        print(type(creator_id), type(user_id))
        if creator_id != user_id:
            raise HTTPException(status_code=401, detail="<ERR> ID аккаунтов не совпадают.")
        services = service_service.read_user_services(user_id)
        if services:
            return {"services": services}
        else:
            raise HTTPException(
                status_code=404, detail="<ERR> Услуги не найдены.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="<ERR> Невалидный ID.")


@ app.get("/services_read")
def read_service(service_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        creator_id = auth(credentials.credentials)['user_id']
        key = f'services/{service_id}'
        redis_info = r.get(key)
        if redis_info:
            print("Redis info")
            redis_creator_id = json.loads(redis_info)["creator_id"]
            if redis_creator_id == creator_id:
                return {"service": json.loads(redis_info), "message": "Взято из redis"}
            else:
                raise HTTPException(status_code=400, detail="<ERR> ID аккаунтов не совпадают.")
        service = service_service.read_service(service_id)
        if service:
            if service["creator_id"] == creator_id:
                service_json = json.dumps(service)
                r.set(key, service_json)
                r.expire(key, 30)
                return {"service": service}
            else:
                raise HTTPException(status_code=401, detail="<ERR> ID аккаунтов не совпадают.")
        else:
            raise HTTPException(
                status_code=404, detail="<ERR> Услуга не найдена.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="<ERR> Невалидный ID.")


@ app.post("/services/")
def create_service(service: Service, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        creator_id = auth(credentials.credentials)['user_id']
        if creator_id == service.creator_id:
            service_id = service_service.create_service(
                service.title, service.description, service.creator_id)
            key = f'services/{service_id}'
            service = service_service.read_service(service_id)
            json_service = json.dumps(service)
            if service:
                r.set(key, json_service)
                r.expire(key, 30)
                return service
        else:
            raise HTTPException(
                status_code=401, detail="<ERR> Неверный аккаунт для создания услуги.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"<ERR> Некорректный ввод или услуга уже существует в БД. {e}")
    return {"service_id": service_id}


@ app.put("/update_service")
def update_service(service_id: str, service: Service, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if auth(credentials.credentials)['user_id'] == service.creator_id:
            updated_service = service_service.update_service(
                service_id, service.title, service.description, service.creator_id)
        else:
            raise HTTPException(
                status_code=401, detail="<ERR> Невалидный ID создателя для изменения.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="<ERR> Невалидный ID.")
    if updated_service and updated_service != 1:
        key = f'services/{service_id}'
        updated_service_json = json.dumps(updated_service)
        r.rpush(key, updated_service_json)
        r.expire(key, 30)
        return updated_service
    elif updated_service == 1:
        raise HTTPException(
            status_code=400, detail="<ERR> Нечего обновлять.")
    else:
        raise HTTPException(
            status_code=400, detail="<ERR> Ничего нет по данному ID.")


@ app.delete("/services_delete")
def delete_service(service_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        headers = {"Authorization": f"Bearer {credentials.credentials}"}
        service_info = requests.get(
            f"http://services:8080/services_read?service_id={service_id}", headers=headers)
        if service_info.status_code == 200:
            creator_id = auth(credentials.credentials)['user_id']
            print(service_info.json())
            if service_info.json()["service"]["creator_id"] == creator_id:
                key = f'deleted/{service_id}'
                redis_info = r.get(key)
                if redis_info:
                    return {"message": json.loads(redis_info)}
                if service_service.delete_service(service_id):
                    r.set(key, "<ERR> Услуга не найдена (использован redis).")
                    r.expire(key, 100)
                    return {"message": "Услуга успешно удалена"}
                else:
                    raise HTTPException(
                        status_code=404, detail="<ERR> Услуга не найдена.")
            else:
                raise HTTPException(
                    status_code=401, detail="<ERR> Некорректный аккаунт.")
        elif service_info.status_code == 404:
            raise HTTPException(
                status_code=404, detail="<ERR> Услуга не найдена.")
        else:
            raise HTTPException(
                status_code=401, detail="<ERR> Некорректный аккаунт.")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="<ERR> Некорректная информация.")
