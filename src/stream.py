import streamlit as st
import pandas as pd

from json import JSONDecodeError
from query_inbox import get_emails
from parse_email import (
    extract_fields, summarize_email,
    truncate_email, remove_links, remove_email_addresses,
    IC_FIELD_LIST, FF_FIELD_LIST
)
from calendar_event import create_event, format_event_data

from mock_data import mock_extracted_fields

options = ["Free Food", "Events", "Email Brief"]
app_mode = st.sidebar.selectbox("Set App Mode", options)

titles = {
    "Free Food": "Free Food Forecast Filter For Frugal, Food-Festivity-Following Friends",
    "Events": "Inbox to Calendar",
    "Email Brief": "Morning Brief"
}

st.title(titles[app_mode])
num_emails = st.number_input("How many emails to analyze?", value=2)
value_filters = pd.DataFrame(
    [
        {"filter": "from", "value (edit me)": "", "use filter": False },
        {"filter": "subject", "value (edit me)": "", "use filter": False },
        {"filter": "label", "value (edit me)": "", "use filter": False }
    ]
)
with st.expander("Additional Filters"):
    edited_value_filters = st.experimental_data_editor(value_filters, use_container_width=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        starred_flag = st.checkbox("Starred")

    with c2:
        unread_flag = st.checkbox("Unread")

    with c3:
        read_flag = st.checkbox("Read")

    with c4:
        snoozed_flag = st.checkbox("Snoozed")

txt = ''
lol = """---------- Forwarded message --------- From: COE COE-INFO Date: Mon, May 8, 2023 at 3:47 PM Subject: [Ugrad-announce] NSBE Professional Workshop with Santa Barbara Young Black Professionals To: Hello everyone! <span style='color: #FCB0B3'>NSBE (National Society of Black Engineers and Scientists) is having a Professional Workshop on <span style='color: #269EE3'>Wednesday, May 10th at 7:00pm</span> in the <span style='color: #34D1BF'>ESB Room 2001</span>! Brandon Scott from Santa Barbara Young Black Professionals will be giving a presentation on resume building, interview tips and insight on professionalism for potential careers.</span> Come with any professional questions you may have! <span style='color: #7D83FF'>Food will be provided!</span> See the attached flyer for more information. Sincerely, Jasmyn Gellineau NSBE External Vice President _ Ugrad-announce mailing list Ugrad-announce@lists.engr.ucsb.edu https://lists.engr.ucsb.edu/mailman/listinfo/ugrad-announce"""
# st.markdown(lol, unsafe_allow_html=True)

MAX_SUBJ_CHAR_LEN = 60
MAX_EMAIL_LENGTH = 500
MAX_TOKEN_OUTPUT = 300
SUBJ_EXC_LIST = ["Security alert", "Delivery Status Notification"]

COLOUR_MAPPINGS = {
    "Free Food": {
        "is_free_food_event": "#7D83FF",
        "name": "#FCB0B3",
        "location": "#34D1BF",
        "start": "#269EE3",
        "food_type": "#FFEE99"
    },
    "Events": {
        "name": "#FCB0B3",
        "location": "#34D1BF",
        "start": "#269EE3",
    }
}

FIELD_LISTS = {
    "Free Food": FF_FIELD_LIST,
    "Events": IC_FIELD_LIST
}

processed_email_ids = set()

def get_colour_key(mode):
    return (
        "**Colour Mapping**\n"
        + "\n".join([
            f"* {key}: <span style='color: #1D2021; background-color: {val}'>{val}</span>" 
            for key, val in COLOUR_MAPPINGS[mode].items()
        ])
        + "\n---"
    )

def highlight_source(email_txt, fields):
    highlighted = email_txt
    colour_mapping = COLOUR_MAPPINGS[app_mode]
    for field, colour in colour_mapping.items():
        if fields[field]["value"] is None:
            continue
        src = fields[field]["source"]
        if src is not None:
            h_src = f"<span style='color: {colour}'>{src}</span>"
            highlighted = highlighted.replace(src, h_src)
    # print(highlighted)
    return highlighted

def build_analysis_box(subj_line, email_txt, fields):
    with st.expander(f"Subject: {subj_line[:MAX_SUBJ_CHAR_LEN]}..."):
        left_col, right_col = st.columns(2)
        with left_col:
            st.markdown(get_colour_key(app_mode), unsafe_allow_html=True)
            st.markdown(
                highlight_source(email_txt, fields),
                unsafe_allow_html=True
            )
        with right_col:
            st.json(fields)

def build_query_string():
    # query_string = "is:unread"
    query_string = ""
    for _, filter in edited_extra_filters.iterrows():
        if filter["use filter"]:
            query_string += f" {filter['filter']}:{filter['value (edit me)']}"
    if starred_flag:
        query_string += " is:starred"
    if unread_flag:
        query_string += " is:unread"
    if read_flag:
        query_string += " is:read"
    if snoozed_flag:
        query_string += " is:snoozed"
    return query_string if len(query_string) > 0 else None

def remove_by_subject_line(emails):
    return [
        (subj, email) for subj, email in emails
        if not any([exc in subj for exc in SUBJ_EXC_LIST])
    ]

if st.button("Go!"): 
    query_string = build_query_string()
    preprocessed = get_emails(num_emails, query=query_string)

    emails = []
    for id, email_dict in preprocessed.items():
        email = email_dict["body"]
        if id not in processed_email_ids:
            processed_email_ids.add(id)
            truncated = truncate_email(email, MAX_EMAIL_LENGTH)
            sans_links = remove_links(truncated)
            cleaned = remove_email_addresses(sans_links)
            emails.append((email_dict["subject"], cleaned))

    emails = remove_by_subject_line(emails)

    if app_mode == "Email Brief":
        for subj, email in emails:
            with st.expander(f"Subject: {subj[:MAX_SUBJ_CHAR_LEN]}..."):
                two_liner = summarize_email(email)
                st.write(two_liner)

    else:
        for i, (subj, email) in enumerate(emails):
            
            try:
                fields = extract_fields(email, fields=FIELD_LISTS[app_mode], max_tokens=MAX_TOKEN_OUTPUT)
                print(email)
                print(fields)
                # fields = mock_extracted_fields[i % len(mock_extracted_fields)]
                
                continue_field = "is_free_food_event" if app_mode == "Free Food" else "is_event"
                if fields[continue_field]["value"]:
                    event_data = format_event_data(fields)
                    success = create_event(event_data)
                    if success:
                        build_analysis_box(subj, email, fields)
            except JSONDecodeError:
                print(f"Failed to decode expected JSON output from GPT on index {i}")
            except TypeError as e:
                print(f"GPT probably messed up the output formatting again (index {i})")
                print(e)

# # Create a sidebar with some options

# # st.button("Go!")

# # Show some data based on the selected option
# if selected_option == "Option 1":
#     st.write("You selected Option 1.")
# elif selected_option == "Option 2":
#     st.write("You selected Option 2.")
# else:
#     st.write("You selected Option 3.")

