from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
from app.database import SessionLocal
from app.routers import auth,catalog,operations,orders,user_resources
app=FastAPI(title=settings.app_name,version=settings.app_version,description="FastAPI conversion of the Pharmacy Express.js API. Authenticate in Swagger with a Bearer JWT.",docs_url="/docs",redoc_url="/redoc",openapi_url="/openapi.json")
app.add_middleware(CORSMiddleware,allow_origins=[settings.client_origin],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for r in (auth.router,catalog.router,user_resources.router,orders.router,operations.router): app.include_router(r)
@app.get("/api/health",tags=["Health"])
def health():
    with SessionLocal() as db: db.execute(text("select 1"))
    return {"status":"ok","database":"connected"}
@app.exception_handler(RequestValidationError)
async def validation_error(_:Request,exc:RequestValidationError): return JSONResponse(status_code=400,content={"message":"; ".join(e["msg"] for e in exc.errors())})
@app.exception_handler(SQLAlchemyError)
async def db_error(_:Request,exc:SQLAlchemyError): return JSONResponse(status_code=500,content={"message":"Database error"})
@app.exception_handler(404)
async def not_found(_:Request,exc): return JSONResponse(status_code=404,content={"message":"Route not found"})
