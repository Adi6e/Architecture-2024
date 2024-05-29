
from routers.gateway_router import router as gateway_router
from fastapi import FastAPI, HTTPException, Request, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
app = FastAPI()

app.include_router(gateway_router, tags=["Users"], prefix="/api/gateway")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        if error["msg"] == "Field required" or error["msg"] == "missing":
            modified_details.append(
                {
                    "message": f"The field {error["loc"][1]} absent in your request",
                }
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )
