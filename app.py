from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import json
import shutil
from extractor import extract_from_sample_report, extract_from_thermal_images
from main import generate_report

app = FastAPI()

# Ensure directories exist
if not os.path.exists("assets"):
    os.makedirs("assets")

# Serve static files (images)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/status")
def get_status():
    return {
        "inspection_pdf": os.path.exists("Sample Report.pdf"),
        "thermal_pdf": os.path.exists("Thermal Images.pdf"),
        "extracted_data": os.path.exists("extracted_data.json"),
        "report_md": os.path.exists("DDR_Final_Report_v3.md")
    }

@app.post("/upload")
async def upload_files(inspection: UploadFile = File(...), thermal: UploadFile = File(...)):
    try:
        with open("Sample Report.pdf", "wb") as buffer:
            shutil.copyfileobj(inspection.file, buffer)
        with open("Thermal Images.pdf", "wb") as buffer:
            shutil.copyfileobj(thermal.file, buffer)
        return {"message": "Files uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract")
def run_extraction():
    if not os.path.exists("Sample Report.pdf") or not os.path.exists("Thermal Images.pdf"):
        raise HTTPException(status_code=400, detail="PDFs missing. Upload them first.")
    try:
        sample_text, sample_mapping = extract_from_sample_report("Sample Report.pdf", "assets")
        thermal_text, thermal_data = extract_from_thermal_images("Thermal Images.pdf", "assets")
        
        data = {
            "sample_report_text": sample_text,
            "sample_image_mapping": sample_mapping,
            "thermal_report_text": thermal_text,
            "thermal_data": thermal_data
        }
        
        with open("extracted_data.json", "w") as f:
            json.dump(data, f, indent=4)
            
        return {"message": "Extraction complete", "images_extracted": len(sample_mapping) + len(thermal_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
def run_generation():
    if not os.path.exists("extracted_data.json"):
        raise HTTPException(status_code=400, detail="Extracted data not found. Run /extract first.")
    
    try:
        with open("extracted_data.json", "r") as f:
            data = json.load(f)
        
        report_md = generate_report(data)
        
        with open("DDR_Final_Report_v3.md", "w") as f:
            f.write(report_md)
            
        return {"message": "Report generation complete"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report")
def get_report():
    if not os.path.exists("DDR_Final_Report_v3.md"):
        raise HTTPException(status_code=404, detail="Report not found")
    with open("DDR_Final_Report_v3.md", "r") as f:
        content = f.read()
    return {"content": content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
