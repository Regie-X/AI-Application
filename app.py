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
api_key = st.secrets.get("GEMINI_API_KEY")


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

        # mole_fractions = {species.name: gas.X[species.index] for species in gas.species()}
        mole_fractions = {species: mole_fraction for species, mole_fraction in zip(gas.species_names, gas.X)}
        
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

def process_simulation_snapshot(process_type: str, inlet_composition: str, temperature_k: float, pressure_pa: float, flow_rate: float, reactor_params: dict = None) -> str:
    """    Simulates a chemical process snapshot based on the specified process type, inlet composition, temperature, pressure, and flow rate.
    Args:
        process_type (str): The type of process to simulate (e.g., 'combustion', 'reaction', 'distillation').
        inlet_composition (str): The inlet composition as a string (e.g., 'CH4:1, O2:2, N2:7.52').
        temperature_k (float): The temperature in Kelvin.
        pressure_pa (float): The pressure in Pascals.
        flow_rate (float): The flow rate in moles per second.
        reactor_params (dict, optional): Additional parameters for the reactor simulation, such as volume.
    Returns:
        str: A JSON string containing the simulation results, including outlet composition and conversion,
             or an error message if the simulation fails.
    """
    
    try:
        gas = ct.Solution('gri30.yaml')
        gas.TPX = temperature_k, pressure_pa, inlet_composition
        reactor = ct.IdealGasReactor(gas, volume=reactor_params.get("volume", 1.0))
        sim = ct.ReactorNet([reactor])
        sim.advance_to_steady_state()
        return json.dumps({
            "status": "success",
            "process_type": process_type,
            "outlet_composition": {species: reactor.thermo.X[i] for i, species in enumerate(gas.species_names)},
            "conversion": 1 - reactor.thermo[inlet_composition.split(":")[0]].X
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Process simulation failed: {str(e)}"})

def generate_phase_diagram(components: list, temperature_k: float, pressure_pa: float, mole_fractions: list) -> str:
    """    Generates a phase diagram for a mixture of components at specified temperature and pressure.
    Args:
        components (list): List of chemical components (e.g., ['CH4', 'O2', 'N2']).
        temperature_k (float): The temperature in Kelvin.
        pressure_pa (float): The pressure in Pascals.
        mole_fractions (list): List of mole fractions corresponding to the components.
    Returns:
        str: A JSON string containing the phase diagram data, including vapor and liquid compositions,
             or an error message if the generation fails.
    """
    
    try:
        gas = ct.Solution('gri30.yaml')
        gas.TPX = temperature_k, pressure_pa, {comp: x for comp, x in zip(components, mole_fractions)}
        
        return json.dumps({
            "status": "success",
            "components": components,
            "phase_data": {"vapor_composition": gas.X, "liquid_composition": gas.X}  # Simplified
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Phase diagram generation failed: {str(e)}"})




def get_wikipedia_data(query: str) -> str:
    """
    Fetches the full main content of a Wikipedia article based on a query.
    
    Args:
        query (str): The chemical or scientific topic to retrieve from Wikipedia.
        
    Returns:
        str: A JSON string containing the article title, full text, and page metadata.
    """
    search_url = f"https://en.wikipedia.org/wiki/{requests.utils.quote(query)}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        page_title = soup.find("h1", id="firstHeading").text.strip()

        # Extract the main content
        content_div = soup.find("div", class_="mw-parser-output")
        paragraphs = content_div.find_all(['p', 'h2', 'h3', 'ul', 'ol'])  # Main content only

        article_text = ""
        for tag in paragraphs:
            if tag.name in ["h2", "h3"]:
                section_title = tag.get_text(strip=True).replace("[edit]", "")
                article_text += f"\n\n### {section_title}\n\n"
            else:
                text = tag.get_text(strip=True)
                if text:
                    article_text += f"{text}\n\n"

        if article_text.strip():
            return json.dumps({
                "status": "success",
                "query": query,
                "wikipedia_url": search_url,
                "title": page_title,
                "article_text": article_text.strip()
            })
        else:
            return json.dumps({
                "status": "error",
                "query": query,
                "wikipedia_url": search_url,
                "message": "No article text found on the page."
            })

    except requests.exceptions.RequestException as e:
        return json.dumps({
            "status": "error",
            "query": query,
            "wikipedia_url": search_url,
            "message": f"Network error: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "query": query,
            "wikipedia_url": search_url,
            "message": f"Parsing error: {str(e)}"
        })




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
system_instruction_prompt = """
You are Catalyst Mind, an intelligent chemical engineering agent powered by Google Generative AI, specializing strictly in chemical operations and process control. Your role is to provide accurate, detailed responses to queries about chemical processes, control strategies, and related engineering principles, using provided tools for calculations and data retrieval when necessary. You are capable of delivering expert solutions and recommendations based on the latest chemical engineering practices and data.

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
- calculate_adiabatic_flame_temperature: Calculates adiabatic flame temperature.
This requires the fuel and oxidizer chemical formulas, equivalence ratio, initial temperature in Kelvin, and initial pressure in Pascals.
If all the values aren't provided, ask the user to specify them. If all parameters are provided except the initial temperature and pressure, use 298.15 Kelvin and 101325 Pascals.
State clearly that the initial pressure and temperature are assumed to be 1 atm (101325 Pa) and 298.15K if not specified.
    fuel (string, e.g., 'CH4', 'C2H5OH')
    oxidizer (string, e.g., 'O2', 'air')
    equivalence_ratio (float, e.g., 1.0 for stoichiometric)
    initial_temp_k (float, Kelvin, e.g., 298.15)
    initial_pressure_pa (float, Pascals, e.g., 101325.0)

- get_species_molecular_weight: Retrieves molecular weight of a species.
This returns the molecular weight of a specified chemical species.
This requires the chemical formula or common name of the species and outputs the molecular weight of the specified component.
    species_name (string, e.g., 'CO2', 'H2O')

- get_equilibrium_concentrations: Calculates equilibrium mole fractions.
This tool should be used when the equilibrium composition, equilibrium concentration, or steady-state composition of a mixture is desired.
If the temperature and pressure aren't specified, assume standard temperature and pressure and inform the user fo the assumption.
This requires the initial mixture formula, temperature in Kelvin, and pressure in Pascals.
Outputs the equilibrium mole fractions of all species present in the mixture.
    mixture_formula (string, e.g., 'CH4:1, O2:2, N2:7.52')
    temperature_k (float, Kelvin, e.g., 1500.0)
    pressure_pa (float, Pascals, e.g., 101325.0)

- get_species_thermodynamic_properties: Retrieves thermodynamic properties (enthalpy, entropy, Gibbs, heat capacity).
This tool should be used when the thermodynamic properties of a species are required. The properties include enthalpy, entropy, Gibbs free energy, and heat capacity at constant pressure.
If the temperature and pressure aren't specified, assume standard conditions (298.15 Kelvin and 101325 Pascals) and inform the user of the assumption.
If the thermodynamic properties of a reaction mixture are required, obtain the desired thermodynamic properties of the reactants and the products.
Subtract the properties of the reactants from the products to obtain the reaction enthalpy, entropy, and Gibbs free energy depending on what is required.
This tool requires the chemical formula or common name of the species, temperature in Kelvin, and pressure in Pascals.
Outputs the thermodynamic properties in J/kmol or J/kmol-K.
    species_name (string, e.g., 'H2O')
    temperature_k (float, Kelvin)
    pressure_pa (float, Pascals)

- process_simulation_snapshot: Simulates a chemical process snapshot.
This tool should be used when simulating a chemical process such as combustion, reaction, or distillation.
If the temperature and pressure are not specified, assume standard conditions (298.15 Kelvin and 101325 Pascals) and inform the user of the assumption.
If the prompt is about obtaining the outlet composition and/or conversion of a chemical process, use this tool.
This requires the process type, inlet composition, temperature in Kelvin, pressure in Pascals, flow rate in moles per second, and optional reactor parameters (e.g., volume).
Outputs the outlet composition and conversion. If the temperature and pressure are not specified, assume 298.15 Kelvin and 101325 Pascals. State in the query output that those values were assumed.
    process_type (string, e.g., 'combustion', 'reaction', 'distillation')
    inlet_composition (string, e.g., 'CH4:1, O2:2, N2:7.52')
    temperature_k (float, Kelvin)
    pressure_pa (float, Pascals)
    flow_rate (float, moles per second)
    reactor_params (dict, optional, e.g., {'volume': 1.0})

- generate_phase_diagram: Generates a phase diagram for a mixture.
This tool should be used when generating a phase diagram for a mixture of components at specified temperature and pressure.
This tool should be used when generating the liquid and vapour compositions of a mixture at specified temperature and pressure.
If the temperature and pressure are not specified, assume standard conditions (298.15 Kelvin and 101325 Pascals) and inform the user of the assumption.
If the prompt is about obtaining the phase diagram data for a mixture, use this tool.
This tool requires the components, temperature in Kelvin, pressure in Pascals, and mole fractions.
Outputs the phase diagram data, including vapor and liquid compositions.
Always assume the temperature and pressure are 298.15 Kelvin and 101325 Pascals if not specified.
Components should be provided as a list of chemical formulas, and mole fractions should match the components.
Ensure the mole fractions sum to 1.0.
    components (list, e.g., ['CH4', 'O2', 'N2'])
    temperature_k (float, Kelvin) 
    pressure_pa (float, Pascals)
    mole_fractions (list, e.g., [0.1, 0.2, 0.7])



- get_wikipedia_data: Fetches accurate text data of a Wikipedia article based on a query.
Note: This tool is for retrieving detailed information from Wikipedia articles related to chemical processes and operations.
This requires a query string and outputs text data.
If the query involves asking for indepth knowledge about a chemical process or a chemical compound, it should be used to fetch the article content.
    For example, if the prompt is "What is benzene?" or a prompt that asks for basic information about a chemical compound or process, there is no need to use this tool to fetch the article content.
    However, a prompt such as "Provide a detailed overview of benzene" or a prompt that asks beyond basic information about a chemical compound or process should, use this tool to fetch the article content.
Based on the user prompt, obtain the keyword or topic they are interested in, and use that as the query input to fetch the relevant Wikipedia article.
If the prompt asks for safety operations for a chemical compound or process, always use this tool to fetch the article content.
Ensure the query is specific enough to retrieve relevant information (e.g., "Chemical engineering", "Catalysis", "Thermodynamics").
For this particular tool, don't return the JSON output directly in the response. Instead, return a summary of the contents.
The summary should include the title of the article, a brief overview of the main content, and a deep breakdown of the relevant sections that pertain to the user's query.
If the query is about safety information, always use this tool to fetch the article content.
Don't mention Wikipedia in your response to the query. State that the information is retrieved from a reliable source.
    query (string, e.g., 'Chemical engineering', "Ammonia")

    

Workflow for Handling Queries:
Parse User Intent: Determine if the query requires:
* Before processing, check if the query is within the domain of chemical operations and process control.
* If not, respond with: "I'm sorry, but that query is outside my expertise in chemical operations and process control. Please ask about chemical processes or related topics."
* Afterwards, check if each query requires a tool. If it requires a tool, ensure all necessary parameters are provided.
* If parameters are missing, ask the user to provide them (e.g., "Please provide the fuel and oxidizer for the adiabatic flame temperature calculation.").
* Once the parameters are available, immediately call one of the defined tools using the JSON format specified above.
* Then, output the tool call JSON and a brief message indicating the action being taken (e.g., "Executing calculation..." or "Fetching data...").
* If no tool is needed, respond with a detailed explanation based on the query.
* If the query is about safety information, check if a URL is provided. If not, ask for a URL to fetch data from.
* If a URL is provided, call the get_safety_information_from_url tool with the URL and optional keyword.
* If the query is about chemical properties or data, check if it requires a search on the Royal Society of Chemistry (RSC) website. If so, call the get_rsc_data tool with the query.
* If the query is about a chemical process simulation, call the process_simulation_snapshot tool with the required parameters.
* If the query is about generating a phase diagram, call the generate_phase_diagram tool with the required parameters.
* Never say the name of the tool you're using in your response. Just provide the results or the action being taken.
* At most, if you are required to provide information about yourself, just say: "I am Catalyst Mind, a chatbot and agent powered by Google Generative AI, specializing in chemical operations and process control. I can assist with calculations, data retrieval, and analysis related to chemical processes."




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


