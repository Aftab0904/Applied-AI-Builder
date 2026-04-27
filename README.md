# Detailed Diagnostic Report (DDR) Generator

This professional tool automates the generation of structural forensic diagnostic reports by analyzing site inspection data and thermal imaging. It leverages advanced Large Language Models (LLMs) to provide expert-level engineering insights, root cause analysis, and remediation strategies.

## Architecture

```mermaid
graph TD
    subgraph Frontend_Layer [Frontend Layer - Streamlit]
        UI[User Interface]
        UP[File Uploader]
        PV[Report Preview]
    end

    subgraph Backend_Layer [Backend Layer - FastAPI]
        API[REST API Endpoints]
        EX[Data Extractor]
        GEN[Report Generator]
    end

    subgraph Processing_Layer [Processing Layer]
        MUP[PyMuPDF Parser]
        REG[Regex Pattern Matcher]
    end

    subgraph AI_Layer [AI Intelligence Layer]
        OR[OpenRouter API]
        LLM[LLM Engine]
    end

    UI --> UP
    UP --> API
    API --> EX
    EX --> MUP
    EX --> REG
    API --> GEN
    GEN --> OR
    OR --> LLM
    LLM --> GEN
    GEN --> PV
    PV --> UI

    style Frontend_Layer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Backend_Layer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Processing_Layer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style AI_Layer fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
```

## Technical Stack

| Category | Technology |
| :--- | :--- |
| Frontend | Streamlit |
| Backend | FastAPI |
| Language | Python |
| PDF Processing | PyMuPDF (fitz) |
| AI Integration | OpenRouter API |
| Environment | Python Dotenv |
| API Server | Uvicorn |

## Project Overview

The DDR Generator streamlines the workflow for structural and civil engineers. By uploading site inspection reports and thermal imaging PDFs, the system automatically:

1.  Identifies moisture intrusion patterns.
2.  Correlates thermal anomalies with physical observations.
3.  Determines probable root causes using expert engineering logic.
4.  Assesses severity and recommends practical actions.

## Visual Demo

### Application Interface
![Upload Interface](Demo_ScreenShots/Screenshot%20(231).png)

### Data Extraction Process
![Extraction](Demo_ScreenShots/Screenshot%20(232).png)

### Structural Analysis
![Structural Analysis](Demo_ScreenShots/Screenshot%20(233).png)

### Thermal Mapping
![Thermal Mapping](Demo_ScreenShots/Screenshot%20(234).png)

### Image Correlation
![Image Correlation](Demo_ScreenShots/Screenshot%20(235).png)

### Expert Report Generation
![Report Generation](Demo_ScreenShots/Screenshot%20(236).png)

### Final DDR Preview
![Final Report 1](Demo_ScreenShots/Screenshot%20(237).png)
![Final Report 2](Demo_ScreenShots/Screenshot%20(238).png)
![Final Report 3](Demo_ScreenShots/Screenshot%20(239).png)

## Local Setup

### Prerequisites
- Python 3.8+
- OpenRouter API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aftab0904/Applied-AI-Builder.git
   cd ddr_generator_portable
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file and add your API key:
   ```text
   OPENROUTER_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   # Start backend
   python app.py
   
   # Start frontend (in a new terminal)
   streamlit run streamlit_app.py
   ```
