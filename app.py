import streamlit as st
import os
import google.generativeai as genai
import logging

# --- Basic Configuration ---
# Configure logging to show messages in the terminal.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sets the page layout to wide, and defines a title and icon for the browser tab.
st.set_page_config(
    layout="wide",
    page_title="MITRE ATT&CK TTP Extractor",
    page_icon="🔍"
)

# --- Gemini API Configuration & State Management ---
# Initialize session state variables to track API status
if 'gemini_configured' not in st.session_state:
    st.session_state.gemini_configured = False

# Function to configure Gemini API
def configure_gemini():
    """Attempts to configure the Gemini API and updates session state."""
    api_key = None
    try:
        # This is the standard way to access secrets when deployed on Streamlit Community Cloud.
        logging.info("Attempting to get API key from Streamlit secrets.")
        api_key = st.secrets["GEMINI_API_KEY"]
        logging.info("Found API key in Streamlit secrets.")
    except (st.errors.StreamlitAPIException, KeyError):
        # This block now correctly catches the error when secrets aren't found locally.
        # It then falls back to checking the environment variable.
        logging.info("Streamlit secret not found. Falling back to environment variable.")
        api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.gemini_configured = True
            logging.info("Gemini API configured successfully.")
        except Exception as e:
            st.error(f"Failed to configure Gemini API with the provided key: {e}")
            logging.error(f"Failed to configure Gemini API: {e}")
            st.session_state.gemini_configured = False
    else:
        st.session_state.gemini_configured = False
        logging.warning("Gemini API key not found in st.secrets or environment variables.")

# --- Core Functionality ---
@st.cache_data(show_spinner=False)
def extract_ttps_from_report(text: str):
    """
    Uses the Gemini 1.5 Flash model to extract MITRE ATT&CK TTPs from a given text.

    Args:
        text: The cyber threat intelligence report text.

    Returns:
        A string containing the extracted TTPs in a formatted list,
        or an error message if the API call fails.
    """
    if not st.session_state.get('gemini_configured', False):
        logging.error("Extraction called but Gemini is not configured.")
        return "Error: Gemini API key is not configured. Cannot proceed."

    prompt = f"""
You are an expert cybersecurity analyst. Your task is to extract MITRE ATT&CK Tactics, Techniques, and Sub-techniques (TTPs) from the provided cyber threat intelligence report.
**Instructions:**
1.  Carefully read the threat report below.
2.  Identify all mentions of actions that correspond to the MITRE ATT&CK framework.
3.  Format your output *exactly* as follows, using plain text:
    - Tactic: [Tactic Name] (ID: [Tactic ID])
      - Technique: [Technique Name] (ID: [Technique ID])
      - Sub-technique: [Sub-technique Name] (ID: [Sub-technique ID])  (if applicable)
4.  **Crucially, only include TTPs that are explicitly mentioned or strongly implied in the report text.** Do not infer or add any information that is not present.
5.  If no TTPs are found, state "No MITRE ATT&CK TTPs were identified in the report."
**Threat Report:**
---
{text}
---
    """

    try:
        logging.info("Generating content with Gemini model...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        logging.info("Successfully received response from Gemini.")
        return response.text.strip()
    except Exception as e:
        st.error(f"An error occurred while contacting the Gemini API: {e}")
        logging.error(f"An error occurred during Gemini API call: {e}", exc_info=True)
        return None

# --- Sample Data ---
SAMPLE_REPORT = """
**Threat Intelligence Report: FIN7 Operations**
**Date:** 2024-10-26
**Executive Summary:**
This report details the recent activities of the financially motivated threat group FIN7. The group continues to target retail and hospitality sectors. Our analysis indicates a multi-stage attack methodology, beginning with a spearphishing campaign.
**Initial Access:**
FIN7 initiates its campaigns with carefully crafted spearphishing emails containing malicious attachments. These attachments are often Word documents with macros (T1566.001) that, when enabled, execute a PowerShell script to download the initial payload.
**Execution & Persistence:**
The downloaded payload is a PowerShell script (T1059.001) that establishes persistence by creating a scheduled task (T1543.003) set to run periodically. This ensures the malware survives system reboots.
"""

# --- Main App UI ---
def main():
    """Main function to run the Streamlit UI."""
    logging.info("--- Streamlit App Starting ---")

    # Configure Gemini on first run
    if 'gemini_configured' not in st.session_state or not st.session_state.gemini_configured:
        configure_gemini()

    st.title("🔍 MITRE ATT&CK TTP Extractor with Gemini")
    st.markdown("This tool uses Google's `gemini-1.5-flash` model to analyze a threat intelligence report and extract Tactics, Techniques, and Procedures (TTPs) based on the MITRE ATT&CK framework.")

    # Show a persistent warning if the API key is not configured
    if not st.session_state.gemini_configured:
        st.warning("⚠️ Gemini API key not found or invalid. Please set the `GEMINI_API_KEY` environment variable and restart the app.")

    st.info("💡 **How to use:** Paste a threat intelligence report into the text box below and click the 'Extract TTPs' button. A sample report is pre-loaded for demonstration.", icon="💡")
    st.divider()

    user_input = st.text_area(
        "📝 **Paste the Threat Report Text Here:**",
        value=SAMPLE_REPORT,
        height=400,
        help="You can use the sample report or paste your own."
    )

    if st.button("🚀 Extract TTPs", type="primary", use_container_width=True, disabled=(not st.session_state.gemini_configured)):
        if user_input:
            with st.spinner("Analyzing report and extracting TTPs using Gemini... Please wait."):
                extracted_ttps = extract_ttps_from_report(user_input)
                if extracted_ttps:
                    st.success("✅ TTPs Extracted Successfully!")
                    st.code(extracted_ttps, language="markdown")
                else:
                    st.error("❌ Failed to extract TTPs. Check the terminal for error logs.")
        else:
            st.warning("Please paste a report into the text box before extracting.")

    st.divider()
    st.markdown("Powered by [Google Gemini](https://ai.google.dev/) and [Streamlit](https://streamlit.io).")
    logging.info("--- Streamlit App UI Rendered ---")

if __name__ == "__main__":
    main()
