# import streamlit as st

# def render_hero():
#     st.markdown("""
#     <div class='hero-section'>
#         <div class='hero-left'>
#             <img src='assets/logotrans-without-title.png' width='60' />
#             <h1>VitaCare <br> <span>hospital</span></h1>
#             <p>Your Health, Anywhere. Anytime.</p>
#             <a href="/Appointment" target="_self"><button class='primary-btn'>Book an appointment</button></a>
#             <a href="/Order_Medicines" target="_self"><button class='secondary-btn'>Order Medicines</button></a>
#         </div>
#         <div class='hero-right'>
#             <img src='assets/hospital.jpg' />
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# def render_about():
#     st.markdown("""
#     <section class='about-section'>
#         <img src='assets/logotrans-small.png' width='80'/>
#         <h2>Committed to You</h2>
#         <p>
#         Virtual Hospital is a healthcare app that allows users to seamlessly book appointments with doctors,
#         upload prescriptions, and order medicines online. Leveraging AI, we simplify understanding your treatment.
#         </p>
#         <a href="/Prescription_Upload" target="_self"><button class='primary-btn'>Learn More</button></a>
#     </section>
#     """, unsafe_allow_html=True)

# def render_services():
#     st.markdown("""
#     <section class='services'>
#         <h3>Our Services</h3>
#         <div class='service-cards'>
#             <div class='card'><i class="fa-solid fa-stethoscope"></i><p>Doctor’s Appointment</p></div>
#             <div class='card'><i class="fa-solid fa-prescription"></i><p>Prescription Analysis</p></div>
#             <div class='card'><i class="fa-solid fa-pills"></i><p>Pharmacy Service</p></div>
#         </div>
#     </section>
#     """, unsafe_allow_html=True)

# def render_doctors():
#     st.markdown("""
#     <section class='doctors'>
#         <h3>Meet our Doctors</h3>
#         <div class='doctor-cards'>
#             <div class='doc-card'><img src='assets/doc1.webp'><h4>Dr. Alice Smith</h4><p>Cardiologist</p></div>
#             <div class='doc-card'><img src='assets/doc2.jpg'><h4>Dr. David Kim</h4><p>General Physician</p></div>
#             <div class='doc-card'><img src='assets/doc3.webp'><h4>Dr. Clara Lee</h4><p>Gynecologist</p></div>
#         </div>
#     </section>
#     """, unsafe_allow_html=True)

# def render_contact():
#     st.markdown("""
#     <section class='contact'>
#         <div>
#             <img src='assets/logotrans-small.png' width='100'/>
#             <h2>VitaCare Hospital</h2>
#         </div>
#         <div class='contact-details'>
#             <p><strong>Mail:</strong> 123 Anywhere St.</p>
#             <p><strong>Email:</strong> hello@reallygreatsite.com</p>
#             <p><strong>Phone:</strong> 123-456-789</p>
#         </div>
#     </section>
#     """, unsafe_allow_html=True)
import streamlit as st

def render_hero():
    col1, col2, col3 = st.columns([1,1, 1])
    with col1:
        st.image("assets/logotrans-without-title.png", width=60)
        st.markdown("<h1 style='font-size: 3.5rem; color: #8032a8;'>VitaCare<br><span style='font-weight:300;'>hospital</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; color: black;'>Your Health, Anywhere. Anytime.</p>", unsafe_allow_html=True)
        st.link_button("Book an appointment", "/appointment")
        st.link_button("prescription uploads", "/prescription")
        st.link_button("Order Medicines", "/orders")
    with col2:
        st.markdown("###")  # Spacer (adjust as needed)
        st.markdown("###")  # Spacer (adjust as needed)
        st.markdown("###")  # Spacer (adjust as needed)
        st.image("assets/logotrans-small.png", width=200)

    with col3:
        st.image("assets/hospital-1.webp", use_container_width=True)

    


def render_about():
    st.markdown("---")
    st.image("assets/logotrans-small.png", width=80)
    st.markdown("<h2 style='color:#8032a8; text-align:center; width:100%'>Committed to You</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p style="max-width: 1200px; text-align:center;">
        Virtual Hospital is a healthcare app that allows users to seamlessly book appointments with doctors,
        upload prescriptions, and order medicines online. Leveraging AI, we simplify understanding your treatment.
        </p>
    """, unsafe_allow_html=True)
    st.link_button("Learn More", "/Prescription_Upload")

def render_services():
    st.markdown("---")
    st.markdown("<h3 style='color:#8032a8;'>Our Services</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🩺 Doctor’s Appointment", unsafe_allow_html=True)
        st.markdown("Easily book virtual consultations with licensed doctors.")
    with col2:
        st.markdown("### 📄 Prescription Analysis", unsafe_allow_html=True)
        st.markdown("Upload prescriptions and recognize medicines using AI.")
    with col3:
        st.markdown("### 💊 Pharmacy Service", unsafe_allow_html=True)
        st.markdown("Order prescribed medicines and get home delivery.")

def render_doctors():
    st.markdown("---")
    st.markdown("<h3 style='color:#8032a8;'>Meet our Doctors</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("assets/doc1.webp", use_container_width=True)
        st.markdown("**Dr. Alice Smith**  \nCardiologist", unsafe_allow_html=True)
        st.markdown("With over a decade of experience, Dr. Smith is the resident expert on heart health.")

    with col2:
        st.image("assets/doc2.jpg", use_container_width=True)
        st.markdown("**Dr. David Kim**  \nGeneral Physician", unsafe_allow_html=True)
        st.markdown("As the senior doctor in VitaCare, Dr. Kim specializes in general care for all ages.")

    with col3:
        st.image("assets/doc3.webp", use_container_width=True)
        st.markdown("**Dr. Clara Lee**  \nGynecologist", unsafe_allow_html=True)
        st.markdown("Dr. Lee has over 15 years of experience as a fertility expert and obstetrician.")

def render_contact():
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("assets/logotrans-small.png", width=100)
        st.markdown("<h2>VitaCare Hospital</h2>", unsafe_allow_html=True)
    with col2:
        st.markdown("### Get in Touch")
        st.markdown("**Mailing Address:** 123 Anywhere St. Any City, ST 12345")
        st.markdown("**Email Address:** hello@reallygreatsite.com")
        st.markdown("**Phone Number:** 123-456-789")
