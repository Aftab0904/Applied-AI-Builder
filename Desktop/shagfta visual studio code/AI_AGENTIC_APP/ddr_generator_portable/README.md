# Detailed Diagnostic Report (DDR) Generator

This implementation provides an automated solution for converting raw, multi-source structural inspection data into professional, client-ready diagnostic reports. The system is designed to handle the logical merging of physical site observations with technical thermal findings, ensuring high accuracy and structural integrity.

## System Architecture

The following diagram illustrates the multi-layered reasoning engine, from technical data acquisition to the final synthesis and correlation layers.

```mermaid
graph TD
    subgraph Ingestion [Data Acquisition]
        I[Inspection PDF]
        T[Thermal PDF]
        ENV[.env Configuration]
    end

    subgraph Parsing [Technical Extraction Engine]
        direction TB
        MUP[PyMuPDF: Binary Image/Text Stream]
        REG[Regex: Pattern Matching for ID Mapping]
        IMG[Image-Context Correlation Pipeline]
        
        MUP --> REG
        REG --> IMG
    end

    subgraph Reasoning [Cognitive Synthesis Engine]
        direction TB
        OR[OpenRouter Gateway]
        LLM[Multimodal Reasoning: GPT-4o / Claude]
        PER[Engineering Persona Simulation]
        JOIN[Thermal-Visual Logic Join]
        
        OR --> LLM
        LLM --> PER
        PER --> JOIN
    end

    subgraph Deliverable [Production Output]
        DDR[Final Diagnostic Report]
        MD[Markdown Rendering]
        AS[Evidence Assets: assets/]
    end

    Ingestion --> Parsing
    Parsing --> Reasoning
    Reasoning --> Deliverable

    %% Advanced Styling
    style Ingestion fill:#f5f5f5,stroke:#333,stroke-width:2px
    style Parsing fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Reasoning fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Deliverable fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

## The Role of OpenRouter

OpenRouter serves as the central API gateway for the project, providing a unified interface to access world-class language and vision models. 

### Why OpenRouter is used:
- Model Versatility: It allows the system to switch between different high-reasoning models like Claude 3.5 Sonnet and GPT-4o without changing the backend logic.
- Performance Optimization: It automatically routes requests to ensure that the most efficient and accurate model is used for complex engineering assessments.
- Unified Integration: By using one API, the system can leverage multiple model providers, ensuring high availability and reliability for processing technical documents.

## Handling Image and Visual Data

A core feature of this system is its ability to handle technical visual evidence alongside text.

### Technical Extraction Logic
Standard text extractors often miss the relationship between a photo and its label. This project uses a custom pipeline built with PyMuPDF to extract binary image data directly from the source PDFs. We use regular expressions to identify specific IDs like "Photo 1" or "RB02380X" within the report text. This creates a mapping table that ensures every site observation is physically linked to the correct evidence file.

### Multimodal Vision Analysis
The system leverages multimodal AI models that process both text and pixels. When an image is sent to the reasoning engine, the model analyzes the visual patterns—such as the color gradients in a thermal map—to confirm structural issues like moisture intrusion or heat loss.

### Logic Bridge
The system prompt includes a "logic bridge" that forces the AI to look for a 5°C temperature differential in the thermal data before confirming a visual report of moisture. This ensures that the final report is backed by scientific data rather than just visual guesswork.

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
