# Ensure to install the required packages on your local terminal:
# pip install google-generativeai streamlit Pillow PyPDF2 cantera requests beautifulsoup4


import streamlit as st
import google.generativeai as genai
import json
import io
from PIL import Image
import PyPDF2
import base64
import os
import cantera as ct
import requests # New import for web fetching
from bs4 import BeautifulSoup # New import for HTML parsing

from tools.chem_info import *
from tools.online_data import *





# --- Page Configuration ---
st.set_page_config(
    page_title="Catalyst Mind",
    page_icon="⚛️",
    layout="centered"
)


st.markdown("""
<style>
    /* Main container centering */
    .main .block-container {
        max-width: 200px;  /* Adjust width as needed */
        margin: auto;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    
    
    /* Chat message centering */
    .stChatMessage {
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    


""", unsafe_allow_html=True)

# --- Centered Title Section with Enhanced Styling ---
st.markdown("""
<style>
    .title-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 700;
        color: #58a6ff;
        margin-bottom: 0.5rem;
        white-space: nowrap;
    }
    .subtitle {
        font-size: 1.1rem;
        margin-top: 0;
        letter-spacing: 0.5px;
    }
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #58a6ff, transparent);
        margin: 1rem auto;
        width: 60%;
    }
</style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown("""
<div class="title-container">
    <div class="main-title">⚛️Catalyst Mind </div>
    <div class="subtitle">Advanced chemical process analysis powered by Gemini AI and Cantera</div>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)




# --- API Key Configuration ---
# api_key = st.secrets.get("GEMINI_API_KEY")
api_key = "AIzaSyBCjtvQ7kvYQcImqRToLSDyfkofCGiRM74"

if api_key is None:
    st.error("Google Generative AI API key is not set. Please configure it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)


# --- Professional Dark Theme Sidebar with Consistent Font Sizing ---
with st.sidebar:
    st.title("⚗️ Catalyst Mind")
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #0e1117;
        color: white;
    }
    .capability-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        border-left: 4px solid #4a6fa5;
        color: #ffffff !important;
        font-size: 14px;  /* Base font size for all cards */
    }
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 10px;
        vertical-align: middle;
        color: #58a6ff;
    }
    .st-expander {
        background-color: #262730;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .st-expander .streamlit-expanderHeader {
        color: #ffffff;
        font-weight: 600;
        font-size: 15px;  /* Header font size */
    }
    .st-expander .streamlit-expanderContent {
        color: #ffffff;
        font-size: 14px;  /* Ensures content matches card font size */
    }
    ul, ol {
        margin-bottom: 0;
        padding-left: 20px;
        font-size: 14px;  /* List items match card font size */
    }
    li {
        color: #ffffff;
        margin-bottom: 8px;
    }
    strong {
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # Capabilities Section with Expanders
    with st.expander("🧪 **AI Capabilities**", expanded=True):
        # Thermodynamics Section
        with st.expander("🌡️ **Thermodynamic Analysis**", expanded=False):
            st.markdown("""
            <div class="capability-card">
                <ul>
                    <li>Species property determination (H, S, G, Cp)</li>
                    <li>Phase equilibrium calculations</li>
                    <li>Reaction enthalpy/entropy analysis</li>
                    <li>Temperature/pressure effects modeling</li>
                    <li>Ideal/non-ideal system evaluation</li>
                    <li>Adiabatic flame temperature calculations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Reaction Engineering Section
        with st.expander("⚡ **Reaction Engineering**", expanded=False):
            st.markdown("""
            <div class="capability-card">
                <ul>
                    <li>Adiabatic flame temperature calculation</li>
                    <li>Equilibrium composition determination</li>
                    <li>Batch/continuous reactor analysis</li>
                    <li>Reaction kinetic parameter estimation</li>
                    <li>Catalytic reaction evaluation</li>
                    <li>Process simulation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Process Analysis Section
        with st.expander("📊 **Process Analysis**", expanded=False):
            st.markdown("""
            <div class="capability-card">
                <ul>
                    <li>Mass/energy balance calculations</li>
                    <li>Process optimization scenarios</li>
                    <li>Safety parameter evaluation (LFL/UFL, AIT)</li>
                    <li>Equipment sizing guidance</li>
                    <li>Process flow diagram interpretation</li>
                    <li>Dynamic process simulation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # Technical Specifications Section
    with st.expander("🔧 **Technical Specifications**", expanded=False):
        st.markdown("""
        <div class="capability-card">
            <ul>
                <li><strong>AI Engine:</strong> Gemini 1.5 Flash</li>
                <li><strong>Thermodynamics:</strong> Cantera 3.0</li>
                <li><strong>Mechanisms:</strong> GRI-Mech 3.0</li>
                <li><strong>Database:</strong> NASA polynomials (300-5000K)</li>
                <li><strong>Precision:</strong> 64-bit floating point</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # How To Use Section
    with st.expander("🛠️ **How To Use**", expanded=False):
        st.markdown("""
        <div class="capability-card">
            <ol>
                <li>Enter query in natural language</li>
                <li>Upload relevant files if needed</li>
                <li>Receive AI-powered analysis</li>
                <li>View detailed calculations</li>
                <li>Request further refinements</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    # --- Download Chat Session ---
    if st.sidebar.button("📥 Download This Session"):
        import datetime
        import json
        session_data = {
            "timestamp": str(datetime.datetime.now()),
            "chat": st.session_state.get("messages", [])
        }
        session_json = json.dumps(session_data, indent=2)

        b64 = base64.b64encode(session_json.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="catalyst_mind_session.json">Click here to download</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.8em; color: #aaa;">
        For chemical engineering professionals<br>
        v2.1 | Secure API Connection
    </div>
    """, unsafe_allow_html=True)

    



# --- Map tool names to actual functions ---
available_tools = {
    "calculate_adiabatic_flame_temperature": calculate_adiabatic_flame_temperature,
    "get_species_molecular_weight": get_species_molecular_weight,
    "get_equilibrium_concentrations": get_equilibrium_concentrations,
    "get_species_thermodynamic_properties": get_species_thermodynamic_properties,
    "process_simulation_snapshot": process_simulation_snapshot,
    "generate_phase_diagram": generate_phase_diagram,
    "get_wikipedia_data": get_wikipedia_data
}


# --- Initialize the Generative Model ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- System Instruction Prompt (UPDATED for Manual Tool Use) ---
# Load system instruction prompt from a text file
try:
    with open ("prompts.txt", "+r", encoding = "utf-8") as file:
        system_instruction_prompt = file.read()
except Exception as e:
    print ("Error accessing document")
    st.stop()

# --- Session State Initialization for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "parts": [{"text": system_instruction_prompt}]},
        {"role": "assistant", "parts": [{"text": "Hello! I am Catalyst Mind. How can I assist you with chemical operations or process control today?"}]}
    ]

# --- Display Existing Chat Messages ---
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        for part_content in message["parts"]:
            if isinstance(part_content, dict) and "text" in part_content:
                st.markdown(part_content["text"])
            elif isinstance(part_content, Image.Image):
                st.image(part_content, caption="Uploaded Image", use_container_width=True)
            # Display tool outputs if they are part of the conversation history (as plain text/JSON)
            elif isinstance(part_content, dict) and "tool_output" in part_content:
                st.subheader("Tool Output:")
                st.json(part_content["tool_output"]) # Display raw JSON for debugging tool output

# --- Chat Input with File Acceptance ---
prompt_input = st.chat_input(
    "Ask me about chemical operations, process control, or upload an image, PDF, or TXT file...",
    accept_file=True,
    file_type=["png", "jpg", "jpeg", "pdf", "txt"]
)

# --- Process User Input and Generate Response ---
if prompt_input:
    user_text = prompt_input.text
    uploaded_files = prompt_input.files

    user_message_parts = []
    if user_text:
        user_message_parts.append({"text": user_text})

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.type
            file_name = uploaded_file.name
            
            if file_type.startswith("image"):
                try:
                    image_data = uploaded_file.read()
                    pil_image = Image.open(io.BytesIO(image_data))
                    user_message_parts.append(pil_image)
                except Exception as e:
                    st.error(f"Error processing image {file_name}: {e}. This image will not be sent.")
                    continue
            elif file_type == "application/pdf":
                try:
                    with st.spinner(f"Extracting text from PDF: {file_name}..."):
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        pdf_text = ""
                        for page_num in range(len(pdf_reader.pages)):
                            page_text = pdf_reader.pages[page_num].extract_text()
                            if page_text:
                                pdf_text += page_text + "\n"
                        
                        if pdf_text.strip():
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
                    user_message_parts.append({"text": f"Error processing PDF '{file_name}': {e}"})
                    continue
            elif file_type == "text/plain":
                try:
                    text_content = uploaded_file.read().decode("utf-8")
                    max_text_length = 2000
                    display_text = text_content.strip()
                    if len(display_text) > max_text_length:
                        display_text = display_text[:max_text_length] + "...\n\n[Content truncated due to length.]"

                    user_message_parts.append({"text": f"Content from TXT '{file_name}':\n\n{display_text}"})
                    st.info(f"Successfully processed TXT file: {file_name}.")
                except Exception as e:
                    st.error(f"Error processing text file {file_name}: {e}. This file will not be sent.")
                    user_message_parts.append({"text": f"Error processing text file '{file_name}': {e}"})
                    continue
            else:
                st.warning(f"Unsupported file type: {file_name} ({file_type}). Only images (PNG, JPG, JPEG), PDFs, and TXT files are supported.")
                continue
    
    if not user_message_parts:
        st.warning("Please enter a query or upload a valid image/PDF/TXT file to send a message.")
        st.stop()

    st.session_state.messages.append({"role": "user", "parts": user_message_parts})
    
    with st.chat_message("user"):
        for part_content in user_message_parts:
            if isinstance(part_content, dict) and "text" in part_content:
                st.markdown(part_content["text"])
            elif isinstance(part_content, Image.Image):
                st.image(part_content, caption="Your Uploaded Image", use_container_width=True)

    # --- Agentic AI Loop for Manual Tool Calling ---
    with st.spinner("Catalyst Mind is thinking..."):
        # Prepare messages for Gemini API
        gemini_messages_for_api = []
        for msg in st.session_state.messages:
            role_for_gemini = "user" if msg["role"] == "user" else "model"
            parts_for_gemini = []
            for part_content in msg["parts"]:
                if isinstance(part_content, dict) and "text" in part_content:
                    parts_for_gemini.append({"text": part_content["text"]})
                elif isinstance(part_content, Image.Image):
                    parts_for_gemini.append(part_content)
                elif isinstance(part_content, dict) and "tool_output" in part_content:
                    # When sending tool output back to the model, format it as regular text
                    # or a specific string that the model understands as "tool result"
                    parts_for_gemini.append({"text": f"Tool Output:\n```json\n{json.dumps(part_content['tool_output'], indent=2)}\n```"})
                elif isinstance(part_content, str): # Fallback for any raw strings
                    parts_for_gemini.append({"text": part_content})
            
            if not parts_for_gemini:
                continue
            gemini_messages_for_api.append({"role": role_for_gemini, "parts": parts_for_gemini})

        try:
            # First call to model.generate_content to get the model's initial thought/tool call
            response_stream = model.generate_content(
                gemini_messages_for_api,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1024
                )
            )

            full_response_content = ""
            tool_call_detected = False
            tool_output_result = None
            tool_name_called = None
            tool_args_called = None

            for chunk in response_stream:
                if chunk.text:
                    full_response_content += chunk.text
            
            # Attempt to parse the full response content for a tool call JSON
            # The model is prompted to output JSON followed by a message.
            # We look for the JSON at the beginning of the response.
            try:
                # Find the start and end of the JSON block
                json_start = full_response_content.find('{')
                json_end = full_response_content.rfind('}') + 1 # +1 to include the '}'
                
                if json_start != -1 and json_end != -1 and json_start < json_end:
                    json_str = full_response_content[json_start:json_end]
                    parsed_json = json.loads(json_str)
                    
                    if "tool_call" in parsed_json and \
                       "name" in parsed_json["tool_call"] and \
                       "args" in parsed_json["tool_call"]:
                        
                        tool_name_called = parsed_json["tool_call"]["name"]
                        tool_args_called = parsed_json["tool_call"]["args"]
                        tool_call_detected = True
                        
                        # Remove the JSON part from the content that will be displayed as model's thought
                        full_response_content = full_response_content[json_end:].strip()

            except json.JSONDecodeError:
                # Not a valid JSON, or JSON is incomplete/malformed.
                # Treat as a regular text response.
                pass
            except Exception as e:
                st.warning(f"Error parsing potential tool call JSON: {e}")
                pass # Continue as normal text response

            if tool_call_detected:
                st.info(f"Catalyst Mind decided to use a tool: `{tool_name_called}` with arguments: `{tool_args_called}`")
                
                # Execute the tool based on its name
                if tool_name_called in available_tools:
                    try:
                        # Ensure arguments are correctly typed for the Python function
                        # This is a simple example; for robust production, you'd add validation/conversion
                        # based on the expected types of the tool function's parameters.
                        tool_output_result = available_tools[tool_name_called](**tool_args_called)
                        tool_output_result_parsed = json.loads(tool_output_result) # Parse JSON string back to dict
                        st.success(f"Tool output: {tool_output_result_parsed['status']}")
                        st.json(tool_output_result_parsed) # Display parsed output for debugging
                        
                        # Add the tool output to the conversation history
                        st.session_state.messages.append({
                            "role": "tool_output_display", # Custom role for display purposes
                            "parts": [{"tool_output": tool_output_result_parsed}]
                        })

                        # Prepare messages for the second API call, including the tool output
                        # We append the tool's raw JSON output as a text part for the model to process
                        gemini_messages_for_api.append({
                            "role": "user", # Model's perspective: it "receives" the tool output from the system/user
                            "parts": [{"text": f"Tool execution result for {tool_name_called}:\n```json\n{tool_output_result}\n```"}]
                        })
                        
                        # Make a second call to get the model's interpretation of the tool output
                        final_response_stream = model.generate_content(
                            gemini_messages_for_api,
                            stream=True,
                            generation_config=genai.types.GenerationConfig(
                                temperature=0.7,
                                max_output_tokens=1024
                            )
                        )
                        full_response_content = "" # Reset to accumulate final response
                        for final_chunk in final_response_stream:
                            if final_chunk.text:
                                full_response_content += final_chunk.text
                        
                    except Exception as tool_e:
                        st.error(f"Error executing tool '{tool_name_called}': {tool_e}")
                        full_response_content = f"An error occurred while executing the tool '{tool_name_called}'. Please check the parameters or try again. Error: {tool_e}"
                else:
                    st.warning(f"Catalyst Mind tried to call an unknown tool: {tool_name_called}")
                    full_response_content = f"Catalyst Mind attempted to use an unknown tool: {tool_name_called}. Please ensure your query is within my capabilities."
            
            # Display the assistant's final response (either direct or after tool call)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                if full_response_content:
                    message_placeholder.markdown(full_response_content + "▌")
                else:
                    message_placeholder.markdown("No direct text response. A tool might have been executed.")
                message_placeholder.markdown(full_response_content)
                
            # Add the assistant's final response to the session state chat history
            if full_response_content:
                st.session_state.messages.append({"role": "assistant", "parts": [{"text": full_response_content}]})
            
        except Exception as e:
            st.error(f"An error occurred while generating response: {e}")
            st.warning("Please try again. If the issue persists, verify your API key or the model's availability.")


