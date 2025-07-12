# Catalyst Mind: An Intelligent Chemical Engineering Agent powered by Google Generative AI for Chemical Operations and Process Control

An interactive AI assistant built using a **blurred/darkened background image**, Gemini API thus providing access to Google Generative AI interface, alongside the use of modern UI enhancements.  
<img width="1920" height="822" alt="Screenshot (287)" src="https://github.com/user-attachments/assets/84c3bce3-77d8-4e87-a85d-61ffea04e068" />

---
## 🧬Overview
Catalyst Mind is an intelligent AI agent designed to be your go-to resource for all things related to chemical operations and process control. Powered by Google's Gemini 1.5 Flash multimodal AI, this application can answer your text queries, interpret process diagrams (via image uploads), and even extract information from PDF and TXT documents to provide comprehensive and accurate insights.

Whether you're a student, an engineer, or just curious about chemical processes, Catalyst Mind is here to help you understand complex concepts, troubleshoot issues, and enhance your knowledge in the field.

What sets Catalyst Mind is its ability to solve various simulation processes and obtain quick access to thermodynamic data which typically requires a complex (time-consuming) experimentation and analysis process.


## 🚀 Features  

- ✅ **Multimodal Interaction**: Engage with the AI using both text and image inputs. Upload diagrams, flowcharts, or equipment photos for analysis. 📸
- ✅ **Document Processing**: Get insights from your PDF and TXT files. Upload reports, manuals, or research papers, and Catalyst Mind will extract relevant text to inform its responses. 📄  
- ✅ **Chemical Operations & Process Control Expertise**: Specialized knowledge base focused on chemical engineering principles, reactions, process control strategies (PID, advanced control), and safety protocols. 🔬 
- ✅ **Real-time Responsese**: Powered by Gemini 1.5 Flash for quick and relevant answers. ⚡
- ✅ **Streamlit Interface**:
  - Built with Streamlit.
  - Interactive sidebar with dropdowns.
  - Downloadable chat session feature.
  - Mobile-responsive and user-friendly interface ✨.  
- ✅ **Persistent Chat History**: Your conversation is maintained within the session for a seamless experience. 💬
- ✅ **Chemical Process & Thermodynamic Calculations**:
  - Adiabatic flame temperature using **Cantera**
  - Molecular weight retrieval for chemical species
  - Plans to support enthalpy, Gibbs free energy, and reaction kinetics 🔬
- ✅ **Scientific Knowledge Retrieval**: Privides real time search of Wikipedia articles to extract relevant data.
- ✅ **Agentic AI Behavior**: Uses Gemini’s tool-calling system to autonomously interpret queries, call on appropriate tools when necessary and integrate the results of the tool into responses.

---
# 🛠️ Tech Stack

| Component        | Description                           |
|------------------|---------------------------------------|
| Streamlit        | Frontend web app                      |
| Google Generative AI (Gemini) | Language model + tool-calling agent |
| Cantera          | Thermodynamic simulations & combustion |
| BeautifulSoup    | Web scraping (Wikipedia, RSC)         |
| Pillow           | Image processing                      |
| PyPDF2           | PDF parsing                           |


---

## ❇️ Setup  

### 1. Prerequisites  
- Python 3.8+  
- Streamlit (`pip install streamlit`)  
- Google Generative AI SDK (`pip install google-generativeai`)  

### 2. Installation
```bash
git clone https://github.com/your-repo/your-app.git
cd your-app
pip install -r requirements.txt
```

### 3. Setting of Google Generative API Key
```bash
# .streamlit/secrets.toml (Create a streamlit folder in your dierctory and create
# a secrets.toml file in which the code displayed down here is stored).
GEMINI_API_KEY = "your-api-key-here"
```

### 4. Running the Streamlit Application
```bash
streamlit run app.py
```
This will trigger "http://localhost:8501" in your browser in which you can:
- Ask chemical engineering questions.
- Upload PDFs or images for processing.
- Request calculations (e.g. flame temperature).
- View or download your chat session

---
📁 Directory Structure
```bash
📦 Catalyst-Mind
├── app.py                 # Main Streamlit app
├── README.md
├── requirements.txt
└── .streamlit/
    └── secrets.toml       # API key config (optional)
```
---

## ☁️ Deployment on Streamlit Community Cloud
Streamlit Community Cloud makes deployment incredibly easy!

### 1. Push Your Code to GitHub:
Ensure your entire project (including app.py, requirements.txt, and the images folder if you're using a local background) is pushed to a GitHub repository. Remember to keep secrets.toml out of your repository!

### 2. Go to Streamlit Community Cloud:
Visit share.streamlit.io and log in with your GitHub account.

### 3. Deploy a New App:
Click "New app" or "Deploy an app."
Select your repository, branch (e.g., main), and the main file path (app.py).

### 4. Configure Secrets:
Crucially, in the deployment settings, expand the "Advanced settings" section.
Add your GEMINI_API_KEY directly in the "Secrets" text area.

### 5. Deploy:
Click the "Deploy!" button. Streamlit will build and launch your application.
Once deployed, you'll get a public URL (e.g., https://your-app-name.streamlit.app/) that you can share with anyone!

---
## Usage 💡
### 1. Enter your query: 
Type your question about chemical operations or process control in the chat input box at the bottom.

### 2. Upload files: 
Click the file upload icon in the chat input to upload images (PNG, JPG, JPEG), PDF documents, or TXT files.

### 3. Get responses: 
Catalyst Mind will process your input (text and/or files) and provide a relevant response.

### 4. Continue the conversation: 
The chat history is maintained, allowing for follow-up questions and deeper discussions.

---
## ✨ Example Queries
### 1. What is a distillation column? 
The prompt will load as it is pertaining to a chemical engineering process.

### 2. How do I make a bomb?
The application won't provide any relevant information due to the possibility to significantly affect human life.

### 3. Explain the history of the world.
The application won't provide any relevant information as the query doesn't pertain to chemical processes.

### 4. Upload image, PDF or Text File
Based on the contents of the image or file being uploaded, the application would provide necessary information if pertaining to chemical processes.

### 5. Calculate the adiabatic temperature of methan in air at 300K and 1 atm

### 6. What is the molecular weight of CO2?

### 7. What is the equilibrium composition of a mixture containing 1mole of CH4, 3 moles of hydrogen and 7.3 moles of nitrogen at 453Kelvin and 2 bar?

N.B: Find attached a sample picture that can be downloaded and fed as a prompt to the application
![Picture1](https://github.com/user-attachments/assets/648ce584-7415-426d-b44c-af43fb325ae5)

