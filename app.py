
# Ensure to install the required packages on your local terminal:
# pip install google-generativeai streamlit Pillow PyPDF2

import streamlit as st
import google.generativeai as genai
import json
import io
from PIL import Image
import PyPDF2
import base64 # New import for PDF processing

# --- Page Configuration ---
st.set_page_config(
    page_title="Catalyst Mind",
    page_icon="⚙️",
    layout="wide"
)


st.set_page_config(layout="wide")

# Inject CSS with local image
def set_bg_hack(img_path):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("data:image/png;base64,{img_to_bytes(img_path)}");
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}
         /* Dark overlay */
         .stApp::before {{
             content: "";
             position: absolute;
             top: 0;
             left: 0;
             right: 0;
             bottom: 0;
             background-color: rgba(0, 0, 0, 0.3);
             z-index: -1;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack("images/background.jpg")


# --- API Key Configuration ---
# IMPORTANT: For deploying on Streamlit Community Cloud or similar platforms,
# it's recommended to use Streamlit Secrets (st.secrets) for API keys.
# For local testing, you can replace "YOUR_GEMINI_API_KEY" with your actual key.
# If running in a Canvas environment with a free model like gemini-1.5-flash-latest,
# you can leave this empty, as the key is often provided automatically.
api_key = st.secrets.get("API_KEY") # Try to get from secrets first
#api_key = "AIzaSyDa9i75ooUlyakmOT35YFOR58g0TG-a2T0"

# API key validation
if api_key == None:
    st.error("Google Generative AI API key is not set. Please configure it in Streamlit Secrets or replace 'YOUR_GEMINI_API_KEY'.")
    st.stop() # Stop the app if no API key is found

# Configure the generative AI client
genai.configure(api_key=api_key)


st.title("Catalyst Mind - Google Generative AI ChatBot ⚙️")
st.caption("A ChatBot powered by Google Generative AI for Chemical Operations and Process Control")


st.sidebar.title("Navigation")
st.sidebar.markdown("Welcome to the Catalyst Mind ChatBot! This application allows you to interact with a Google Generative AI model to generate responses based on your input text. You can ask questions or provide prompts related to chemical operations and process control.")
st.sidebar.markdown("### How to Use:")
st.sidebar.markdown("1. Enter your text in the text area provided.")
st.sidebar.markdown("2. Click the 'Generate Response' button to get a response from the AI model.")
st.sidebar.markdown("3. The response will be displayed below the input area.")
st.sidebar.markdown("### About:")
st.sidebar.markdown("This application is designed to assist with queries related to chemical operations and process control using the capabilities of Google Generative AI. It can help in generating insights, answering questions, and providing information based on the input provided by the user.")

st.sidebar.markdown("### Contact:")



# Creating an instance of the Gemini-1.5.Flash AI Model
model = genai.GenerativeModel("gemini-1.5-flash")

# --- System Instruction Prompt ---
# This prompt defines the chatbot's persona and purpose.
# It's sent as an initial 'user' message to the model to guide its behavior.
system_instruction_prompt = """
You are Catalyst Mind, a chatbot powered by Google Generative AI.
You are designed to assist users with queries related to chemical operations and process control.
Your expertise includes:
- Explaining chemical processes and reactions.
- Providing insights into process control strategies (e.g., PID, advanced control).
- Answering questions about chemical engineering principles.
- Interpreting process diagrams or images related to chemical plants (if provided).
- Offering guidance on safety protocols in chemical environments.

**Guidelines:**
- Be precise, accurate, and concise in your responses.
- If a user uploads an image, analyze it in the context of chemical operations or process control.
- If you upload a PDF or TXT file, I will extract text from it and include it in your query.
- If you don't have enough information or if a query is outside your domain, politely state that you cannot assist.
- Maintain a professional and helpful tone.

 For each task, you are to execute and consider the following:
     1. Identify the chemical processes or operations required by the user and provide a detailed explanation on the chemical process.
     2. Determine the associated chemical parameters and conditions.
     3. Provide insight on the performance/evaluation metric for the process and challenges that have and may be encountered.
     4. Deliver the potential solutions and optimizations for the chemical process.
     5. Provide appropriate justifications for the reasoning behind your optimization techniques and solutions.
     6. Address potential constraints or limitations that may occur.
     7. Provide safety considerations and best practices related to the chemical operations discussed.
    

     Your domain/area of expertise is strictly limited to chemical operations and process control.
     You are not to provide any information outside of this domain. 
     If you are unable to answer a question or the question falls outside of the specified domain, kindly inform the user.
     If necessary, ask questions for clarification based on the user's request.
     Also ensure that any query or request that can significantly harm human life should be avoided.
"""

# --- Session State Initialization for Chat History ---
# We store messages in a list of dictionaries, where each dictionary
# has a 'role' (user/assistant) and 'parts' (list of text/image content).
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Initial system instruction for the model (user role, but not displayed as a chat bubble)
        {"role": "user", "parts": [{"text": system_instruction_prompt}]},
        # Initial greeting from the assistant (displayed as a chat bubble)
        {"role": "assistant", "parts": [{"text": "Hello! I am Catalyst Mind. How can I assist you with chemical operations or process control today?"}]}
    ]

# --- Display Existing Chat Messages ---
# Loop through messages in session state, starting from the 2nd message (index 1)
# to skip the hidden system instruction.
for message in st.session_state.messages[1:]: # Start from index 1 to display the initial assistant greeting
    with st.chat_message(message["role"]):
        for part_content in message["parts"]: # Iterate through the contents within 'parts'
            if isinstance(part_content, dict) and "text" in part_content:
                st.markdown(part_content["text"])
            elif isinstance(part_content, Image.Image): # Check if it's a PIL Image object
                st.image(part_content, caption="Uploaded Image", use_container_width=True)

# --- Chat Input with File Acceptance ---
# This widget allows users to type text and also upload files (images, PDFs, TXT in this case).
prompt_input = st.chat_input(
    "Ask me about chemical operations, process control, or upload an image, PDF, or TXT file...",
    accept_file=True, # Enable file uploads
    # UPDATED: Added 'pdf' and 'txt' to allowed file types
    file_type=["png", "jpg", "jpeg", "pdf", "txt"] # Specify allowed file types
)

# --- Process User Input (Text and/or Image/PDF/TXT) ---
if prompt_input:
    user_text = prompt_input.text
    uploaded_files = prompt_input.files # This is a list of UploadedFile objects

    # Prepare the parts for the user's message
    user_message_parts = []
    
    # Add the text prompt if available
    if user_text:
        user_message_parts.append({"text": user_text})

    # If files were uploaded, process them
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.type
            file_name = uploaded_file.name
            
            if file_type.startswith("image"):
                try:
                    # Read the file data and open it as a PIL Image
                    image_data = uploaded_file.read()
                    pil_image = Image.open(io.BytesIO(image_data))
                    user_message_parts.append(pil_image) # Append PIL Image object directly
                except Exception as e:
                    st.error(f"Error processing image {file_name}: {e}. This image will not be sent.")
                    continue
            elif file_type == "application/pdf":
                try:
                    with st.spinner(f"Extracting text from PDF: {file_name}..."):
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        pdf_text = ""
                        for page_num in range(len(pdf_reader.pages)):
                            # Extract text from each page
                            page_text = pdf_reader.pages[page_num].extract_text()
                            if page_text:
                                pdf_text += page_text + "\n" # Add newline between pages
                        
                        if pdf_text.strip(): # Check if any meaningful text was extracted
                            # Truncate content if too long to avoid hitting token limits
                            max_text_length = 2000
                            display_text = pdf_text.strip()
                            if len(display_text) > max_text_length:
                                display_text = display_text[:max_text_length] + "...\n\n[Content truncated due to length.]"
                            
                            user_message_parts.append({"text": f"Content from PDF '{file_name}':\n\n{display_text}"})
                            st.info(f"Successfully extracted text from PDF: {file_name}.")
                        else:
                            st.warning(f"Could not extract any readable text from PDF: {file_name}. It might be a scanned PDF without OCR, or empty.")
                            user_message_parts.append({"text": f"Attempted to process PDF '{file_name}', but no text could be extracted."})

                except Exception as e:
                    st.error(f"Error processing PDF {file_name}: {e}. This PDF will not be sent.")
                    user_message_parts.append({"text": f"Error processing PDF '{file_name}': {e}"}) # Add error message to parts
                    continue
            elif file_type == "text/plain":
                try:
                    # Read the text file content
                    text_content = uploaded_file.read().decode("utf-8")
                    
                    # Truncate content if too long
                    max_text_length = 2000
                    display_text = text_content.strip()
                    if len(display_text) > max_text_length:
                        display_text = display_text[:max_text_length] + "...\n\n[Content truncated due to length.]"

                    user_message_parts.append({"text": f"Content from TXT '{file_name}':\n\n{display_text}"})
                    st.info(f"Successfully processed TXT file: {file_name}.")
                except Exception as e:
                    st.error(f"Error processing text file {file_name}: {e}. This file will not be sent.")
                    user_message_parts.append({"text": f"Error processing text file '{file_name}': {e}"}) # Add error message to parts
                    continue
            else:
                st.warning(f"Unsupported file type: {file_name} ({file_type}). Only images (PNG, JPG, JPEG), PDFs, and TXT files are supported.")
                continue
    
    # If no text and no valid file content were provided, show a warning and stop processing
    if not user_message_parts:
        st.warning("Please enter a query or upload a valid image/PDF/TXT file to send a message.")
        st.stop() # Stop further execution for this rerun

    # Store and display the current user prompt in the chat history
    st.session_state.messages.append({"role": "user", "parts": user_message_parts})
    
    with st.chat_message("user"):
        for part_content in user_message_parts: # Iterate through the parts we just created
            if isinstance(part_content, dict) and "text" in part_content:
                st.markdown(part_content["text"])
            elif isinstance(part_content, Image.Image): # Check if it's a PIL Image object
                st.image(part_content, caption="Your Uploaded Image", use_container_width=True)

    # --- Prepare Messages for Gemini API ---
    # Convert the session state messages into the format expected by the Gemini API.
    # The Gemini API expects a list of dictionaries, where each dict has 'role' and 'parts'.
    # For 'parts', text is a dict {"text": "..."} and images are PIL Image objects directly.
    gemini_messages_for_api = []
    for msg in st.session_state.messages:
        # Map Streamlit roles to Gemini API roles ('user' -> 'user', 'assistant' -> 'model')
        role_for_gemini = "user" if msg["role"] == "user" else "model"
        
        parts_for_gemini = []
        for part_content in msg["parts"]: # Iterate through the contents within 'parts'
            if isinstance(part_content, dict) and "text" in part_content:
                parts_for_gemini.append({"text": part_content["text"]})
            elif isinstance(part_content, Image.Image):
                parts_for_gemini.append(part_content)
            # This 'elif' handles cases where a raw string might somehow end up in parts,
            # though with current logic, it should mostly be dicts or PIL Images.
            elif isinstance(part_content, str):
                parts_for_gemini.append({"text": part_content})
        
        # Ensure that 'parts_for_gemini' is not empty before appending the message
        if not parts_for_gemini:
            # This should ideally not happen if the initialization and user input handling are correct,
            # but it's a good safeguard against potential future issues or unexpected states.
            # print(f"Warning: Skipping message due to empty parts for role: {role_for_gemini}")
            continue # Skip this message if its parts are empty

        gemini_messages_for_api.append({"role": role_for_gemini, "parts": parts_for_gemini})

    # --- Generate a Response using the Gemini API ---
    try:
        # Call the generate_content method with the prepared messages
        # stream=True allows for a typewriter effect as the response comes in
        stream = model.generate_content(
            gemini_messages_for_api,
            stream=True,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7, # Controls randomness (0.0-1.0). Lower for more focused, higher for more creative.
                max_output_tokens=1024 # Maximum number of tokens in the generated response.
            )
        )

        # Display the assistant's response in a chat bubble
        with st.chat_message("assistant"):
            message_placeholder = st.empty() # Create an empty container to update dynamically
            full_response_content = ""
            for chunk in stream:
                if chunk.text: # Check if the chunk contains text
                    full_response_content += chunk.text
                    # Update the placeholder with the accumulating text and a blinking cursor
                    message_placeholder.markdown(full_response_content + "▌")
            # Final update to remove the cursor once streaming is complete
            message_placeholder.markdown(full_response_content)
            
        # Add the assistant's full response to the session state chat history
        st.session_state.messages.append({"role": "assistant", "parts": [{"text": full_response_content}]})
        
    except Exception as e:
        st.error(f"An error occurred while generating response: {e}")
        st.warning("Please try again. If the issue persists, verify your API key or the model's availability.")