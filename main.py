from fastapi import FastAPI 
import dal.dal as dal

app = FastAPI()


@app.get("/")
async def root():
    dal.dal.get_messages("1")
    return {"message": "Hello World"}