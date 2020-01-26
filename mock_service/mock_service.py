import asyncio
import os
import uuid

import httpx
from prometheus_client import start_http_server, Summary, Counter
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import uvicorn
import logging

app = Starlette()
client = httpx.AsyncClient()
CALLBACK_URL = os.environ["CALLBACK_URL"]
logger = logging.getLogger(__name__)

# prometheus metric 1 - general information about time and count of function calls
AUTH_TIME = Summary('request_processing_seconds', 'Time spent processing authentication')
# prometheus metric 2 - failures authenticing
AUTH_FAILED = Counter('auth_failures', 'Failed authentication attempts')

@app.route("/api/endpoint", methods=["POST"])
async def fake_endpoint(request):
    identifier = str(uuid.uuid4())
    payload = {
        "identifier": identifier,
        "some_parameter": request.query_params.get("some_parameter"),
    }
    task = BackgroundTask(trigger_webhook, payload)
    return JSONResponse(
        {"identifier": identifier, "success": True}, background=task)


async def trigger_webhook(payload):
    await asyncio.sleep(5)
    params = {
        "success": True,
        "identifier": payload["identifier"],
        "some_parameter": payload["some_parameter"],
    }
    await client.get(CALLBACK_URL, params=params)

@app.route("/auth", methods=["POST"])
async def auth(request):

    data = await request.json()
    try:
        usernameJson = data['username']
        passwordJson = data['password']
    except KeyError:
        logger.warning("Auth payload did not contain username and password")
        return JSONResponse(False)
    return process_auth(usernameJson, passwordJson)

@AUTH_TIME.time()
def process_auth(usernameJson, passwordJson):
    authHardcoded = {"joe-packham" : "pwd1"}
    password = authHardcoded.get(usernameJson)
    if password == None:
        logger.warning("Username not found")
        AUTH_FAILED.inc(1)
        return JSONResponse(False)

    if password == passwordJson:
        return JSONResponse(True)
    else:
        logger.warning("Password does not match")
        AUTH_FAILED.inc(1)
        return JSONResponse(False)

if __name__ == "__main__":
    # start prometheus logging on 8081
    start_http_server(8081)
    # start mock_service on 8080
    uvicorn.run(app, host="0.0.0.0", port=8080)
