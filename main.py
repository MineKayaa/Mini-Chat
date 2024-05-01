from fastapi import FastAPI 
import dal.dal as dal
import services.chatbot as chatbot

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/chat/")
async def chat(input: str, chat_id: str | None = None):
    output = chatbot.chatbotService.ask_question(input, chat_id)
    return {"message": output}

@app.get("/get-messages")
async def chat(chat_id: str):
    messages = dal.dal.get_messages(chat_id)
    return {"message_history": messages}