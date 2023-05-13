import openai
import json
from constants import *
from parse_fields import ParseField, format_field_list
from copy import deepcopy
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_random_exponential
from config import OPENAI_API_KEY, MSHO_OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
# openai.api_key = MSHO_OPENAI_API_KEY

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def text_completion(generation_args, text_only=False):
    response = openai.Completion.create(**generation_args)
    res_obj = json.loads(str(response))
    if text_only:
        text_choices = [choice["text"] for choice in res_obj["choices"]]
        return text_choices[0] if len(text_choices) == 1 else text_choices
    return res_obj

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def chat_completion(generation_args):
    response = openai.ChatCompletion.create(**generation_args)
    return json.loads(str(response))

def get_text_from_completion(cmp):
    text_choices = [choice["message"]["content"] for choice in cmp["choices"]]
    return text_choices[0] if len(text_choices) == 1 else text_choices

def chat_gpt_completion(chat_history, max_tokens):
    completion_args = deepcopy(CHATGPT_ARGS)
    completion_args["messages"] = chat_history
    completion_args["max_tokens"] = max_tokens
    # return chat_completion(completion_args, text_only=True)
    completion = chat_completion(completion_args)
    return get_text_from_completion(completion)

SAVE_TO_FILE = False

def is_food_event(email_txt):
    prompt = IS_FF_EVENT_TEMPLATE.format(email=email_txt)
    chat_history = [{"role": "user", "content": prompt}]
    completion = chat_gpt_completion(chat_history, max_tokens=3)
    print(completion)
    if SAVE_TO_FILE:
        with open("save_res.json", 'w') as f:
            json.dump(completion, f, indent=2)
    return completion == "True"

NAME_FIELD = ParseField("name", "The name of the event", "string")
DATE_TIME_START_FIELD = ParseField("date_time_start", "The start date and time of the event", "Date")
LOCATION_FIELD = ParseField("location", "The location of the event", "string")
DEFAULT_FIELD_LIST = [NAME_FIELD, DATE_TIME_START_FIELD, LOCATION_FIELD]

def extract_fields(txt, fields=DEFAULT_FIELD_LIST):
    string_fields = format_field_list(fields)
    chat_history = [
        { 
            "role": "system", 
            "content": PARSE_SYS_TEMPLATE.format(string_fields=string_fields)
        },
        {
            "role": "user",
            "content": PARSE_USER_TEMPLATE.format(document=txt)
        }
    ]
    completion = chat_gpt_completion(chat_history, max_tokens=300)
    try:
        if isinstance(completion, str):
            completion = json.loads(completion)
        else:
            completion = json.loads(completion[0])
    except json.JSONDecodeError as e:
        print(completion)
        raise e

    return completion
