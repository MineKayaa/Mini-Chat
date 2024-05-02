import helpers.utils as utils
import dal.dal as dal

class chatbotService:
    def ask_question(input : str, chat_id : str):
        chat_history = ""
        #if chat_id is empty create new chat_id
        if (chat_id == None or chat_id == "") :
            chat_id = str(dal.dal.get_last_chat_id() + 1)
        #else get chat history for current chat_id
        else :
            chat_history = dal.dal.get_messages(chat_id)
            print(chat_history)
    
        ai_message =  utils.utils.get_agent(input, chat_history)

        dal.dal.insert_message(chat_id, ai_message , input)
        return  ai_message



