import fitz  # PyMuPDF
import os
import json
import re

def extract_from_sample_report(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    text_content = []
    image_mapping = {} # "Photo 1" -> "assets/photo_1.png"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        text_content.append(f"--- Page {page_num + 1} ---")
        text_content.append(text)
        
        # Find all "Photo X" in text
        photo_labels = re.findall(r"Photo\s+(\d+)", text)
        
        # Get all images on page
        images = page.get_images(full=True)
        # Filter for "real" images (ignore small icons/logos)
        real_images = []
        for img in images:
            xref = img[0]
            info = doc.extract_image(xref)
            if info["width"] > 100 and info["height"] > 100:
                real_images.append(xref)
        
        # Match labels to images if counts match or make sense
        # This is a heuristic: if we find 6 labels and >= 6 images, we match them
        if photo_labels and real_images:
            for i in range(min(len(photo_labels), len(real_images))):
                label = f"Photo {photo_labels[i]}"
                xref = real_images[i]
                info = doc.extract_image(xref)
                img_path = os.path.join(output_dir, f"photo_{photo_labels[i]}.{info['ext']}")
                with open(img_path, "wb") as f:
                    f.write(info["image"])
                image_mapping[label] = img_path

    return "\n".join(text_content), image_mapping

def extract_from_thermal_images(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    text_content = []
    thermal_data = {} # "RB02380X" -> {"thermal": "path", "normal": "path", "text": "..."}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        text_content.append(f"--- Thermal Page {page_num + 1} ---")
        text_content.append(text)
        
        # Find ID
        match = re.search(r"(RB[0-9]{5}X)", text)
        if match:
            image_id = match.group(1)
            images = page.get_images(full=True)
            real_images = []
            for img in images:
                xref = img[0]
                info = doc.extract_image(xref)
                if info["width"] > 100 and info["height"] > 100:
                    real_images.append(xref)
            
            # Usually the first image is thermal (top), second is normal (bottom)
            if len(real_images) >= 2:
                # Save Thermal
                info_t = doc.extract_image(real_images[0])
                t_path = os.path.join(output_dir, f"{image_id}_thermal.{info_t['ext']}")
                with open(t_path, "wb") as f: f.write(info_t["image"])
                
                # Save Normal
                info_n = doc.extract_image(real_images[1])
                n_path = os.path.join(output_dir, f"{image_id}_normal.{info_n['ext']}")
                with open(n_path, "wb") as f: f.write(info_n["image"])
                
                thermal_data[image_id] = {
                    "thermal_img": t_path,
                    "normal_img": n_path,
                    "page_text": text
                }

    return "\n".join(text_content), thermal_data

if __name__ == "__main__":
    sample_text, sample_mapping = extract_from_sample_report("Sample Report.pdf", "assets")
    thermal_text, thermal_data = extract_from_thermal_images("Thermal Images.pdf", "assets")
    
    with open("extracted_data.json", "w") as f:
        json.dump({
            "sample_report_text": sample_text,
            "sample_image_mapping": sample_mapping,
            "thermal_report_text": thermal_text,
            "thermal_data": thermal_data
        }, f, indent=4)
    print("Improved extraction complete.")
