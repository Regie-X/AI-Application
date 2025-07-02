# Catalyst Mind: A Web Application powered by Google Generative AI for Chemical Operations and Process Control

A sleek Streamlit web application featuring a **blurred/darkened background image**, AI integration (Gemini API), and modern UI enhancements.  
![image](https://github.com/user-attachments/assets/feb46881-e31a-4811-b2b5-9d4d07198b36)

---
## 🧬Overview
Catalyst Mind is an intelligent chatbot designed to be your go-to resource for all things related to chemical operations and process control. Powered by Google's Gemini 1.5 Flash multimodal AI, this application can answer your text queries, interpret process diagrams (via image uploads), and even extract information from PDF and TXT documents to provide comprehensive and accurate insights.

Whether you're a student, an engineer, or just curious about chemical processes, Catalyst Mind is here to help you understand complex concepts, troubleshoot issues, and enhance your knowledge in the field


## 🚀 Features  

- ✅ **Multimodal Interaction** – Engage with the AI using both text and image inputs. Upload diagrams, flowcharts, or equipment photos for analysis. 📸
- ✅ **Document Processing** – Get insights from your PDF and TXT files. Upload reports, manuals, or research papers, and Catalyst Mind will extract relevant text to inform its responses. 📄  
- ✅ **Chemical Operations & Process Control Expertise** – Specialized knowledge base focused on chemical engineering principles, reactions, process control strategies (PID, advanced control), and safety protocols. 🔬 
- ✅ **Real-time Responsese** –  Powered by Gemini 1.5 Flash for quick and relevant answers. ⚡
- ✅ **Streamlit Interface** – A clean, intuitive, and interactive web interface built with Streamlit. ✨  
- ✅ **Persistent Chat History** – Your conversation is maintained within the session for a seamless experience. 💬 


---

## 🛠️ Setup  

### 1. Prerequisites  
- Python 3.8+  
- Streamlit (`pip install streamlit`)  
- Google Generative AI SDK (`pip install google-generativeai`)  

### 2. Installation  
git clone https://github.com/your-repo/your-app.git
cd your-app
pip install -r requirements.txt

### 3. Setting of Google Generative API Key

### 4. Addition of a Local Background Image (Aesthetics)

### 5. Running the Streamlit Application

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
## Sample Prompts
### 1. What is a distillation column? 
The prompt will load as it is pertaining to a chemical engineering process.

### 2. How do I make a bomb?
The application won't provide any relevant information due to the possibility to significantly affect human life.

### 3. Explain the history of the world.
The application won't provide any relevant information as the query doesn't pertain to chemical processes.

### 4. Upload image, PDF or Text File
Based on the contents of the image or file being uploaded, the application would provide necessary information if pertaining to chemical processes.

N.B: Find attached a sample picture that can be downloaded and fed as a prompt to the application
![Picture1](https://github.com/user-attachments/assets/648ce584-7415-426d-b44c-af43fb325ae5)

