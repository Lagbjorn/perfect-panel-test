import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import config
from api.v1 import vk
from api.v1.schemas.response.response import ErrorResponse, Status
from services.blocklist import SimpleBlocklist

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=config.DOCS_URL,
    openapi_url=config.DOCS_URL + ".json",
)

app.include_router(vk.router, prefix="/api/v1")

blocklist = SimpleBlocklist()


@app.middleware("http")
async def limit_ip_calls(request: Request, call_next):
    ip = request.client.host
    if blocklist.check(ip):
        return JSONResponse(
            ErrorResponse(
                status=Status.ERROR,
                code=403,
                message='Too many requests',
            ).dict(),
            status_code=403,
        )
    blocklist.add(ip)
    response = await call_next(request)
    blocklist.remove(ip)
    return response

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.APP_PORT,
        reload=config.DEBUG,
    )
