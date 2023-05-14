import streamlit as st
import argparse
import json
from read_email import get_emails
from parse_email import is_food_event, extract_fields
from calendar_event import create_event, convert_json
from datetime import datetime, timedelta

def jspp(dict):
    print(json.dumps(dict, indent=2))

def reformat_fields_for_calendar_event(fields):
    rfmtd = {k: v["value"] for k, v in fields.items()}

    start = datetime.fromisoformat(rfmtd["start"].rstrip("Z"))
    start = start.replace(year=datetime.now().year)
    rfmtd["start"] = start.isoformat().rstrip("Z")
    
    if rfmtd["end"] is None:
        end = start + timedelta(hours=1)
        rfmtd["end"] = end.isoformat().rstrip('Z')
    else:
        end = datetime.fromisoformat(rfmtd["end"].rstrip("Z"))
        end = end.replace(year=start.year)
        rfmtd["end"] = end.isoformat().rstrip("Z")
    
    return rfmtd

def truncate_email(email, max_words):
    return ' '.join(email.split()[:max_words])

# Create a header for your app
st.title("Free Food Finder for Fat Fucks")
num_emails = st.number_input("How many emails to analyze?", value=10)
txt = ''
st.write(txt)

processed_email_ids = set()

    # def run(mel=500, emt=300):
if st.button("Go!"): 
        # if "clicked" in st.session_state:
        #     st.warning("already clicked")
        #     return
        # st.session_state.clicked = True
            
    emails = get_emails(num_emails)
    email_txt = []
    for id, email in emails.items():
        if id not in processed_email_ids:
            processed_email_ids.add(id)
            email_txt.append(truncate_email(email, 500))
    
    event_count = 0
    for email in email_txt:
        print(email)
        if is_food_event(email):
            fields = extract_fields(email, max_tokens=300)
            reformatted = reformat_fields_for_calendar_event(fields)
            jspp(convert_json(reformatted))
            success = create_event(convert_json(reformatted))
            if success:
                event_count += 1

    if event_count == 0:
        st.error("No events created :(")
    else:
        st.success("Successfully created events!")

    for email in email_txt:
        st.text(email)

# Create a sidebar with some options
options = ["Option 1", "Option 2", "Option 3"]
selected_option = st.sidebar.selectbox("Select an option", options)

# st.button("Go!")

# Show some data based on the selected option
if selected_option == "Option 1":
    st.write("You selected Option 1.")
elif selected_option == "Option 2":
    st.write("You selected Option 2.")
else:
    st.write("You selected Option 3.")

