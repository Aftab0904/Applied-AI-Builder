# Applied AI Builder: Automated Detailed Diagnostic Report (DDR) Workflow

This technical implementation provides an automated solution for converting raw, multi-source structural inspection data into professional, client-ready forensic reports. The system is designed to handle the logical merging of physical site observations with thermal diagnostic findings, ensuring high accuracy and structural integrity.

## Advanced System Architecture

The following diagram details the multi-layered reasoning engine, from raw data extraction to the final synthesis and conflict resolution layers.

```mermaid
graph TD
    subgraph Input_Layer [Data Acquisition Layer]
        I[Inspection PDF]
        T[Thermal PDF]
        ENV[.env Configuration]
    end

    subgraph Processing_Layer [Extraction & Analysis Engine]
        direction TB
        MUP[PyMuPDF: Image/Text Stream]
        REG[Regex: ID & Pattern Matching]
        IMG[Image-Context Correlation]
        
        MUP --> REG
        REG --> IMG
    end

    subgraph Reasoning_Layer [Synthesis & Logic Engine]
        direction TB
        ML[Logical Merging Logic]
        CD[Conflict Detection Node]
        GA[Gap Analysis: Not Available Logic]
        VP[Validation & Prompt Engineering]
        
        ML --> CD
        CD --> GA
        GA --> VP
    end

    subgraph Output_Layer [Assignment-Compliant Deliverable]
        DDR[Final DDR Document]
        MD[Markdown Rendering]
        AS[Asset Mapping: assets/]
    end

    Input_Layer --> Processing_Layer
    Processing_Layer --> Reasoning_Layer
    Reasoning_Layer --> Output_Layer

    %% Styling for colorful boxes
    style Input_Layer fill:#eceff1,stroke:#455a64,stroke-width:2px
    style Processing_Layer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Reasoning_Layer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Output_Layer fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px

    %% Node styling
    classDef engine fill:#fff,stroke:#333,stroke-dasharray: 5 5;
    class CD,GA,REG engine;
```

## Technical Stack

| Category | Technology |
| :--- | :--- |
| Frontend Framework | Streamlit (Interactive UI) |
| Backend Framework | FastAPI (REST API Engine) |
| Data Extraction | PyMuPDF (fitz) |
| AI Reasoning | OpenRouter API / LLM |
| Language | Python 3.8+ |
| Image Processing | Regex-based Asset Mapping |

## Core Engineering Principles (Assignment Compliance)

### 1. Intelligent Data Merging
The system identifies corresponding areas across different documents by correlating "Photo IDs" with "Thermal IDs." This ensures that a moisture reading from a thermal camera is accurately placed alongside the physical observation of the same structural element.

### 2. Handling Missing and Conflicting Data
In adherence to professional engineering standards, the system follows strict rules:
- **Conflict Management:** If temperature readings contradict physical observations (e.g., "Dry" text vs "Wet" thermal), the report explicitly highlights the discrepancy.
- **Data Gap Identification:** If an area lacks an image or data, the system explicitly labels the section as "Not Available" or "Image Not Available" rather than inventing facts.
- **Anti-Hallucination:** The AI engine is constrained by a system prompt that forbids the creation of information not present in the source files.

### 3. Image Contextualization
Images are extracted and contextualized. Each image is placed directly under the observation it supports. The system filters out unrelated assets (logos/icons) to ensure only relevant diagnostic evidence is included.

## Visual Demo & Workflow

### 1. File Upload & Interface
The user uploads the Sample Inspection and Thermal Reports via the Streamlit interface.
![Upload Interface](Demo_ScreenShots/Screenshot%20(231).png)

### 2. Multi-Source Extraction
The backend processes both files, extracting text strings and saving images to the local asset directory.
![Extraction Process](Demo_ScreenShots/Screenshot%20(232).png)

### 3. AI-Driven Synthesis
The LLM analyzes the extracted data to determine root causes and severity levels based on real-world engineering logic.
![Analysis](Demo_ScreenShots/Screenshot%20(233).png)

### 4. Thermal Mapping & Correlation
Thermal findings are paired with physical photos to provide a complete picture of the structural health.
![Thermal Mapping](Demo_ScreenShots/Screenshot%20(234).png)
![Correlation](Demo_ScreenShots/Screenshot%20(235).png)

### 5. Final Structured Report
The output is a client-ready DDR containing all 7 required sections, including Property Issue Summary and Recommended Actions.
![Final Report 1](Demo_ScreenShots/Screenshot%20(237).png)
![Final Report 2](Demo_ScreenShots/Screenshot%20(238).png)

## Local Setup

1. **Environment Setup:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Installation:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration:**
   Add your `OPENROUTER_API_KEY` to the `.env` file.

4. **Execution:**
   - Start the backend: `python app.py`
   - Start the frontend: `streamlit run streamlit_app.py`
