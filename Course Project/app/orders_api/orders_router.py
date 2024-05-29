from fastapi import FastAPI, HTTPException, Request, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from orders_service.orderer import OrderCRUD
import json

app = FastAPI()
order_crud = OrderCRUD()


@app.post("/orders/", response_model=str)
async def create_order(order_data: dict = Body(...)):
    try:
        order_id = order_crud.create_order(order_data)
    except:
        raise HTTPException(
            status_code=400, detail="<ERR> Order created unsuccessfully (missing details).")
    return order_id


@app.get("/get_all")
async def get_all():
    try:
        orders = order_crud.read_all()
        # print(orders)
    except:
        raise HTTPException(
            status_code=400, detail="<ERR> Some problems.")
    return orders


@app.get("/orders")
async def read_order(order_id: str):
    try:
        order = order_crud.read_order(order_id)
        if order:
            return order
    except:
        raise HTTPException(
            status_code=400, detail="<ERR> Order founded unsuccessfully (bad ID).")
    raise HTTPException(status_code=404, detail="<ERR> Order not found.")


@app.put("/orders")
async def update_order(order_id: str, updated_data: dict = Body(...)):
    try:
        updated_count = order_crud.update_order(
            order_id, updated_data)
    except:
        raise HTTPException(
            status_code=400, detail="<ERR> Order updated unsuccessfully (bad ID).")
    if updated_count:
        return updated_count
    else:
        raise HTTPException(
            status_code=400, detail="<ERR> Нечего обновлять или конференция не найдена.")


@app.delete("/orders")
async def delete_order(order_id: str):
    try:
        deleted_count = order_crud.delete_order(order_id)
        if deleted_count:
            return deleted_count
    except:
        raise HTTPException(
            status_code=400, detail="<ERR> Order deleted unsuccessfully (bad ID).")
    raise HTTPException(status_code=404, detail="<ERR> Order not found.")
