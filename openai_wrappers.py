import openai
import json
from constants import *
from copy import deepcopy
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_random_exponential

class OpenAIWrapper:
    # singleton class
    _instance = None

    def __new__(cls, api_key):
        openai.api_key = api_key
        if cls._instance is None:
             cls._instance = super().__new__(cls)
        return cls._instance
         
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def text_completion(self, generation_args, text_only=False):
        response = openai.Completion.create(**generation_args)
        res_obj = json.loads(str(response))
        if text_only:
            text_choices = [choice["text"] for choice in res_obj["choices"]]
            return text_choices[0] if len(text_choices) == 1 else text_choices
        return res_obj

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def chat_completion(self, generation_args):
        response = openai.ChatCompletion.create(**generation_args)
        return json.loads(str(response))

    def get_text_from_completion(self, cmp):
        text_choices = [choice["message"]["content"] for choice in cmp["choices"]]
        return text_choices[0] if len(text_choices) == 1 else text_choices

    def chat_gpt_completion(self, chat_history, max_tokens):
        completion_args = deepcopy(CHATGPT_ARGS)
        completion_args["messages"] = chat_history
        completion_args["max_tokens"] = max_tokens
        # return chat_completion(completion_args, text_only=True)
        completion = self.chat_completion(completion_args)
        return self.get_text_from_completion(completion)
