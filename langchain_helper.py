import os
import json
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import logging
load_dotenv()

@st.cache_data(show_spinner=False)
def get_structured_logical_file_summary_cached(summary_input: str, persona: str):
    return get_structured_logical_file_summary(summary_input, persona)

# Logging setup
logging.basicConfig(level=logging.INFO)

# GenAI explanation for a curve
def get_curve_explanation_from_ai(curve_name: str) -> str:
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        logging.error("Missing OpenAI API key.")
        return "❌ OpenAI API key not found. Please configure it properly."

    prompt = PromptTemplate.from_template(f"""
    You are a senior oilfield well log expert specializing in petrophysics and log data interpretation.

    Please explain the DLIS or LAS curve with the following name:
    `{curve_name}`

    Your explanation should include:
    1. What does this curve typically measure?
    2. What type of tool usually records it?
    3. Typical usage in oil & gas or formation evaluation.
    4. Expected units (if any).
    5. Interpretation tips, warnings, or remarks.

    Be concise but insightful.
    The explanation should help a petrophysicist or data engineer quickly understand this curve when reviewing well log data.

    If you don't recognize the curve, explicitly say so, but try to guess based on common industry naming patterns.
    """)

    try:
        llm = ChatOpenAI(
            temperature=0.1,
            model="gpt-4",
            openai_api_key=openai_api_key
        )

        prompt_text = prompt.format()  # Generate plain string
        response = llm.predict(prompt_text)

        return response

    except Exception as e:
        logging.error(f"GenAI curve explanation failed: {e}")
        return f"❌ AI explanation failed: {e}"


def get_structured_logical_file_summary(summary_input: str, persona: str):
    prompt = ChatPromptTemplate.from_template(
        """
You need to extract actionable insights from well log data, focusing on measurement types, tools used, and key data points for analysis.

Summarize the metadata from the DLIS file focusing on the well information (e.g., well name, field, and logging company). 
Emphasize the measurement types (e.g., depth, azimuth, inclinations) and tools used for logging, along with any relevant details about the origin, such as the company and date. 
Provide key insights into the data's potential use for reservoir evaluation and formation analysis.

Metadata:

{summary_input}

"""
    )

    llm = ChatOpenAI(
        temperature=0.3,
        model="gpt-4",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    chain: Runnable = prompt | llm | StrOutputParser()
    return chain.invoke({"summary_input": summary_input, "persona": persona})


def summarize_metadata_for_prompt(logical_file) -> str:
    result_lines = []


    # # 1. ORIGIN Summary (Full Origin Data)
    # origins = getattr(logical_file, 'origins', [])
    # if origins:
    #     for origin in origins:
    #         try:
    #             # Get the entire description of the origin
    #             origin_data = origin.describe()
    #
    #             # Convert the origin data into a string representation for the LLM
    #             origin_summary = json.dumps(origin_data, indent=2)
    #
    #             # Append the full origin information to the result lines
    #             result_lines.append(f"ORIGIN INFO:\n{origin_summary}")
    #
    #         except Exception as e:
    #             logging.error(f"Error processing origin: {e}")
    #             continue

    # 1. ORIGIN Summary (Full Origin Data)
    origins = getattr(logical_file, 'origins', [])
    if origins:
        origin_summaries = []  # Store all origin summaries here
        for origin in origins:
            try:
                # Get the entire description of the origin
                origin_description = origin.describe()  # This will get a descriptive string of the origin

                # You can directly append this description to the result_lines list
                origin_summaries.append(
                    f"ORIGIN INFO:\n{origin_description}")  # You can customize how this is formatted

            except Exception as e:
                logging.error(f"Error processing origin: {e}")
                continue

        # Append to result lines
        result_lines.extend(origin_summaries)  # Add the origin summaries to your result lines

    # 2. FRAME Summary
    frames = getattr(logical_file, 'frames', [])
    frame_summaries = []
    for frame in frames:
        try:
            frame_name = getattr(frame, 'name', 'Unnamed')
            num_channels = len(getattr(frame, 'channels', []))
            frame_summaries.append(f"{frame_name} ({num_channels} channels)")
        except Exception:
            continue

    if frame_summaries:
        result_lines.append("FRAMES:\n- " + "\n- ".join(frame_summaries))

    # 3. CHANNEL Summary
    channels = getattr(logical_file, 'channels', [])
    if channels:
        channel_names = sorted([ch.name for ch in channels if hasattr(ch, 'name')])
        channel_chunk = channel_names[:25]  # cap for LLM
        result_lines.append("SAMPLE CHANNELS:\n- " + "\n- ".join(channel_chunk))
        if len(channel_names) > 25:
            result_lines.append(f"... and {len(channel_names) - 25} more")

    return "\n\n".join(result_lines)
