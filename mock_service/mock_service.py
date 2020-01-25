import asyncio
import os
import uuid

import httpx
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import uvicorn
import logging

app = Starlette()
client = httpx.AsyncClient()
CALLBACK_URL = os.environ["CALLBACK_URL"]
logger = logging.getLogger(__name__)


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

    authHardcoded = {"joe-packham" : "pwd1", "nisarg-mehta" : "pwd2", "fabio-tamagno" : "pwd3"}
    password = authHardcoded.get(usernameJson)
    if password == None:
        logger.warning("Username not found")
        return JSONResponse(False)

    if password == passwordJson:
        return JSONResponse(True)
    else:
        logger.warning("Password does not match")
        return JSONResponse(False)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
