import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from read_email import get_emails
from parse_email import is_food_event, extract_fields
from calendar_event import create_event, convert_json

app = Flask(__name__)
CORS(app)

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

@app.route("/email2calendar", methods=["POST"])
def email2calendar():
    request_data = request.json
    num_emails = request_data.get("num_emails", 10)
    max_email_length = request_data.get("max_email_length", 500)
    max_extract_tokens = request_data.get("max_extract_tokens", 300)
    processed_email_ids = set(request_data.get("processed_email_ids", []))

    emails = get_emails(num_emails)
    email_txt = []
    for id, email in emails.items():
        if id not in processed_email_ids:
            processed_email_ids.add(id)
            email_txt.append(truncate_email(email, max_email_length))

    for email in email_txt:
        # print(email)
        if is_food_event(email):
            fields = extract_fields(email, max_tokens=max_extract_tokens)
            reformatted = reformat_fields_for_calendar_event(fields)
            create_event(convert_json(reformatted))

    return jsonify(processed=list(processed_email_ids))

if __name__ == '__main__':
    app.run(debug=True)
