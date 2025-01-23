import streamlit as st
import numpy as np
from PIL import Image
from skimage import transform
import cv2
from tensorflow.keras.models import load_model
import os

# Page Configuration and Setup
st.set_page_config(
    page_title="Dental Caries Detection",
    page_icon=":tooth:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Enhanced UI
def set_custom_style():
    st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(to right, #f0f4f8, #e6eaf4);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #ffffff, #f0f2f6);
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }
    .stImage {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
    .prevention-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Prevention Guidance Function
def show_prevention_guidance(caries_detected):
    st.title(":shield: Dental Health Prevention Guide")
    
    if caries_detected:
        # Guidance for Caries Detected
        st.markdown("<div class='prevention-card'>", unsafe_allow_html=True)
        st.header(":warning: Caries Detected - Immediate Actions", anchor=False)
        st.markdown("""
        ### Urgent Dental Care Steps:
        1. **Schedule a Dental Appointment Immediately**
           - Consult a dentist within the next week
           - Discuss treatment options for caries
           - Potential treatments include:
             * Dental fillings
             * Root canal (if decay is advanced)
             * Dental crown
        
        2. **Oral Hygiene Intensive Care**
           - Brush teeth 2-3 times daily with fluoride toothpaste
           - Use soft-bristled toothbrush
           - Floss daily to remove food particles
           - Consider antiseptic mouthwash
        
        3. **Dietary Modifications**
           - Reduce sugar and acidic food intake
           - Avoid frequent snacking
           - Drink water after meals
           - Increase calcium-rich foods
        
        4. **Professional Recommendations**
           - Get professional dental cleaning
           - Apply fluoride treatments
           - Consider dental sealants
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # Guidance for No Caries Detected
        st.markdown("<div class='prevention-card'>", unsafe_allow_html=True)
        st.header(":white_check_mark: No Caries - Maintenance Plan", anchor=False)
        st.markdown("""
        ### Preventive Oral Health Strategies:
        1. **Consistent Oral Hygiene**
           - Brush teeth twice daily (morning and night)
           - Use fluoride toothpaste
           - Floss daily
           - Replace toothbrush every 3-4 months
        
        2. **Balanced Nutrition**
           - Consume calcium-rich foods
           - Limit sugary and acidic foods
           - Stay hydrated
           - Eat crunchy fruits and vegetables
        
        3. **Regular Dental Check-ups**
           - Biannual dental visits
           - Professional cleaning
           - Routine X-rays
           - Early detection screenings
        
        4. **Additional Preventive Measures**
           - Use fluoride mouthwash
           - Consider dental sealants
           - Use interdental brushes
           - Practice proper brushing technique
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Nutrition and Lifestyle Tips
    st.markdown("<div class='prevention-card'>", unsafe_allow_html=True)
    st.header(":green_apple: Nutrition and Lifestyle for Dental Health", anchor=False)
    st.markdown("""
    ### Dental-Friendly Lifestyle Choices:
    - Quit smoking and limit alcohol consumption
    - Manage stress (can impact oral health)
    - Stay hydrated
    - Get adequate sleep
    - Regular exercise promotes overall health
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Home Page and Other Existing Functions (unchanged from previous code)
def home_page():
    st.title(":tooth: Dental Caries Detection System")
    
    # Use os.path to make file path handling more flexible
    import os
    
    # Define the image path
    image_path = 'dentai.jpg'
    
    # Check if file exists before trying to display
    if os.path.exists(image_path):
        st.sidebar.image(
            image_path,
            caption='Dental Health Model',  # Corrected caption
            use_container_width=True
        )
    else:
        # Fallback if image is not found
        st.sidebar.warning("Image not found. Please check the file path.")

    st.sidebar.markdown("### About")
    st.sidebar.info("""
    **Developers:**
    - Veera lakshmi M 👨‍💻
    - Lakshmi R 👨‍💻
    - Logeshwari S 👨‍💻

    **College:** Sethu Institute of Technology 🎓

    This application is built using Streamlit ✨
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### About Our System
        
        Dental Caries Detection uses advanced machine learning to analyze dental panoramic X-rays and identify potential caries (tooth decay).
        
        #### Key Features:
        - AI-powered image analysis
        - High accuracy detection
        - Quick and non-invasive screening
        - Supports PNG and JPG formats
        
        ### Early Detection Matters
        Detecting dental caries early can prevent:
        - Extensive tooth damage
        - Costly dental procedures
        - Potential tooth loss
        """)
    
    with col2:
        # Use your local image path
        local_image_path = r"pixelcut-export.png"
        
        if os.path.exists(local_image_path):
            st.image(local_image_path, 
                     caption="Dental Panoramic X-Ray", 
                     use_column_width=True)
        else:
            st.warning("Image not found. Please check the file path.")

def detection_page():
    st.title(":orange[Dental Caries Detection Portal]")
    
    # Load Pre-trained Model
    model_path = r'caries_model1.h5'
    
    try:
        model1 = load_model(model_path)
    except Exception as e:
        st.error(f"Model Loading Error: {e}")
        st.error("Please ensure the model file exists at the specified path.")
        return
    
    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload a dental panoramic X-ray image", 
        type=['png', 'jpg'], 
        help="Please upload a clear dental panoramic X-ray in PNG or JPG format"
    )
    
    if uploaded_file is not None:
        # Process Image
        image_file = Image.open(uploaded_file)
        img_array = np.array(image_file).astype('float32')/255
        img_res = transform.resize(img_array, (256, 256, 3))
        img_res = np.expand_dims(img_res, axis=0)
        
        # Display Uploaded Image
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image_file, caption='Uploaded Panoramic Dental X-Ray', use_column_width=True)
        
        with col2:
            # Prediction
            try:
                pred = model1.predict(img_res)
                confidence = pred[0][0] * 100
                caries_detected = round(pred[0][0]) == 0
                
                st.subheader("Detection Result:")
                if caries_detected:
                    st.warning("Caries Presence Detected :warning:")
                else:
                    st.success("No Caries Detected :white_check_mark:")
                
                st.metric("Confidence Level", f"{confidence:.2f}%")
                
                # Add Prevention Guidance Button
                if st.button("View Prevention Guidance"):
                    show_prevention_guidance(caries_detected)
                
            except Exception as e:
                st.error(f"Prediction Error: {e}")
    else:
        st.info("Please upload a dental X-ray image to get started.")

# Exit Page with Comprehensive Closing
def exit_page():
    st.title(":wave: Dental Health Journey Continues")
    st.markdown("""
    ### Thank You for Using Dental Caries Detection
    
    #### Your Oral Health Matters
    This application is a screening tool, not a substitute for professional dental care.
    
    ##### Next Steps:
    - Always consult with dental professionals
    - Maintain regular dental check-ups
    - Practice consistent oral hygiene
    - Stay informed about your dental health
    """)
    
    # Feedback and Support Section
    st.markdown("---")
    st.subheader(":phone: Need Support?")
    support_contact = st.checkbox("Show Support Contact Information")
    
    if support_contact:
        st.markdown("""
        ### Dental Health Support
        - **Emergency Dental Helpline**: 1-800-DENTAL-CARE
        - **Online Consultation**: www.dentalhealth.org
        - **Email Support**: support@dentalcare.com
        
        Remember, early detection and prevention are key to maintaining excellent oral health!
        """)
    
    # Exit Application
    if st.button("Close Application", key="final_exit"):
        st.balloons()  # Celebratory animation
        st.success("Thank you for prioritizing your dental health!")
        st.stop()

# Main Application
def main():
    set_custom_style()
    
    # Sidebar Navigation
    page = st.sidebar.radio(
        "Navigate", 
        ["Home", "Caries Detection", "Exit"], 
        index=0
    )
    
    if page == "Home":
        home_page()
    elif page == "Caries Detection":
        detection_page()
    else:
        exit_page()

if __name__ == "__main__":
    main()