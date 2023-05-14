import streamlit as st
import json
from query_inbox import get_emails
from parse_email import extract_fields, truncate_email, remove_links
from calendar_event import create_event, format_event_data

def jspp(dict):
    print(json.dumps(dict, indent=2))

# Create a header for your app
st.title("Free Food Finder for Fat Fucks")
num_emails = st.number_input("How many emails to analyze?", value=10)
txt = ''
st.write(txt)

MAX_EMAIL_LENGTH = 500
MAX_TOKEN_OUTPUT = 300
processed_email_ids = set()

if st.button("Go!"): 
        # if "clicked" in st.session_state:
        #     st.warning("already clicked")
        #     return
        # st.session_state.clicked = True
            
    preprocessed = get_emails(num_emails)
    emails = []
    for id, email in preprocessed.items():
        if id not in processed_email_ids:
            processed_email_ids.add(id)
            truncated = truncate_email(email, MAX_EMAIL_LENGTH)
            cleaned = remove_links(truncated)
            emails.append(cleaned)

    event_count = 0
    for i, email in enumerate(emails):
        print(email)
        fields = extract_fields(email, max_tokens=MAX_TOKEN_OUTPUT)
        if fields["is_free_food_event"]["value"]:
            event_data = format_event_data(fields)
            jspp(event_data)
            success = create_event(event_data)
            if success:
                event_count += 1

    if event_count == 0:
        st.error("No events created :(")
    else:
        st.success("Successfully created events!")

    for email in emails:
        st.text(email)

"""
Starter Code (saving for later)

"""

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
