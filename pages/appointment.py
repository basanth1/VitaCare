import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

st.title("Virtual Hospital - Doctor Appointment Booking with Video Call")

# Sample doctors
doctors = [
    {"name": "Dr. Alice Smith", "specialty": "Cardiologist"},
    {"name": "Dr. Bob Johnson", "specialty": "Dermatologist"},
    {"name": "Dr. Clara Lee", "specialty": "Gynecologist"},
    {"name": "Dr. David Kim", "specialty": "General Physician"},
]

# Select doctor
doctor_names = [doc["name"] for doc in doctors]
selected_doctor = st.selectbox("Select Doctor", doctor_names)

# Select date
min_date = datetime.today()
selected_date = st.date_input("Select Date", min_date, min_value=min_date)

# Select time
available_times = [f"{hour}:00" for hour in range(9, 18)]
selected_time = st.selectbox("Select Time", available_times)

# Patient info
patient_name = st.text_input("Your Full Name")
patient_contact = st.text_input("Contact Number or Email")

if st.button("Confirm Appointment and Start Video Call"):
    if not patient_name or not patient_contact:
        st.error("Please enter your name and contact info.")
    else:
        st.success(f"Appointment confirmed with {selected_doctor} on {selected_date} at {selected_time}.")

        # Create a unique room name - simple example combining doctor & patient & timestamp
        room_name = f"vh_{selected_doctor.replace(' ', '')}_{patient_name.replace(' ', '')}_{int(datetime.now().timestamp())}"

        st.write("Join the video call below:")

        # Embed Jitsi Meet iframe
        jitsi_url = f"https://meet.jit.si/{room_name}"

        components.iframe(jitsi_url, height=600, scrolling=True)

