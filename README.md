DLIS InfoView

Overview

DLIS InfoView is a cutting-edge, GenAI-powered application specifically designed to simplify the exploration, visualization, and interpretation of Digital Log Interchange Standard (DLIS) well log files. Built to address common challenges encountered by petrophysicists, geologists, and data engineers, this tool significantly enhances productivity and insight extraction from complex well log data.

Key Features

Comprehensive DLIS File Overview: Easily browse and understand logical files, frames, channels, origins, parameters, and tools.

GenAI-Powered Smart Summaries: Automated generation of detailed, contextual summaries tailored for petrophysicists and data engineers.

Interactive Data Visualization: Intuitive selection and visualization of curves with export capabilities to PNG.

AI-Enhanced Quality Reports: Detailed reports highlighting missing depth channels, unit issues, duplicate entries, empty frames, and suspicious parameters.

Contextualized AI Curve Explanations: Real-time explanations of curve names and data characteristics powered by GPT-4.

Technologies Used

Python: Core programming language.

Streamlit: For interactive, web-based frontend.

dlisio: Python library by Equinor for handling DLIS files.

LangChain & OpenAI GPT-4: Advanced conversational and contextual GenAI.

Pandas & Plotly: Data manipulation and visualization.

Installation

Clone the repository and install dependencies:

git clone [Insert GitHub Repository URL]
cd dlis-infoview
pip install -r requirements.txt

Environment Setup

Create a .env file in the root directory and include your OpenAI API key:

OPENAI_API_KEY="your-openai-api-key"

Usage

Launch the Streamlit application:

streamlit run app.py

Open your web browser and navigate to:

http://localhost:8501

Demo

[Watch the Video Demonstration Here](Insert Link)

Contribution

We welcome contributions! Feel free to fork this repository, submit issues, or create pull requests.

Contact Mivaa

Interested in creating similar GenAI-enabled solutions? Contact us at SwapnilPatel22@gmail.com and explore how we can help transform your data workflows.
