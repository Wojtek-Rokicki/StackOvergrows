from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "skrypt1"}

@app.get("/test")
async def get_test():
    print('test started')
    await asyncio.sleep(1)
    print('test ended')
    return {"Hello": "skrypt1 test"}