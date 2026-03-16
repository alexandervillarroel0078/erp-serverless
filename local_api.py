from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from lambdas.clientes.handler import lambda_handler as clientes_handler
from lambdas.compras.handler import lambda_handler as compras_handler
from lambdas.inventario.handler import lambda_handler as inventario_handler
from lambdas.ventas.handler import lambda_handler as ventas_handler

app = FastAPI(title="Local API Gateway Simulator")


def build_event(request: Request, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Construye un evento compatible con Lambda/API Gateway."""
    return {
        "httpMethod": request.method,
        "path": request.url.path,
        "headers": dict(request.headers),
        "queryStringParameters": dict(request.query_params),
        "pathParameters": {},
        "body": body or {},
        "isBase64Encoded": False,
        "requestContext": {
            "http": {
                "method": request.method,
                "path": request.url.path,
                "protocol": "HTTP/1.1",
                "sourceIp": request.client.host if request.client else "127.0.0.1",
            }
        },
    }


def run_lambda(handler, event):
    """Ejecuta la lambda y convierte la respuesta en FastAPI JSONResponse."""
    response = handler(event, None)

    if not isinstance(response, dict):
        raise HTTPException(status_code=500, detail="Lambda returned invalid response format")

    status_code = int(response.get("statusCode", 200))
    headers = response.get("headers", {}) or {}
    body = response.get("body", {})

    if isinstance(body, str):
        try:
            import json

            body = json.loads(body)
        except Exception:
            pass

    return JSONResponse(status_code=status_code, content=body, headers=headers)


@app.post("/clientes")
async def post_clientes(request: Request):
    payload = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    event = build_event(request, payload)
    return run_lambda(clientes_handler, event)


@app.post("/ventas")
async def post_ventas(request: Request):
    payload = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    event = build_event(request, payload)
    return run_lambda(ventas_handler, event)


@app.post("/compras")
async def post_compras(request: Request):
    payload = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    event = build_event(request, payload)
    return run_lambda(compras_handler, event)


@app.post("/inventario")
async def post_inventario(request: Request):
    payload = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    event = build_event(request, payload)
    return run_lambda(inventario_handler, event)


@app.get("/clientes")
async def get_clientes(request: Request):
    event = build_event(request)
    return run_lambda(clientes_handler, event)


@app.get("/ventas")
async def get_ventas(request: Request):
    event = build_event(request)
    return run_lambda(ventas_handler, event)


@app.get("/compras")
async def get_compras(request: Request):
    event = build_event(request)
    return run_lambda(compras_handler, event)


@app.get("/inventario")
async def get_inventario(request: Request):
    event = build_event(request)
    return run_lambda(inventario_handler, event)
