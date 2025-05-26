import streamlit as st
# import nltk
# from nltk.tokenize import sent_tokenize

# Ensure nltk sentence tokenizer is available
# nltk.download("punkt")

# --- Configuration ---
LABELS = ["-","Informative", "Question", "Opinion", "Irrelevant"]
st.set_page_config(layout="wide")

# --- Input Document ---
st.title("Sentence Labeling Interface")

doc = "This is the first sentence. Here is another one. What do you think about it? This could be useful."


# st.markdown("""
#     <style>
#     div[data-baseweb="select"] > div {
#         min-height: 10px;
#     }
#     div[data-baseweb="select"] span {
#         font-size: 0.5rem;
#     }
#     </style>
# """, unsafe_allow_html=True)

if doc:
    # Split into sentences
    sentences = doc.split(".")

    st.subheader("Label each sentence:")

    labeled_data = {}
    for idx, sentence in enumerate(sentences):
        cols = st.columns([1, 9])  # Dropdown (1) + Sentence (9)

        with cols[0]:
            label = st.selectbox(
                label="Label",
                options=LABELS,
                key=f"label_{idx}",
                label_visibility="collapsed"
            )
        with cols[1]:
            st.markdown(f"""
    <div style="padding-top: 6px;">
        <code>{sentence}</code>
    </div>
""", unsafe_allow_html=True)
        
        labeled_data[sentence] = label

    # st.subheader("Labeled Output")
    # st.json(labeled_data)