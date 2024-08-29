import streamlit as st
from utils.pdf_handling import extract_text_from_pdf
from utils.chat_history import ChatHistory
from utils.chat_functions import brainstorm_chat

from scripts.generate_content import generate_document

def set_chatbox_layout():
    if "history" not in st.session_state:
        st.session_state["history"] = ChatHistory()
        st.session_state["first_prompt"] = True
        st.session_state["doc_chat_history"] = ChatHistory()
        message = "Hello there! Chat with me to define your document's purpose and content. I will create a detailed outline based on your input, then generate a complete document for you to review and finalize once you click the \"Generate\" button on the left."
        st.session_state["history"].add_assistant_message(message)
    
    if "upload_bool" not in st.session_state:
        st.session_state["upload_bool"] = False

    # Create upload element
    label = "Upload a PDF document"
    uploaded_file = st.file_uploader(label, type="pdf", accept_multiple_files=False, help="Upload your PDF here")#, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")
    st.session_state["uploaded_file"] = uploaded_file
    
    # Handle upload
    if st.session_state["uploaded_file"] and not st.session_state["upload_bool"]:
        st.session_state["upload_bool"] = True
        print("Importing PDF")
        pdf_text = extract_text_from_pdf(st.session_state["uploaded_file"])
        st.session_state["user_context"] = pdf_text
    elif "user_context" not in st.session_state:
        st.session_state["user_context"] = ""
    
    st.title("AI Research Bot")
    
    # Display existing messages in the Streamlit interface
    for msg in st.session_state.history:
        if str(msg["role"]) == "user":
            st.chat_message("human").write(msg["content"])
        elif str(msg["role"]) == "assistant":
            st.chat_message("ai").write(msg["content"])
    
    # Set up markdown to fix chat_input and layer UI issues
    st.markdown("""
    <style>
        .stChatInput { 
            position: fixed;
            bottom: 50px; 
            width: 65%;
            z-index: 3;
        }
        .fixed-square {
            position: fixed;
            bottom: 0;
            left: 28%;
            width: 67%;
            height: 100px;
            background-color: white;
            z-index: 2;
        }
        main {
            z-index 1;
        }
    </style>
    <div class="fixed-square"></div>
    """, unsafe_allow_html=True)


def _write_user_message(user_input):
    st.chat_message("human").write(user_input)
    st.session_state["history"].add_user_message(user_input)


def _write_ai_message(response, already_written_because_streamed=False):
    if not already_written_because_streamed:
        st.chat_message("ai").write(response)
    st.session_state["history"].add_assistant_message(response)


async def generate():
    time_estimate = "2-3 minutes"
    
    generation_response = f"Your document is being generated. This generation process takes about {time_estimate}. Upon completion, a download button will appear below. Have a nice day!"
    _write_ai_message(generation_response)
    title, file = await generate_document(st.session_state["history"])
    st.download_button(label="Download document", data=file, file_name=title+".docx", mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


async def run_chatbot(user_input):
    _write_user_message(user_input)
    response = await brainstorm_chat(user_context=st.session_state["user_context"], language=st.session_state["language"], history=st.session_state["history"])
    _write_ai_message(response)
