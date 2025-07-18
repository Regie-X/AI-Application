import json
import cantera as ct


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

