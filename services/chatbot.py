from langchain_core.prompts import ChatPromptTemplate
import helpers.utils as utils
import dal.dal as dal

class chatbotService:
    def ask_question(input : str, chat_id : str):
        llm = utils.utils.get_model()
        chat_history = ""
        #if chat_id is empty create new chat_id
        if (chat_id == None or chat_id == "") :
            print("aaa")
            chat_id = str(dal.dal.get_last_chat_id() + 1)
        #else get chat history for current chat_id
        else :
            chat_history = dal.dal.get_messages(chat_id)
            print(chat_history)
        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Here is the chat history {chat_history}.",
                ),
                ("human", "{input}"),
            ]
        )

        chain = prompt | llm
        output = chain.invoke(
            {
                "chat_history": chat_history,
                "input": input,
            }
        )

        print(output)
        ai_message = output.content

        dal.dal.insert_message(chat_id, ai_message , input)
        return  ai_message



