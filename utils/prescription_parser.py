import os
import re
import base64
import shutil
from datetime import datetime
from typing import List
import pandas as pd
import easyocr
from rapidfuzz import fuzz
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from openai import OpenAI
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# OpenAI Client
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=GITHUB_TOKEN
)

# EasyOCR Reader
reader = easyocr.Reader(['en'])

# Load local medicine names
df_meds = pd.read_csv("data/Medicine_Details_With_Price.csv")
medicine_names = [re.sub(r'[^A-Za-z0-9\s\-]', '', name).lower()
                  for name in df_meds["Medicine Name"].dropna().unique()]

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

# ------------------ LangChain Function ------------------ #
def query_github_gpt4o(images_base64: list, prompt: str) -> str:
    image_payloads = [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}
        for img in images_base64
    ]

    messages = [
        {"role": "system", "content": "You are an expert medical transcriptionist."},
        {"role": "user", "content": [{"type": "text", "text": prompt}] + image_payloads}
    ]

    response = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-4o",
        temperature=0.5,
        max_tokens=4096,
        top_p=1
    )

    return response.choices[0].message.content

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
def parse_with_easyocr(image_path: str) -> dict:
    import cv2
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"[EasyOCR] File does not exist: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"[EasyOCR] Image at {image_path} could not be loaded. Is it a valid image?")

    result = reader.readtext(image_path, detail=0)
    candidates = extract_medicine_names(result)

    threshold = 65
    matched_meds = []
    for phrase in candidates:
        match, score = best_match(preprocess_text(phrase), medicine_names)
        if score >= threshold:
            matched_meds.append(MedicationItem(name=match))

    return PrescriptionInformations(
        medications=matched_meds,
        additional_notes="Parsed using fallback EasyOCR due to API failure."
    ).dict()

# ------------------ Main Wrapper ------------------ #
def get_prescription_informations(image_paths: List[str]) -> dict:
    parser = JsonOutputParser(pydantic_object=PrescriptionInformations)
    images_base64 = [base64.b64encode(open(img, "rb").read()).decode("utf-8") for img in image_paths]

    prompt = """
    Given the images, provide all available information including:
    - Patient's name, age, and gender
    - Doctor's name and license number
    - Prescription date
    - List of medications with name, dosage, frequency, and duration
    - Additional notes or instructions
    Note: If portions of the image are not clear then leave the values as empty. Do not make up the values.
    """ + parser.get_format_instructions()

    try:
        output_text = query_github_gpt4o(images_base64, prompt)
        return parser.parse(output_text)

    except Exception as e:
        print(f"[Fallback] GPT-4o failed. Switching to EasyOCR: {e}")
        print(f"[Debug] File exists: {os.path.exists(image_paths[0])}, Path: {image_paths[0]}")
        return parse_with_easyocr(image_paths[0])  # assumes 1 image

# Optional cleanup
def remove_temp_folder(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)