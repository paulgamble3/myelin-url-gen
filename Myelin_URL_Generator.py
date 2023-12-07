import streamlit as st
import random
import glob
import json

from firebase.firebase_utils import write_task_item

def sample_call_url():
    call_configs = glob.glob("./call_configs/*.json")
    call_config_fn = random.choice(call_configs)
    with open(call_config_fn) as f:
        call_config = json.load(f)
    call_cfg = random.choice(call_config)
    call_url = call_cfg["url"]

    call_type = call_config_fn.split("/")[-1][5:-5]
    call_type = call_type.replace("_", " ")
    return call_url, call_type



FIREBASE_DB = "12-7-dosage-calls"

st.header("Dosage Engine Questions")


with st.form("url-gen-form"):

    def log_call():
        feedback_obj = {
            "call_id": st.session_state.call_id,
            "username": st.session_state.username
        }
        write_task_item(feedback_obj, FIREBASE_DB)
        #reset call_id
        st.session_state.call_id = ""
        #st.experimental_rerun()
    
    call_url, call_type = sample_call_url()

    st.text_input("Enter your name:", key='username')
    st.subheader("[CALL URL]({})".format(call_url))
    #st.write("Call type: " + call_type.strip())
    #st.write("After a few openings lines and introductions, please ask a hospital policy question from the provided list.")
    call_id = st.text_input("Please copy and paste the call ID:", key="call_id")
    
    submit_button = st.form_submit_button(label='Log call', on_click=log_call)



