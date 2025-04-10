import PIL
import streamlit as st
import tensorflow as tf
import os
import sys

# Add the root directory to the path to import the download_model module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from download_model import download_file_from_google_drive, extract_file_id

st.set_page_config(
    page_title="Skin-Cancer",
    page_icon="♋",
    layout="centered",
    initial_sidebar_state="expanded",
)


def standardize_reduction_wrapper(fn):
    def wrapped(*args, **kwargs):
        if 'reduction' in kwargs and kwargs['reduction'] == 'auto':
            kwargs['reduction'] = 'sum_over_batch_size'
        return fn(*args, **kwargs)
    return wrapped

@st.cache_resource
def load_model():
    model_path = "./model/model.h5"
    
    # Check if model exists, if not download it
    if not os.path.exists(model_path):
        try:
            st.info("Model file not found. Downloading model...")
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Google Drive link for the model
            drive_link = "https://drive.google.com/file/d/1d_zmXyypxBe7h5rh07IXgjxgpwMRzeyu/view?usp=sharing"
            file_id = extract_file_id(drive_link)
            
            if not file_id:
                st.error("Invalid Google Drive link. Please check the URL.")
                st.stop()
            
            download_file_from_google_drive(file_id, model_path)
            
            # Verify the file was downloaded
            if not os.path.exists(model_path):
                st.error("Failed to download the model file.")
                st.stop()
            
            if os.path.getsize(model_path) < 1000:  # Check if file is too small (likely an error)
                os.remove(model_path)
                st.error("Downloaded file appears to be invalid. Please try again.")
                st.stop()
                
            st.success("Model downloaded successfully!")
        except Exception as e:
            st.error(f"Error downloading model: {str(e)}")
            st.stop()
    
    try:
        # Load the model
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        # If model file is corrupted, delete it so it can be downloaded again
        if os.path.exists(model_path):
            os.remove(model_path)
        st.stop()


st.title("Skin-Cancer-Prediction")

pic = st.file_uploader(
    label="Upload a picture",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
    help="Upload a picture of your skin to get a diagnosis",
)

if st.button("Predict"):
    if not pic:
        st.error("Please upload an image")
    else:
        st.header("Results")

        cols = st.columns([1, 2])
        with cols[0]:
            st.image(pic, caption=pic.name, use_container_width=True)

        with cols[1]:
            labels = [
                "actinic keratosis",
                "basal cell carcinoma",
                "dermatofibroma",
                "melanoma",
                "nevus",
                "pigmented benign keratosis",
                "seborrheic keratosis",
                "squamous cell carcinoma",
                "vascular lesion",
            ]

            with st.spinner("Loading model..."):
                model = load_model()

            with st.spinner("Processing image..."):
                img = PIL.Image.open(pic)
                img = img.resize((180, 180))
                img = tf.keras.preprocessing.image.img_to_array(img)
                img = tf.expand_dims(img, axis=0)

                prediction = model.predict(img)
                prediction = tf.nn.softmax(prediction)

                score = tf.reduce_max(prediction)
                score = tf.round(score * 100, 2)

            with st.spinner("Predicting..."):
                prediction = tf.argmax(prediction, axis=1)
                prediction = prediction.numpy()
                prediction = prediction[0]

                disease = str(labels[prediction]).title()
                st.metric("Prediction", disease, delta_color="off")
                st.metric("Confidence", f"{score:.2f}%", delta_color="off")

        st.warning(
            "This is not a medical diagnosis. Please consult a doctor for a professional diagnosis.",
            icon="⚠️",
        )
