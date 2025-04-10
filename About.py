import requests
import streamlit as st
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


st.set_page_config(
    page_title="Skin Cancer",
    page_icon="♋",
    layout="wide",
    initial_sidebar_state="expanded",
)

lottie_health = load_lottieurl(
    "https://assets2.lottiefiles.com/packages/lf20_5njp3vgg.json"
)
lottie_welcome = load_lottieurl(
    "https://assets1.lottiefiles.com/packages/lf20_puciaact.json"
)
lottie_healthy = load_lottieurl(
    "https://assets10.lottiefiles.com/packages/lf20_x1gjdldd.json"
)

st.markdown("<h1 style='text-align: center;'>Welcome To Our Skin Cancer Detection Web-App</h1>", unsafe_allow_html=True)
st_lottie(lottie_welcome, height=400, key="welcome")
# st.header("Melanoma detection at your skin images.")


with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.write("##")
        st.write(
            """
            Skin cancer, particularly melanoma, poses significant health risks when not identified promptly. Early detection is crucial as melanoma alone contributes to a substantial portion of skin cancer-related fatalities. Our AI-powered solution assists medical professionals by analyzing skin images, potentially streamlining the diagnostic process and reducing manual screening efforts.

            The system is trained to identify various skin conditions including:
            * Actinic keratosis (solar keratosis)
            * Basal cell carcinoma (BCC)
            * Dermatofibroma (benign fibrous histiocytoma)
            * Malignant melanoma
            * Melanocytic nevus (mole)
            * Pigmented actinic keratosis
            * Seborrheic keratosis (senile wart)
            * Squamous cell carcinoma (SCC)
            * Vascular skin lesions
            """
        )
    with right_column:
        st_lottie(lottie_health, height=500, key="check")

with st.container():
    st.write("---")
    cols = st.columns(2)
    with cols[0]:
        st.header("How it works?")
        """
        Using Model we have trained, our system uses it and analyzes skin images to identify potential abnormalities.This is not a accurate result but will give you a slight idea.
        """
    with cols[1]:
        st_lottie(lottie_healthy, height=300, key="healthy")
