import argparse
import json
from query_inbox import get_emails
from parse_email import extract_fields, truncate_email
from calendar_event import create_event, format_event_data

def jspp(dict):
    print(json.dumps(dict, indent=2))

dummy_ext = {
  "name": "HRL Laboratories Professionalism Workshop",
  "start": "2023-05-11T18:00:00.000",
  "end": "2023-05-11T19:00:00",
  "location": "ESB 1001"
}

PREPROCESSED_EMAILS = "../data/preprocessed_emails.json"

if __name__ == "__main__":
    psr = argparse.ArgumentParser()
    psr.add_argument("--num_emails", "-ne", type=int, default=10)
    psr.add_argument("--max_email_length", "-mel", type=int, default=500, help="in words")
    psr.add_argument("--extract_max_tokens", "-emt", type=int, default=300)
    psr.add_argument("--ignore_first", "-if", type=int, default=0)
    psr.add_argument("--do_not_deduplicate", "-dnd", action='store_false')
    args = psr.parse_args()

    """
    # max token length

    chat gpt has token limit of 4096 tokens
    1 token is ~3/4 word
    4096 * 3/4 = 3072 words

    """

    preprocessed = get_emails(args.num_emails)

    if args.do_not_deduplicate:
        with open(PREPROCESSED_EMAILS) as f:
            processed_email_ids = set(json.load(f)["ids"])
    else:
        processed_email_ids = set()

    emails = []
    for id, email in preprocessed.items():
        if id not in processed_email_ids:
            processed_email_ids.add(id)
            emails.append(truncate_email(email, args.max_email_length))

    if not args.do_not_deduplicate:
        with open(PREPROCESSED_EMAILS, 'w') as f:
            json.dump({"ids": list(processed_email_ids)}, f)

    for i, email in enumerate(emails[args.ignore_first:]):
        print(email)
        fields = extract_fields(email, max_tokens=args.extract_max_tokens)
        if fields["is_free_food_event"]["value"]:
            event_data = format_event_data(fields)
            create_event(event_data)
