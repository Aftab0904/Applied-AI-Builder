import streamlit as st
import requests
import os
import json

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="DDR Report Generator", layout="wide")

st.title("Detailed Diagnostic Report (DDR) Generator")
st.markdown("Automate structural diagnostic reports from PDF inspections and thermal images.")

# Step 1: Upload
st.subheader("Step 1: Upload Diagnostic Files")
u_col1, u_col2 = st.columns(2)
inspection_file = u_col1.file_uploader("Upload Inspection Report (PDF)", type=["pdf"])
thermal_file = u_col2.file_uploader("Upload Thermal Images (PDF)", type=["pdf"])

if st.button("Upload Files", use_container_width=True):
    if inspection_file and thermal_file:
        files = {
            "inspection": (inspection_file.name, inspection_file, "application/pdf"),
            "thermal": (thermal_file.name, thermal_file, "application/pdf")
        }
        with st.spinner("Uploading files..."):
            res = requests.post(f"{BASE_URL}/upload", files=files)
            if res.status_code == 200:
                st.success("Files uploaded successfully!")
            else:
                st.error(f"Upload failed: {res.text}")
    else:
        st.warning("Please select both files before uploading.")

st.divider()

# Steps 2 & 3
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 2: Extract")
    if st.button("Run Extraction", use_container_width=True):
        with st.spinner("Extracting text and images from PDFs..."):
            res = requests.post(f"{BASE_URL}/extract")
            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error(f"Error: {res.text}")

with col2:
    st.subheader("Step 3: Generate")
    if st.button("Generate Report", use_container_width=True):
        with st.spinner("Generating expert report using AI..."):
            res = requests.post(f"{BASE_URL}/generate")
            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error(f"Error: {res.text}")

st.divider()

# Preview Section
tab1, tab2 = st.tabs(["📄 Report Preview", "🖼️ Extracted Images"])

with tab1:
    if st.button("Refresh Preview"):
        res = requests.get(f"{BASE_URL}/report")
        if res.status_code == 200:
            content = res.json()["content"]
            display_content = content.replace("assets/", f"{BASE_URL}/assets/")
            st.markdown(display_content, unsafe_allow_html=True)
        else:
            st.info("Report not generated yet.")
    elif os.path.exists("DDR_Final_Report_v3.md"):
        with open("DDR_Final_Report_v3.md", "r") as f:
            content = f.read()
        display_content = content.replace("assets/", f"{BASE_URL}/assets/")
        st.markdown(display_content, unsafe_allow_html=True)

with tab2:
    if os.path.exists("extracted_data.json"):
        with open("extracted_data.json", "r") as f:
            data = json.load(f)
        
        st.write("### Site Inspection Images")
        cols = st.columns(4)
        for i, (label, path) in enumerate(data["sample_image_mapping"].items()):
            cols[i % 4].image(f"{BASE_URL}/{path}", caption=label)
            
        st.divider()
        st.write("### Thermal Images")
        for image_id, t_data in data["thermal_data"].items():
            with st.expander(f"Thermal Set: {image_id}"):
                t_col1, t_col2 = st.columns(2)
                t_col1.image(f"{BASE_URL}/{t_data['thermal_img']}", caption="Thermal")
                t_col2.image(f"{BASE_URL}/{t_data['normal_img']}", caption="Normal")
                st.text(t_data["page_text"])
    else:
        st.info("No data extracted yet.")
