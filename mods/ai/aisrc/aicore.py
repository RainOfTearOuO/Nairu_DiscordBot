import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
APIKEY = os.environ.get("APIKEY")
SYS_PROMPT = os.environ.get("SYS_PROMPT")
MAX_CHAT_HISTORY_LENGTH = 2*3  # Maximum number of messages to keep in chat history

class NairuManager:
    def __init__(self, model):
        self.model = model
        self._channel_chat_history = {}

    def send_to_ai(self, user_input: str, channel_id: str) -> str:
        try:
            if channel_id not in self._channel_chat_history:
                self._channel_chat_history[channel_id] = self.model.start_chat()
            chat = self._channel_chat_history[channel_id]

            if len(chat.history) > MAX_CHAT_HISTORY_LENGTH:
                chat.history = chat.history[-MAX_CHAT_HISTORY_LENGTH:]

            response = chat.send_message(user_input)
            return response.text
        except Exception as e:
            if channel_id in self._channel_chat_history:
                chat = self._channel_chat_history[channel_id]
                if not chat.history:
                    self._channel_chat_history.pop(channel_id)
            raise e

    def clear_channel_chat_history(self, channel_id: str):
        try:
            self._channel_chat_history.pop(channel_id)
            return True
        except Exception as e:
            return False

    def show_channel_chat_history(self, channel_id: str): 
        if channel_id in self._channel_chat_history:
            return self._channel_chat_history[channel_id].history
        else:
            return None


def build_nairu_manager():
    genai.configure(api_key=APIKEY)
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        safety_settings=None,
        system_instruction=SYS_PROMPT
    )
    return NairuManager(model)



