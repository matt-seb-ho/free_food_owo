import streamlit as st
import json
from query_inbox import get_emails
from parse_email import extract_fields, truncate_email, remove_links
from calendar_event import create_event, format_event_data

from mock_data import mock_extracted_fields

def jspp(dict):
    print(json.dumps(dict, indent=2))

# Create a header for your app
st.title("Free Food Forecast Filter For Food-Following Friends")
num_emails = st.number_input("How many emails to analyze?", value=2)
txt = ''
st.write(txt)

MAX_EMAIL_LENGTH = 500
MAX_TOKEN_OUTPUT = 300
processed_email_ids = set()

COLOUR_MAPPING = {
    "is_free_food_event": "#7D83FF",
    "name": "#FCB0B3",
    "location": "#34D1BF",
    "start": "#269EE3",
    "food_type": "#FFEE99"
}

colour_key = (
    "**Colour Mapping**\n"
    + "\n".join([
        f"* {key}: <span style='color: #1D2021; background-color: {val}'>{val}</span>" 
        for key, val in COLOUR_MAPPING.items()
    ])
    + "\n---"
)

def highlight_source(email_txt, fields):
    highlighted = email_txt
    for field, colour in COLOUR_MAPPING.items():
        src = fields[field]["source"]
        if src is not None:
            h_src = f"<span style='color: {colour}'>{src}</span>"
            # print(src, h_src)
            highlighted = highlighted.replace(src, h_src)
    return highlighted

def build_analysis_box(email_number, email_txt, fields):
    with st.expander(f"Email {email_number}"):
        left_col, right_col = st.columns(2)
        with left_col:
            st.markdown(colour_key, unsafe_allow_html=True)
            st.markdown(
                highlight_source(email_txt, fields),
                unsafe_allow_html=True
            )
        with right_col:
            st.json(fields)

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
        # fields = extract_fields(email, max_tokens=MAX_TOKEN_OUTPUT)
        fields = mock_extracted_fields[i % len(mock_extracted_fields)]

        if fields["is_free_food_event"]["value"]:
            event_data = format_event_data(fields)
            # jspp(event_data)
            success = create_event(event_data)
            if success:
                build_analysis_box(i, email, fields)
                event_count += 1

# # Create a sidebar with some options
# options = ["Option 1", "Option 2", "Option 3"]
# selected_option = st.sidebar.selectbox("Select an option", options)

# # st.button("Go!")

# # Show some data based on the selected option
# if selected_option == "Option 1":
#     st.write("You selected Option 1.")
# elif selected_option == "Option 2":
#     st.write("You selected Option 2.")
# else:
#     st.write("You selected Option 3.")

