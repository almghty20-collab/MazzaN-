from fastapi import FastAPI, Request

app = FastAPI()

VERIFY_TOKEN = "12345"

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return {"error": "Token inválido"}

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print(data)
    return {"status": "ok"}
