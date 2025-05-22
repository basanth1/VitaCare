import os
import shutil
from datetime import datetime
import pandas as pd
import streamlit as st
from utils.prescription_parser import get_prescription_informations

st.set_page_config(layout="wide")

# Apply CSS
with open("static/prescription.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def remove_temp_folder(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

def main():
    st.title("🧾 Prescription Scanner")

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
            st.session_state.prescription_data = final_result  # Save globally

            # Format additional notes
            if 'additional_notes' in final_result:
                notes = final_result['additional_notes']
                notes_formatted = notes.replace("\n", "<br> ") if isinstance(notes, str) else "<br> ".join(notes)
                final_result['additional_notes'] = f"<ul><li>{notes_formatted}</li></ul>"

            # Replace empty fields with "Not clear (image)"
            data = []
            for key in final_result:
                if key != 'medications':
                    value = final_result[key]
                    if value in [None, "", [], {}]:
                        value = "Not clear (image)"
                    data.append((key, value))
            df = pd.DataFrame(data, columns=["Field", "Value"])
            st.write(df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

            # Display medications
            if final_result.get("medications"):
                meds = final_result["medications"]
                for med in meds:
                    for field in med:
                        if med[field] in [None, "", [], {}]:
                            med[field] = "Not clear (image)"
                meds_df = pd.DataFrame(meds)
                st.subheader("Medications")
                st.write(meds_df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

        remove_temp_folder(output_folder)

if __name__ == "__main__":
    main()
