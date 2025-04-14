
# 📘 DLiS InfoView - GenAI Enabled DLIS Data Workflow

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/python-3.10%2B-green.svg)](https://www.python.org/downloads/release/python-3100/)  
[![Streamlit](https://img.shields.io/badge/streamlit-✓-red.svg)](https://streamlit.io/)  
[![dlisio](https://img.shields.io/badge/dlisio-✓-blue.svg)](https://github.com/equinor/dlisio)  
[![OpenAI GPT-4](https://img.shields.io/badge/OpenAI-GPT_4-ff69b4.svg)](https://openai.com/)

---

## 📖 Overview
**DLiS InfoView** is an innovative Python-based web application designed for efficiently exploring, visualizing, and managing well log data stored in DLIS files (Digital Log Interchange Standard). Integrated with powerful Generative AI (GenAI), it provides seamless interactions, simplified insights, and smarter analytics to oil & gas industry professionals and researchers.

---

## 🎯 Why DLiS InfoView?
Well log data, stored primarily in binary DLIS files, is notoriously difficult to interpret, manage, and explore. Existing industry tools are often expensive, overly complex, and not user-friendly.

**DLiS InfoView** bridges this gap by:
- Offering simple, intuitive visualizations.
- Leveraging AI to enrich and contextualize DLIS data.
- Ensuring robust data health checks and smart recommendations.

---

## 🚀 Key Features
- DLIS File Explorer: Browse logical files, frames, channels, parameters, and tools.
- Smart DLIS Health Check: Automatically identify missing channels, duplicates, empty frames, and data inconsistencies.
- GenAI Summaries: Auto-generate meaningful file summaries tailored for petrophysicists or data engineers.
- AI Curve Explanation: Utilize GenAI to provide detailed, contextual, and petrophysics-friendly descriptions for any selected curve.
- Well Header Summaries: Easily extract critical well metadata (field, company, dates, well names).
- Export Workflows: Seamless LAS data export from selected DLIS curves.

---

## 🔧 Technology Stack
- Python 3.10+
- Streamlit
- dlisio
- Pandas & Plotly
- OpenAI GPT-4 & LangChain

---

## 🛠 Installation

```bash
git clone https://github.com/YourGitHub/DLiS-InfoView.git
cd DLiS-InfoView
pip install -r requirements.txt
streamlit run app.py
```

---

---

## 🔐 Environment Variables (.env)

Create a `.env` file in the project root directory to store your OpenAI API Key securely:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Make sure to install `python-dotenv` (already included in requirements.txt) and add `.env` to your `.gitignore` to avoid exposing sensitive keys.

---

## 🖥 Usage & Workflows

### 1. DLIS File Upload & Exploration
- Drag-and-drop DLIS files.
- Visualize metadata, frames, channels directly.

### 2. AI Assisted Analysis
- Generate AI Summary for contextual file summaries.
- Ask AI about specific log curves to understand their meaning and relevance.

### 3. DLIS Data Health Check
- Generate health reports highlighting data quality issues and recommendations.

### 4. Well Log Visualization
- Visualize and export selected curves easily to LAS format.

---

## 🎥 Video Demo
*https://youtu.be/auywDruHowA*


---

## 🤝 Contribution & Feedback
Feel free to reach out for ideas, collaborations, or feedback.

Email: info@deepdatawithmivaa.com 

---

## 📜 License
MIT License
