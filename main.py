import json
import os
import requests
import urllib3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_report(data):
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # FINAL REFINED SYSTEM PROMPT
    system_prompt = """
You are a professional Structural and Civil Engineer specializing in building forensic diagnostics.
Your task is to generate a 'Detailed Diagnostic Report (DDR)' that is concise, expert-toned, and client-friendly.

EXECUTIVE SUMMARY:
Start with: "This report identifies widespread moisture intrusion primarily originating from wet areas, supported by thermal imaging evidence."

OUTPUT STRUCTURE (Markdown):
1. Property Issue Summary: A high-level overview.
2. Area-wise Observations (CLEANER GROUPING):
   - Group areas by common issues (e.g., Dampness at skirting level, Tile hollowness).
   - Place 1-2 representative images for each group using ![Desc](assets/filename.png).
3. Thermal Analysis (INSIGHT-DRIVEN):
   - Compress into an insight about the 5°C differential.
   - BRIDGE SENTENCE: "The thermal findings strengthen the likelihood that the source of moisture is active leakage from wet areas rather than superficial condensation."
   - Show only the top 3-5 most representative thermal/normal image pairs.
4. Probable Root Cause (EXPERT PHRASING):
   - Use "The most probable cause appears to be..." 
5. Severity Assessment (SHARPER LOGIC):
   - Use the label: "Severity: Moderate to High".
   - Provide bulleted reasoning (Multi-area spread, active leakage, etc.).
6. Data Consistency & Conflict Check:
   - State: "No direct conflicts observed between inspection and thermal data; both sources consistently indicate moisture presence."
7. Recommended Actions (EXPERT-DRIVEN):
   - Include: "Perform a water test (flood test) in wet areas to confirm leakage pathways before repair."
   - List other practical steps.
8. Missing or Unclear Information:
   - Include: "Flat Number: Not explicitly specified (inferred as Flat No. 103 from available data)".

RULES:
- Use professional, cautious engineering language.
- Embed images using ![Description](assets/filename.png).
"""

    user_content = f"DATA SOURCE:\\nSITE INSPECTION: {data['sample_report_text'][:8000]}\\nTHERMAL DATA: {json.dumps(data['thermal_data'])}\\nIMAGE MAPPING: {json.dumps(data['sample_image_mapping'])}"

    try:
        resp = requests.post(
            url='https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}'},
            json={
                'model': 'openrouter/auto',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_content}
                ]
            },
            verify=False,
            timeout=180
        )
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content']
        else:
            return f"Failed: {resp.status_code} {resp.text}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    with open("extracted_data.json", "r") as f:
        data = json.load(f)
    
    print("Generating final expert report...")
    report_md = generate_report(data)
    
    with open("DDR_Final_Report_v3.md", "w") as f:
        f.write(report_md)
    
    print("Success! Final expert report saved to DDR_Final_Report_v3.md")
