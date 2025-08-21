# threat-report-ttp-parser

This project is a powerful yet easy-to-use web tool designed to assist cybersecurity analysts, researchers, and students. By leveraging the natural language processing capabilities of Google's Gemini 1.5 Flash model, this application parses unstructured threat intelligence reports and automatically identifies and lists the corresponding MITRE ATT&CK TTPs.

Simply paste a report into the application, and it will return a structured list of tactics and techniques, helping to speed up analysis and standardize threat data.

## How to Run This Project Locally

Follow these steps to get the MITRE ATT&CK TTP Extractor running on your own machine.

### 1. Prerequisites

- Python 3.8+: Make sure you have a recent version of Python installed.
- Git: You will need Git to clone the repository.
- Google Gemini API Key: You must have a valid API key from the Google AI Studio. You can get one [here](https://makersuite.google.com/app/apikey).

### 2. Clone the Repository

Open your terminal or command prompt and run the following commands to clone the project:

```

git clone https://github.com/tyranny001/threat-report-ttp-parser.git
cd threat-report-ttp-parser

```

### 3. Install Dependencies

This project uses a few Python libraries listed in `requirements.txt`.

Install them using pip:

```

pip install -r requirements.txt

```

### 4. Set Your API Key

You need to set your Gemini API key as an environment variable. This is a secure way to handle keys without hardcoding them into the application.

- On **Windows (Command Prompt):**

```

set GEMINI_API_KEY="YOUR_API_KEY_HERE"

```

- On **macOS / Linux:**

```

export GEMINI_API_KEY="YOUR_API_KEY_HERE"

```

Replace `"YOUR_API_KEY_HERE"` with the actual key you obtained from Google.

> **Important:** You must set this variable in the same terminal session you use to run the application.

### 5. Run the Streamlit App

Once the setup is complete, run the following command in your terminal. This method is recommended as it directly uses the Python interpreter to run the module.

```

python -m streamlit run app.py

```

Your web browser should automatically open with the application running. If not, the terminal will provide a local URL (usually http://localhost:8501) that you can visit.
