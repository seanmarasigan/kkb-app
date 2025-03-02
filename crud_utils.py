import streamlit as st

def add_member(session_state, kkb_member):
    """Adds a member to the kkb_group."""
    if kkb_member:
        session_state.kkb_group[kkb_member] = kkb_member
        session_state.kkb_member_input = ""  # Clear the input field
        st.rerun()

def edit_member(session_state, key, new_name):
    if key in session_state.kkb_group:
        session_state.kkb_group[new_name] = new_name
        del session_state.kkb_group[key]
        session_state.editing = False
        st.rerun()

def delete_member(session_state, key):
    if key in session_state.kkb_group:
        del session_state.kkb_group[key]
        st.rerun()

def clear_text():
    """Reset session state for input text."""
    st.session_state.kkb_member_input = ""