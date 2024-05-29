
from routers.user_router import router as user_router
from routers.login_router import router as login_router
from fastapi import FastAPI, HTTPException, Request, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
app = FastAPI()

app.include_router(user_router, tags=["Users"], prefix="/api/users")
app.include_router(login_router, tags=["Login"], prefix="/api/login_router")


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
