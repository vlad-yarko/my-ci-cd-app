import os
import logging
import random
import time

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST
)

from engine import get_session, engine
from models import Request as SQLRequest, Base
from metrics import (
    REQUESTS,
    RESPONSES,
    EXCEPTIONS,
    REQUEST_LATENCY,
    IN_PROGRESS
)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://frontend"
]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

APP_NAME = "fastapi-backend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TEST_ENV", "") == "true":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)


# @app.get("/requests")
# async def get_requests(session: AsyncSession = Depends(get_session)):
#     stmt = (
#         select(Request)
#         .where(Request.id == True)
#         .with_for_update()
#     )
#     result = await session.execute(stmt)
#     requests_data = result.scalar_one()
#     requests_data.count += 1
#     await session.commit()
#     await session.refresh(requests_data)
#     return {
#         "count": requests_data.count
#     }



# @app.on_event("startup")
# async def startup():
#     if os.getenv("TEST_ENV", "") == "true":
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)



@app.get("/requests")
async def get_requests(session: AsyncSession = Depends(get_session)):
    stmt = select(SQLRequest).where(SQLRequest.id == True).with_for_update()
    result = await session.execute(stmt)
    requests_data = result.scalar_one_or_none()

    if not requests_data:
        requests_data = SQLRequest()
        session.add(requests_data)
        await session.commit()
        await session.refresh(requests_data)

    requests_data.count += 1
    await session.commit()
    await session.refresh(requests_data)

    return {"count": requests_data.count}


@app.get("/health")
async def health_endpoint(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(text("SELECT 1"))
        return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)
    except Exception:
        return JSONResponse(content={"status": "error"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


# @app.get("/react")
# async def react_endpoint():
#     data = os.getenv("REACT_PUBLIC_ANTON")
#     return data


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    path = request.url.path
    method = request.method
    
    REQUESTS.labels(
        path=path,
        app_name=APP_NAME,
        # method=method
    ).inc()

    IN_PROGRESS.labels(
        path=path,
        app_name=APP_NAME,
        # method=method
    ).inc()
    start_time = time.time()

    try:
        response = await call_next(request)
        status_code = str(response.status_code)

        RESPONSES.labels(
            path=path,
            status_code=status_code,
            app_name=APP_NAME,
            # method=method
        ).inc()            
        return response

    except Exception as e:
        EXCEPTIONS.labels(
            path=path,
            app_name=APP_NAME,
            # method=method
        ).inc()
        raise e

    finally:
        time_elapsed = time.time() - start_time
        REQUEST_LATENCY.labels(
            path=path,
            app_name=APP_NAME,
            # method=method
        ).observe(time_elapsed)
        
        IN_PROGRESS.labels(
            path=path,
            app_name=APP_NAME,
            # method=method
        ).dec()


@app.get("/metrics")
async def metrics():
    response = Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    return response
