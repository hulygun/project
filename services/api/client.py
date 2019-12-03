"""
grpc test client
"""

from fastapi import FastAPI

from api.services.books import router

app = FastAPI(docs_url='/api', openapi_url='/api/openapi.json')

app.include_router(router, prefix='/api/book', tags=['book'])
