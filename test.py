import streamlit as st

# Define a text input with a key
text_value = st.text_input("Enter some text:", key="my_input")

# Display the current session state value
st.write("Session state value:", st.session_state['my_input'])

# Add a button to force rerun
if st.button("Force rerun"):
    st.experimental_rerun()