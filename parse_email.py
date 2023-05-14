import json

from config import OPENAI_API_KEY
from constants import PARSE_SYS_TEMPLATE, PARSE_USER_TEMPLATE
from openai_wrappers import OpenAIWrapper
from parse_utils import (
    ParseField,
    format_field_list,
    remove_punctuation
)
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_random_exponential

openai_wrapper = OpenAIWrapper(OPENAI_API_KEY)

IS_FF_EVENT_FIELD = ParseField("is_free_food_event", "Whether the email describes an event with free food", "boolean")
NAME_FIELD = ParseField("name", "The name of the event", "string")
START_FIELD = ParseField("start", "The start date and time of the event", "Date")
END_FIELD = ParseField("end", "The end date and time of the event", "Date")
LOCATION_FIELD = ParseField("location", "The location of the event", "string")
DEFAULT_FIELD_LIST = [NAME_FIELD, START_FIELD, END_FIELD, LOCATION_FIELD]

def truncate_email(email, max_words):
    return ' '.join(email.split()[:max_words])

def extract_fields(txt, fields=DEFAULT_FIELD_LIST, max_tokens=300):
    # prepare prompt
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
    
    # extract info
    completion = openai_wrapper.chat_gpt_completion(chat_history, max_tokens=max_tokens)

    # try to parse the expected JSON format
    try:
        if isinstance(completion, str):
            completion = json.loads(completion)
        else:
            completion = json.loads(completion[0])
    except json.JSONDecodeError as e:
        print(completion)
        raise e

    # handle non-str 
    # is_ff_event = remove_punctuation(completion["is_free_food_event"]).lower() == "true"
    # completion["is_free_food_event"] = is_ff_event

    return completion
