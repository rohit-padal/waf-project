from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def demo(request:Request, call_next):
    print("Starting WAF...") 

    # 1. HTTP method
    print("Method: ", request.method)

    # 2. URL path
    print("Path: ", request.url.path)

    # 3. Query parameters
    print("Parameters: ", request.query_params)

    # 4. Request headers
    print("User-Agent: ", request.headers.get("user-agent"))
    print("Content-Type: ", request.headers.get("content-type"))

    # 5. Request body
    body = await request.body()
    print("Body bytes: ", body)

    # Let the request continue to the route
    async def receive():
        return {
            "type": "http.request",
            "body": body,
            "more_body": False,
        }
    request._receive = receive


    response = await call_next(request)
    return response

@app.get("/search")
async def search(q:str=""):
    return {"received_query": q}

@app.post("/comment")
async def comment(request: Request):
    body = await request.json()
    return {"received_body": body}