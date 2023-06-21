import uvicorn
from fastapi import FastAPI
from config import Config

app = FastAPI()


if __name__ == '__main__':
    uvicorn.run('main:app', host=str(Config.host), port=Config.port, reload=True)
