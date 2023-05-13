import argparse
import json
from read_email import get_emails
from parse_email import is_food_event, extract_fields
from calendar_event import create_events
from datetime import datetime, timedelta

def reformat_fields_for_calendar_event(fields):
    rfmtd = {k: v["value"] for k, v in fields.items()}

    rfmtd["start"] = rfmtd["start"][:-1]
    
    if rfmtd["end"] is None:
        start = datetime.fromisoformat(rfmtd["start"])
        end = start + timedelta(hours=1)
        rfmtd["end"] = end.isoformat()
    
    return rfmtd

if __name__ == "__main__":
    psr = argparse.ArgumentParser()
    psr.add_argument("--num_emails", "-ne", type=int, default=10)
    psr.add_argument("--extract_max_tokens", "-emt", type=int, default=300)
    args = psr.parse_args()

    emails = get_emails(args.num_emails)
    for email in emails:
        print(email)
        # if True:
        if is_food_event(email):
            print("food event detected!")
            fields = extract_fields(email, max_tokens=args.extract_max_tokens)
            reformatted = reformat_fields_for_calendar_event(fields)
            print(reformatted)
            print(json.dumps(reformatted, indent=2))
            # create_events(reformatted)
