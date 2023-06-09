import json
import re

from config import OPENAI_API_KEY
from constants import PARSE_SYS_TEMPLATE, PARSE_USER_TEMPLATE, SYS_SANS_CONFIDENCE, COMBINED_TEMPLATE
from openai_wrappers import OpenAIWrapper
from parse_utils import (
    ParseField,
    format_field_list,
    # remove_punctuation
)

openai_wrapper = OpenAIWrapper(OPENAI_API_KEY)

IS_FF_EVENT_FIELD = ParseField("is_free_food_event", "Whether the email describes an event with free food", "boolean")
IS_EVENT_FIELD = ParseField("is_event", "Is this email is an event invitation", "boolean")
NAME_FIELD = ParseField("name", "The name of the event", "string")
START_FIELD = ParseField("start", "The start date and time of the event", "Date")
END_FIELD = ParseField("end", "The end date and time of the event", "Date")
LOCATION_FIELD = ParseField("location", "The location of the event", "string")
FOOD_TYPE_FIELD = ParseField("food_type", "The type of food at the event", "string")
FF_FIELD_LIST = [IS_FF_EVENT_FIELD, NAME_FIELD, START_FIELD, END_FIELD, LOCATION_FIELD, FOOD_TYPE_FIELD]
IC_FIELD_LIST = [IS_EVENT_FIELD, NAME_FIELD, START_FIELD, END_FIELD, LOCATION_FIELD]

def remove_links(text):
    """
    - Define a regular expression pattern to match links
    - Use the re.sub() function to replace all matches of the link pattern with an empty string

    """
    link_pattern = r'<https?://\S+>'
    return re.sub(link_pattern, '', text)

def remove_email_addresses(text):
    email_address_pattern = r'<\S+@\S+>'
    return re.sub(email_address_pattern, '', text)

def truncate_email(email, max_words):
    return ' '.join(email.split()[:max_words])

def extract_fields(txt, fields=FF_FIELD_LIST, max_tokens=300):
    # prepare prompt
    string_fields = format_field_list(fields)
    # chat_history = [
    #     { 
    #         "role": "system", 
    #         # "content": PARSE_SYS_TEMPLATE.format(string_fields=string_fields)
    #         "content": SYS_SANS_CONFIDENCE.format(string_fields=string_fields)
    #     },
    #     {
    #         "role": "user",
    #         "content": PARSE_USER_TEMPLATE.format(document=txt)
    #     }
    # ]
    chat_history = [{"role": "user", "content": COMBINED_TEMPLATE.format(document=txt, string_fields=string_fields)}]
    
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

def summarize_email(txt, max_tokens=300):
    chat_history = [
        {
            "role": "user",
            "content": f"Email:\n{txt}\n---\nPlease write a 2 sentence summary of this email."
        }
    ]
    summary  = openai_wrapper.chat_gpt_completion(chat_history, max_tokens=max_tokens)
    return summary
