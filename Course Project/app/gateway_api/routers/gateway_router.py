from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
import hashlib
import requests
import pybreaker
from models.service_model import Service
import json

router = APIRouter()
security: HTTPBasicCredentials = HTTPBasic()
security_bearer = HTTPBearer()

# Create a Circuit Breaker instance
circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


def get_token(credentials: HTTPBasicCredentials):
    try:
        response = circuit_breaker.call(
            requests.get,
            "http://user_service:8080/api/login_router/login",
            auth=(credentials.username, credentials.password)
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()["token"]
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="<ERR> User service unavailable due to Circuit Breaker.")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="<ERR> Что-то не так с токеном, возможно, его не существует.")


@router.get("/user_services")
def get_service(user_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.get,
            f"http://services:8080/user_services?user_id={user_id}",
            headers=headers
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="<ERR> Services service unavailable due to Circuit Breaker.")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/get_service")
def get_service(service_id: str, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.get,
            f"http://services:8080/services_read?service_id={service_id}",
            headers=headers
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="<ERR> Services service unavailable due to Circuit Breaker.")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/create_service")
def create_service(service: Service, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.post,
            f"http://services:8080/services/",
            headers=headers,
            data=service.model_dump_json()
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="<ERR> Services service unavailable due to Circuit Breaker.")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.put("/update_service")
def update_service(service_id: str, service: Service, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.put,
            f"http://services:8080/update_service?service_id={service_id}",
            headers=headers,
            data=service.model_dump_json()
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError as e:
        raise HTTPException(
            status_code=503, detail="<ERR> Services service unavailable due to Circuit Breaker.")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.delete("/delete_service")
def delete_service(service_id: str, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = circuit_breaker.call(
            requests.delete,
            f"http://services:8080/services_delete?service_id={service_id}",
            headers=headers
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="<ERR> Services service unavailable due to Circuit Breaker.")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
