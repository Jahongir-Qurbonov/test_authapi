from multiprocessing import freeze_support
import uvicorn
from main import app


if __name__ == '__main__':
    freeze_support()
    uvicorn.run('main:app', reload=True)
