import re
import base64
from datetime import datetime
from typing import List
from io import BytesIO
import pandas as pd
from PIL import Image
from rapidfuzz import fuzz
from langchain_core.pydantic_v1 import BaseModel

# Load local medicine names
df_meds = pd.read_csv("data/Medicine_Details_With_Price.csv")
medicine_names = [re.sub(r'[^A-Za-z0-9\s\-]', '', name).lower() for name in df_meds["Medicine Name"].dropna().unique()]

# ------------------ Data Models ------------------ #
class MedicationItem(BaseModel):
    name: str
    dosage: str = ""
    frequency: str = ""
    duration: str = ""

class PrescriptionInformations(BaseModel):
    patient_name: str = ""
    patient_age: int = 0
    patient_gender: str = ""
    doctor_name: str = ""
    doctor_license: str = ""
    prescription_date: datetime = datetime.today()
    medications: List[MedicationItem] = []
    additional_notes: str = ""

# ------------------ OCR Helper Functions ------------------ #
def extract_medicine_names(ocr_phrases):
    cleaned_names = []
    exclude_keywords = {'bid', 'tid', 'qd', 'od', 'hs', 'am', 'pm', 'tab', 'tablet'}

    for phrase in ocr_phrases:
        cleaned = re.sub(r'[^A-Za-z]', '', phrase)
        lower_cleaned = cleaned.lower()
        if len(cleaned) >= 5 and lower_cleaned not in exclude_keywords:
            cleaned_names.append(cleaned)
    return cleaned_names

def preprocess_text(text):
    text = re.sub(r'[^A-Za-z0-9\s\-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def best_match(ocr_word, choices):
    scores = [
        (
            choice,
            0.4 * fuzz.token_sort_ratio(ocr_word, choice) +
            0.3 * fuzz.partial_ratio(ocr_word, choice) +
            0.3 * fuzz.token_set_ratio(ocr_word, choice)
        )
        for choice in choices
    ]
    return max(scores, key=lambda x: x[1])

# ------------------ EasyOCR Parsing ------------------ #
def get_prescription_informations_from_bytes(file_bytes: bytes) -> PrescriptionInformations:
    import easyocr
    import numpy as np
    import cv2

    reader = easyocr.Reader(['en'])

    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    image = image.resize((1024, 1024))
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    temp_file_path = "/tmp/temp_prescription.jpg"
    cv2.imwrite(temp_file_path, image_bgr)

    result = reader.readtext(temp_file_path, detail=0)
    candidates = extract_medicine_names(result)

    threshold = 65
    matched_meds = []
    for phrase in candidates:
        match, score = best_match(preprocess_text(phrase), medicine_names)
        if score >= threshold:
            matched_meds.append(MedicationItem(name=match))

    return PrescriptionInformations(
        medications=matched_meds,
        additional_notes="Parsed using EasyOCR."
    )
