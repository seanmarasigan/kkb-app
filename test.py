import streamlit as st

# Function to clear input
def clear_text():
    st.session_state.input_text = ""  # Reset session state

# Text input with key
st.text_input("Enter something:", key="input_text")

# Button with on_click event
st.button("Reset", on_click=clear_text)
