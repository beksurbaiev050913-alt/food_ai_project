"""
Web Application for Raw vs Cooked Food Recognition
Run this with: streamlit run app.py
"""

import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io
import os

# Configure page
st.set_page_config(
    page_title="Raw vs Cooked Food Classifier",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .raw-box {
        background-color: #E8F5E9;
        border: 2px solid #4CAF50;
    }
    .cooked-box {
        background-color: #FFF3E0;
        border: 2px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the trained model with caching"""
    try:
        model = keras.models.load_model('food_classifier_model.h5')
        return model
    except:
        return None

def preprocess_image(image):
    """Preprocess image for prediction"""
    img = image.convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(model, image):
    """Make prediction on image"""
    img_array = preprocess_image(image)
    prediction = model.predict(img_array, verbose=0)[0][0]
    
    if prediction > 0.5:
        label = 'Raw'
        confidence = prediction * 100
    else:
        label = 'Cooked'
        confidence = (1 - prediction) * 100
    
    return {
        'label': label,
        'confidence': confidence,
        'raw_score': prediction * 100,
        'cooked_score': (1 - prediction) * 100
    }

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ Raw vs Cooked Food Classifier</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload a food image to determine if it\'s raw or cooked</p>', unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    
    if model is None:
        st.error("⚠️ Model not found! Please train the model first using `train_model.py`")
        st.info("""
        **To train the model:**
        1. Organize your dataset in the required structure
        2. Run: `python train_model.py`
        3. Wait for training to complete
        4. Reload this app
        """)
        return
    
    st.success("✓ Model loaded successfully!")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("""
        This application uses a Convolutional Neural Network (CNN) 
        to classify food images as either **Raw** or **Cooked**.
        
        **How to use:**
        1. Upload a food image
        2. Wait for the prediction
        3. View the results with confidence scores
        """)
        
        st.header("Model Info")
        st.write("- Architecture: Custom CNN")
        st.write("- Input Size: 224x224")
        st.write("- Classes: Raw, Cooked")
        
        st.header("Tips")
        st.write("- Use clear, well-lit images")
        st.write("- Focus on the food item")
        st.write("- Avoid cluttered backgrounds")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a food image...", 
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of food"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_container_width=True)
            
            # Add predict button
            if st.button("🔍 Classify Food", type="primary", use_container_width=True):
                with st.spinner('Analyzing image...'):
                    result = predict_image(model, image)
                    st.session_state['result'] = result
    
    with col2:
        st.header("Prediction Results")
        
        if 'result' in st.session_state:
            result = st.session_state['result']
            
            # Display result with styling
            if result['label'] == 'Raw':
                st.markdown(f"""
                <div class="result-box raw-box">
                    <h2 style="color: #4CAF50; margin: 0;">🥗 RAW FOOD</h2>
                    <h3 style="color: #2E7D32; margin-top: 0.5rem;">Confidence: {result['confidence']:.2f}%</h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-box cooked-box">
                    <h2 style="color: #FF9800; margin: 0;">🍳 COOKED FOOD</h2>
                    <h3 style="color: #E65100; margin-top: 0.5rem;">Confidence: {result['confidence']:.2f}%</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed scores
            st.subheader("Detailed Scores")
            
            # Progress bars
            st.write("**Cooked Score:**")
            st.progress(result['cooked_score'] / 100)
            st.write(f"{result['cooked_score']:.2f}%")
            
            st.write("**Raw Score:**")
            st.progress(result['raw_score'] / 100)
            st.write(f"{result['raw_score']:.2f}%")
            
            # Confidence indicator
            st.subheader("Confidence Level")
            if result['confidence'] > 80:
                st.success("🟢 High Confidence")
            elif result['confidence'] > 60:
                st.warning("🟡 Medium Confidence")
            else:
                st.error("🔴 Low Confidence")
            
            # Additional info
            st.info(f"""
            **Interpretation:**
            The model is {result['confidence']:.2f}% confident that this food is **{result['label']}**.
            """)
        else:
            st.info("👆 Upload an image and click 'Classify Food' to see results")
    
    # Batch processing section
    st.markdown("---")
    st.header("📦 Batch Processing")
    
    uploaded_files = st.file_uploader(
        "Upload multiple images for batch processing",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        help="Select multiple food images to classify at once"
    )
    
    if uploaded_files:
        if st.button("🚀 Process All Images", type="primary"):
            results = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")
                image = Image.open(uploaded_file)
                result = predict_image(model, image)
                result['filename'] = uploaded_file.name
                result['image'] = image
                results.append(result)
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.text("✓ All images processed!")
            
            # Display results in grid
            st.subheader("Batch Results")
            
            cols = st.columns(3)
            for idx, result in enumerate(results):
                with cols[idx % 3]:
                    st.image(result['image'], use_column_width=True)
                    if result['label'] == 'Raw':
                        st.success(f"🥗 {result['label']} ({result['confidence']:.1f}%)")
                    else:
                        st.warning(f"🍳 {result['label']} ({result['confidence']:.1f}%)")
                    st.caption(result['filename'])
            
            # Summary statistics
            st.subheader("Summary")
            raw_count = sum(1 for r in results if r['label'] == 'Raw')
            cooked_count = len(results) - raw_count
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Images", len(results))
            col2.metric("Raw Foods", raw_count)
            col3.metric("Cooked Foods", cooked_count)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>Built with TensorFlow & Streamlit | Raw vs Cooked Food Recognition</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()