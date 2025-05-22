import os
import base64
import shutil
from typing import List
from datetime import datetime
from openai import OpenAI
import streamlit as st
import pandas as pd
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from utils.key import GITHUB_TOKEN
# Set up OpenAI client with GitHub-hosted GPT-4o model
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=GITHUB_TOKEN
)

# Streamlit page configuration
st.set_page_config(layout="wide")

# Load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("static/prescription.css")

# Data models
class MedicationItem(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str

class PrescriptionInformations(BaseModel):
    patient_name: str = Field(description="Patient's name")
    patient_age: int = Field(description="Patient's age")
    patient_gender: str = Field(description="Patient's gender")
    doctor_name: str = Field(description="Doctor's name")
    doctor_license: str = Field(description="Doctor's license number")
    prescription_date: datetime = Field(description="Date of the prescription")
    medications: List[MedicationItem] = []
    additional_notes: str = Field(description="Additional notes or instructions")

# OpenAI Vision call
def query_github_gpt4o(images_base64: list, prompt: str) -> str:
    image_payloads = [
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}
        for img in images_base64
    ]
    
    messages = [
        {
            "role": "system",
            "content": "You are an expert medical transcriptionist."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                *image_payloads
            ]
        }
    ]

    response = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-4o",
        temperature=0.5,
        max_tokens=4096,
        top_p=1
    )

    return response.choices[0].message.content

# Process image and extract prescription info
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

    output_text = query_github_gpt4o(images_base64, prompt)
    return parser.parse(output_text)

# Remove temp folders
def remove_temp_folder(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

# App main function
def main():
    st.title('Medical Prescription Parsing')

    uploaded_file = st.file_uploader("Upload a Prescription image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = uploaded_file.name.split('.')[0].replace(' ', '_')
        output_folder = os.path.join(".", f"Check_{filename}_{timestamp}")
        os.makedirs(output_folder, exist_ok=True)

        check_path = os.path.join(output_folder, uploaded_file.name)
        with open(check_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.expander("Prescription Image", expanded=False):
            st.image(uploaded_file, caption='Uploaded Prescription Image.', use_column_width=True)

        with st.spinner('Processing Prescription...'):  
            final_result = get_prescription_informations([check_path])

            # Format additional notes
            if 'additional_notes' in final_result:
                notes = final_result['additional_notes']
                notes_formatted = notes.replace("\n", "<br> ") if isinstance(notes, str) else "<br> ".join(notes)
                final_result['additional_notes'] = f"<ul><li>{notes_formatted}</li></ul>"

            # Display fields
            data = [(key, final_result[key]) for key in final_result if key != 'medications']
            df = pd.DataFrame(data, columns=["Field", "Value"])
            st.write(df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

            # Display medications
            if final_result.get("medications"):
                meds_df = pd.DataFrame(final_result["medications"])
                st.subheader("Medications")
                st.write(meds_df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

        remove_temp_folder(output_folder)

if __name__ == "__main__":
    main()
