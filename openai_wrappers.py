import openai
import os
import json
import time
from dotenv import load_dotenv
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_random_exponential
# from transformers import GPT2Tokenizer

load_dotenv()
openai.api_key = os.getenv('MSHO_OPENAI_API_KEY')

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def codex_completion(prompt, completion_length, text_only=False, **kwargs):
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=completion_length,
        **kwargs
    )
    res_obj = json.loads(str(response))
    if text_only:
        text_choices = [choice["text"] for choice in res_obj["choices"]]
        return text_choices[0] if len(text_choices) == 1 else text_choices
    return res_obj

# OpenAI currently limits logprobs to 5
def codex_multichoice(prompt, choices, top_k=5):
    # TODO: use GPT-2 tokenizer to determine completion length (max token length of choices)
    res = codex_completion(prompt, completion_length=2, logprobs=top_k)
    top_tokens = res["choices"][0]["logprobs"]["top_logprobs"][1]
    top_choices = {c: top_tokens[c] for c in choices if c in top_tokens}
    if len(top_choices) == 0:
        return None
    return max(top_choices.keys(), key=top_choices.get)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def text_completion(generation_args, text_only=False):
    response = openai.Completion.create(**generation_args)
    res_obj = json.loads(str(response))
    if text_only:
        text_choices = [choice["text"] for choice in res_obj["choices"]]
        return text_choices[0] if len(text_choices) == 1 else text_choices
    return res_obj

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def chat_completion(generation_args, text_only=False):
    response = openai.ChatCompletion.create(**generation_args)
    res_obj = json.loads(str(response))
    if text_only:
        text_choices = [choice["text"]["message"]["content"] for choice in res_obj["choices"]]
        return text_choices[0] if len(text_choices) == 1 else text_choices
    return res_obj
