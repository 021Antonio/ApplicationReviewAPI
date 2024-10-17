import logging
from fastapi import FastAPI, Request, Response
from time import time
from db import engine
from models.base import Base
from routes import review
import os
from cache import redis_client
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json

# Verifica se o diretório de logs existe, se não, cria
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),  # Registra logs em arquivo
        logging.StreamHandler()  # Exibe logs no console
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Inclui as rotas do módulo de review
app.include_router(review.router)

# Função para criar tabelas no banco de dados
def create_tables():
    Base.metadata.create_all(bind=engine)

# Evento de startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Middleware para logging de requisições e respostas, além de caching
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()

    logger.info(f"Recebendo requisição {request.method} {request.url}")

    # Gera uma chave de cache baseada no método e na URL
    cache_key = f"{request.method}_{request.url.path}"

    # Verifica se a resposta está no cache Redis
    cached_response = redis_client.get(cache_key)
    if cached_response:
        logger.info(f"Retornando resposta do cache para {request.url}")
        # Desserializa a resposta armazenada como string JSON para dicionário
        return JSONResponse(content=json.loads(cached_response.decode()))

    # Chama a próxima função no pipeline (processamento da requisição)
    response = await call_next(request)

    duration = time() - start_time

    logger.info(f"Enviando resposta status_code={response.status_code} "
                f"para {request.method} {request.url} em {duration:.2f}s")

    # Verifica se o status da resposta é 200 (sucesso)
    if response.status_code == 200:
        # Lê o corpo da resposta
        body = [section async for section in response.body_iterator]
        response_body = b''.join(body).decode()

        # Desserializa a string JSON para um dicionário Python
        response_content = json.loads(response_body)

        # Cria uma nova resposta JSON com o conteúdo desserializado
        response = JSONResponse(content=response_content)
        
        # Armazena a resposta no Redis como string JSON
        redis_client.setex(cache_key, 5, response_body)

    return response
    