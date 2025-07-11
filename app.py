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





# --- Page Configuration ---
st.set_page_config(
    page_title="Catalyst Mind",
    page_icon="⚛️",
    layout="wide"
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
api_key = st.secrets.get("GEMINI_API_KEY")
api_key = "AIzaSyDa9i75ooUlyakmOT35YFOR58g0TG-a2T0"

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

    

# --- Cantera Tool Definitions ---
def calculate_adiabatic_flame_temperature(fuel: str, oxidizer: str, equivalence_ratio: float, initial_temp_k: float, initial_pressure_pa: float) -> str:
    """
    Calculates the adiabatic flame temperature (AFT) for a given fuel and oxidizer mixture.
    
    Args:
        fuel (str): The chemical formula of the fuel (e.g., 'CH4' for methane, 'C2H5OH' for ethanol).
        oxidizer (str): The chemical formula of the oxidizer (e.g., 'O2' for pure oxygen, 'air' for atmospheric air).
        equivalence_ratio (float): The equivalence ratio (phi). Phi < 1 for lean, Phi = 1 for stoichiometric, Phi > 1 for rich.
        initial_temp_k (float): The initial temperature of the reactants in Kelvin (e.g., 300.0).
        initial_pressure_pa (float): The initial pressure of the reactants in Pascals (e.g., 101325.0 for 1 atm).

    Returns:
        str: A JSON string containing the adiabatic flame temperature in Kelvin and Celsius,
             or an error message if the calculation fails.
    """
    try:
        gas = ct.Solution('gri30.yaml')
        gas.TP = initial_temp_k, initial_pressure_pa
        if oxidizer.lower() == 'air':
            gas.set_equivalence_ratio(equivalence_ratio, fuel, {'O2': 1.0, 'N2': 3.76})
        else:
            gas.set_equivalence_ratio(equivalence_ratio, fuel, oxidizer)
        gas.equilibrate('HP')
        
        aft_k = gas.T
        aft_c = aft_k - 273.15
        
        return json.dumps({
            "status": "success",
            "fuel": fuel,
            "oxidizer": oxidizer,
            "equivalence_ratio": equivalence_ratio,
            "initial_temperature_K": initial_temp_k,
            "initial_pressure_Pa": initial_pressure_pa,
            "adiabatic_flame_temperature_K": aft_k,
            "adiabatic_flame_temperature_C": aft_c
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Cantera calculation failed: {str(e)}",
            "fuel": fuel,
            "oxidizer": oxidizer,
            "equivalence_ratio": equivalence_ratio,
            "initial_temperature_K": initial_temp_k,
            "initial_pressure_Pa": initial_pressure_pa
        })

def get_species_molecular_weight(species_name: str) -> str:
    """
    Retrieves the molecular weight of a specified chemical species using Cantera's default mechanism.

    Args:
        species_name (str): The chemical formula or common name of the species (e.g., 'CO2', 'H2O', 'CH4').

    Returns:
        str: A JSON string containing the molecular weight in kg/kmol (g/mol),
             or an error message if the species is not found.
    """
    try:
        gas = ct.Solution('gri30.yaml')
        mw = gas.molecular_weights[gas.species_index(species_name)]
        
        return json.dumps({
            "status": "success",
            "species": species_name,
            "molecular_weight_kg_kmol": mw,
            "molecular_weight_g_mol": mw / 1000.0
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Species '{species_name}' not found or molecular weight calculation failed: {str(e)}",
            "species": species_name
        })

def get_equilibrium_concentrations(mixture_formula: str, temperature_k: float, pressure_pa: float) -> str:
    """
    Calculates the equilibrium mole fractions of species in a given mixture at a specified temperature and pressure.

    Args:
        mixture_formula (str): The initial composition of the mixture as a string (e.g., 'CH4:1, O2:2, N2:7.52').
                               Ensure the species are defined in the loaded Cantera mechanism (gri30.yaml).
        temperature_k (float): The equilibrium temperature in Kelvin.
        pressure_pa (float): The equilibrium pressure in Pascals.

    Returns:
        str: A JSON string containing the equilibrium mole fractions of all species present,
             or an error message if the calculation fails.
    """
    try:
        gas = ct.Solution('gri30.yaml')
        gas.TPX = temperature_k, pressure_pa, mixture_formula
        gas.equilibrate('TP')

        mole_fractions = {species.name: gas.X[species.index] for species in gas.species()}
        
        return json.dumps({
            "status": "success",
            "mixture_formula": mixture_formula,
            "temperature_K": temperature_k,
            "pressure_Pa": pressure_pa,
            "equilibrium_mole_fractions": mole_fractions
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Equilibrium calculation failed for mixture '{mixture_formula}' at {temperature_k}K, {pressure_pa}Pa: {str(e)}",
            "mixture_formula": mixture_formula,
            "temperature_K": temperature_k,
            "pressure_Pa": pressure_pa
        })

def get_species_thermodynamic_properties(species_name: str, temperature_k: float, pressure_pa: float) -> str:
    """
    Retrieves standard thermodynamic properties (enthalpy, entropy, Gibbs free energy, heat capacity)
    for a specified chemical species at a given temperature and pressure using Cantera.

    Args:
        species_name (str): The chemical formula or common name of the species (e.g., 'CO2', 'H2O', 'CH4').
                            Must be present in the 'gri30.yaml' mechanism.
        temperature_k (float): The temperature in Kelvin.
        pressure_pa (float): The pressure in Pascals.

    Returns:
        str: A JSON string containing the thermodynamic properties in J/kmol or J/kmol-K,
             or an error message if the species is not found or calculation fails.
    """
    try:
        gas = ct.Solution('gri30.yaml')
        # Set the state for the specific species
        gas.TPX = temperature_k, pressure_pa, f'{species_name}:1.0' # Set mole fraction to 1 for the species

        properties = {
            "enthalpy_kmol": gas.h,     # J/kmol
            "entropy_kmol": gas.s,      # J/kmol-K
            "gibbs_kmol": gas.g,        # J/kmol
            "cp_kmol": gas.cp          # J/kmol-K (constant pressure heat capacity)
        }
        
        return json.dumps({
            "status": "success",
            "species": species_name,
            "temperature_K": temperature_k,
            "pressure_Pa": pressure_pa,
            "thermodynamic_properties": properties
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Could not retrieve thermodynamic properties for '{species_name}': {str(e)}. Ensure species is in 'gri30.yaml' and parameters are valid.",
            "species": species_name,
            "temperature_K": temperature_k,
            "pressure_Pa": pressure_pa
        })

def get_safety_information_from_url(url: str, keyword: str = "") -> str:
    """
    Fetches content from a given URL and attempts to extract relevant safety information based on a keyword.
    This tool is designed to mimic web browsing for safety data sheets (SDS) or chemical safety pages.

    Args:
        url (str): The URL of the safety data sheet (SDS) or chemical safety page (e.g., from OSHA, PubChem, CDC).
        keyword (str): An optional keyword to specifically look for within the page content (e.g., 'flammability', 'exposure limits', 'first aid').

    Returns:
        str: A JSON string containing a summary of the extracted safety information,
             or an error message.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15) # Increased timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Prioritize common content areas for text extraction
        text_content_elements = soup.find_all(['p', 'div', 'li', 'h1', 'h2', 'h3', 'span'])
        full_text = "\n".join([elem.get_text(separator=' ', strip=True) for elem in text_content_elements])
        
        extracted_info = ""
        if keyword:
            # Search for keyword in the extracted text
            relevant_lines = [line for line in full_text.split('\n') if keyword.lower() in line.lower()]
            if relevant_lines:
                # Concatenate a few relevant lines, ensuring not to exceed a reasonable length
                extracted_info = "\n".join(relevant_lines[:5]) # Get up to 5 relevant lines
                if len(extracted_info) > 500: # Truncate if still too long
                    extracted_info = extracted_info[:500] + "..."
            
            if not extracted_info:
                extracted_info = f"No specific information found for '{keyword}' on the page."
        else:
            # If no keyword, provide a general summary of the page's text
            extracted_info = full_text[:1000] + "..." if len(full_text) > 1000 else full_text
            if not extracted_info.strip():
                extracted_info = "No significant text content could be extracted from the page."
            else:
                extracted_info = f"General content summary from page:\n{extracted_info}"

        return json.dumps({
            "status": "success",
            "url": url,
            "keyword_searched": keyword,
            "extracted_safety_info": extracted_info
        })
    except requests.exceptions.RequestException as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to fetch content from URL: {str(e)}. The URL might be invalid, blocked, or network issue.",
            "url": url,
            "keyword_searched": keyword
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error processing safety information from URL: {str(e)}",
            "url": url,
            "keyword_searched": keyword
        })

def get_rsc_data(query: str) -> str:
    """
    Searches the Royal Society of Chemistry (RSC) website for information related to a chemical query.
    This tool constructs a search URL for RSC and fetches content from the search results.

    Args:
        query (str): The chemical or scientific query to search on the RSC website.

    Returns:
        str: A JSON string containing a summary of the extracted RSC data from search results, or an error message.
    """
    # RSC search URL. Using 'q' for query parameter.
    search_url = f"https://www.rsc.org/search/results/?q={requests.utils.quote(query)}"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(search_url, headers=headers, timeout=15) # Increased timeout
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results_snippets = []
        # Inspect RSC search results page HTML to find appropriate classes/tags
        # These are common patterns, may need adjustment based on current RSC site structure
        for item in soup.find_all('li', class_='search-result'): # Example: common class for search results
            title_tag = item.find(['h2', 'h3', 'a'], class_='result-title') # Look for title in h2/h3 or a tag
            link_tag = item.find('a')
            snippet_tag = item.find('p', class_='result-snippet') # Example: common class for snippet

            title = title_tag.get_text(strip=True) if title_tag else 'No Title'
            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else '#'
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else 'No snippet available.'
            
            # Ensure link is absolute
            if link and not link.startswith(('http://', 'https://')):
                if link.startswith('/'):
                    link = f"https://www.rsc.org{link}" # Prepend base URL if relative
                else:
                    link = f"https://www.rsc.org/{link}" # Assume relative path from base

            results_snippets.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}")
            if len(results_snippets) >= 3: # Limit to top 3 results for brevity
                break

        if results_snippets:
            extracted_info = "\n\n---\n\n".join(results_snippets)
        else:
            extracted_info = f"No relevant search results found on Royal Society of Chemistry for query '{query}'."

        return json.dumps({
            "status": "success",
            "query": query,
            "rsc_search_url": search_url,
            "extracted_rsc_info": extracted_info
        })
    except requests.exceptions.RequestException as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to search Royal Society of Chemistry: {str(e)}. Network error or site blocked.",
            "query": query,
            "rsc_search_url": search_url
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error processing Royal Society of Chemistry data: {str(e)}",
            "query": query
        })


# --- Map tool names to actual functions ---
available_tools = {
    "calculate_adiabatic_flame_temperature": calculate_adiabatic_flame_temperature,
    "get_species_molecular_weight": get_species_molecular_weight,
    "get_equilibrium_concentrations": get_equilibrium_concentrations,
    "get_species_thermodynamic_properties": get_species_thermodynamic_properties, # NEW TOOL
    "get_safety_information_from_url": get_safety_information_from_url, # NEW TOOL
    "get_rsc_data": get_rsc_data # NEW TOOL
}


# --- Initialize the Generative Model ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- System Instruction Prompt (UPDATED for Manual Tool Use) ---
system_instruction_prompt = """
You are Catalyst Mind, a chatbot powered by Google Generative AI, specializing strictly in chemical operations and process control. Your role is to provide accurate, detailed responses to queries about chemical processes, control strategies, and related engineering principles, using provided tools for calculations and data retrieval when necessary.

Core Instructions:
Domain Restriction: Respond only to queries within chemical operations and process control. For out-of-scope queries, reply: "I'm sorry, but that query is outside my expertise in chemical operations and process control. Please ask about chemical processes or related topics."
Safety First: For queries involving potentially hazardous chemicals or operations, respond with: "This request involves potentially hazardous substances or operations. Please clarify the context or specific requirements to ensure safety." Do not proceed without clarification.
Response Structure: For each query, address:
Detailed explanation of the chemical process or operation.
Relevant chemical parameters and conditions.
Performance metrics and potential challenges.
Solutions and optimizations with justifications.


Constraints or limitations.
Safety considerations and best practices.
Tool Usage Guidelines:You have access to specialized tools for calculations and data retrieval. When a query requires a tool, output a JSON object with the exact format below, followed by a brief message (e.g., "Executing calculation..." or "Fetching data..."). If parameters are missing or unclear, ask for clarification before outputting JSON.

Defined Structure for JSON Format
{
  "tool_call": {
    "name": "tool_function_name",
    "args": {
      "param1": "value1",
      "param2": "value2"
    }
  }
}

Available Tools and Parameters:
calculate_adiabatic_flame_temperature: Calculates adiabatic flame temperature.
fuel (string, e.g., 'CH4', 'C2H5OH')
oxidizer (string, e.g., 'O2', 'air')
equivalence_ratio (float, e.g., 1.0 for stoichiometric)
initial_temp_k (float, Kelvin, e.g., 298.15)
initial_pressure_pa (float, Pascals, e.g., 101325.0)

get_species_molecular_weight: Retrieves molecular weight of a species.
species_name (string, e.g., 'CO2', 'H2O')

get_equilibrium_concentrations: Calculates equilibrium mole fractions.
mixture_formula (string, e.g., 'CH4:1, O2:2, N2:7.52')
temperature_k (float, Kelvin, e.g., 1500.0)
pressure_pa (float, Pascals, e.g., 101325.0)

get_species_thermodynamic_properties: Retrieves thermodynamic properties (enthalpy, entropy, Gibbs, heat capacity).
species_name (string, e.g., 'H2O')
temperature_k (float, Kelvin)
pressure_pa (float, Pascals)

get_safety_information_from_url: Extracts safety information from a URL (e.g., SDS, OSHA page).
url (string, valid URL)
keyword (string, optional, e.g., 'flammability')

get_rsc_data: Searches Royal Society of Chemistry website for chemical data.
query (string, e.g., 'methane properties')

Workflow for Handling Queries:
Parse User Intent: Determine if the query requires:
General information (use your knowledge base).
A calculation (use a Cantera-based tool).

External data (use get_rsc_data or get_safety_information_from_url).

Tool Selection:
Match the query to the appropriate tool based on keywords (e.g., "adiabatic flame temperature" → calculate_adiabatic_flame_temperature).
If a tool is needed, verify all required parameters are provided. If not, respond with a question like: "Please provide [missing parameter] for the calculation."
Output the tool call JSON only when all parameters are valid and complete.


Tool Output Handling:
After receiving tool output, interpret results in the context of the query.
If the tool returns an error, respond with: "The tool encountered an error: [error message]. Please check your input or try again."


Multimodal Inputs:
For uploaded images, analyze them in the context of chemical operations (drawings, diagrams, etc.).
For PDF/TXT files, use extracted text to inform your response.

Error Prevention:
Do not estimate or assume parameters; always ask for clarification if data is missing.
Validate tool inputs before execution (e.g., positive temperatures, valid species names).
For web-based tools, prioritize reliable sources (OSHA, PubChem, RSC).

Response Clarity:
Provide concise, accurate answers.
For calculations, explain results (e.g., "The adiabatic flame temperature of 2200 K indicates...").
Include safety warnings where applicable.

"""

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


