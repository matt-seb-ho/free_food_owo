import argparse
import json
from read_email import get_emails
from parse_email import is_food_event, extract_fields
from calendar_event import create_event, convert_json
from datetime import datetime, timedelta

ACTUALLY_DO_IT = False

def jspp(dict):
    print(json.dumps(dict, indent=2))

def reformat_fields_for_calendar_event(fields):
    rfmtd = {k: v["value"] for k, v in fields.items()}

    rfmtd["start"] = rfmtd["start"].rstrip("Z")
    
    if rfmtd["end"] is None:
        start = datetime.fromisoformat(rfmtd["start"])
        end = start + timedelta(hours=1)
        rfmtd["end"] = end.isoformat().rstrip('Z')
    else:
        rfmtd["end"] = rfmtd["end"].rstrip("Z")
    
    return rfmtd

def truncate_email(email, max_words):
    return ' '.join(email.split()[:max_words])

dummy_ext = {
  "name": "HRL Laboratories Professionalism Workshop",
  "start": "2023-05-11T18:00:00.000",
  "end": "2023-05-11T19:00:00",
  "location": "ESB 1001"
}

if __name__ == "__main__":
    psr = argparse.ArgumentParser()
    psr.add_argument("--num_emails", "-ne", type=int, default=10)
    psr.add_argument("--max_email_length", "-mel", type=int, default=500, help="in words")
    psr.add_argument("--extract_max_tokens", "-emt", type=int, default=300)
    psr.add_argument("--ignore_first", "-if", type=int, default=0)
    psr.add_argument("--dont_dedup", "-ddd", action='store_false')
    args = psr.parse_args()

    """
    # max token length

    chat gpt has token limit of 4096 tokens
    1 token is ~3/4 word
    4096 * 3/4 = 3072 words

    """

    emails = get_emails(args.num_emails)

    if args.dont_dedup:
        with open("processed_email_cache.json") as f:
            processed_email_ids = set(json.load(f)["ids"])
    else:
        processed_email_ids = set()

    email_txt = []
    for id, email in emails.items():
        if id not in processed_email_ids:
            processed_email_ids.add(id)
            email_txt.append(truncate_email(email, args.max_email_length))

    if not args.dont_dedup:
        with open("processed_email_cache.json", "w") as f:
            json.dump({"ids": list(processed_email_ids)}, f)

    for i, email in enumerate(email_txt[args.ignore_first:]):
        print(email)
        if is_food_event(email):
            fields = extract_fields(email, max_tokens=args.extract_max_tokens)
            reformatted = reformat_fields_for_calendar_event(fields)
            print("no converted")
            jspp(reformatted)
            print("converted")
            jspp(convert_json(reformatted))
            create_event(convert_json(reformatted))
