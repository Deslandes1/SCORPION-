import streamlit as st
import openai
import base64
import io
import time
from PIL import Image
from openai import OpenAI

# ----------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="SCORPION ♏️ - AI App Builder",
    page_icon="♏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------
# Custom CSS – clean light background
# ----------------------------------------------------------------------
st.markdown("""
<style>
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    .stApp {
        background: #f5f5f5;
    }
    .flag-img {
        width: 80px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .scorpion-title {
        font-size: 3rem;
        font-weight: bold;
        color: #d62c1e;
        text-align: center;
        margin: 0;
    }
    .scorpion-sub {
        text-align: center;
        color: #333;
        margin-top: -0.5rem;
    }
    .info-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #d62c1e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .price-tag {
        background: #d62c1e;
        display: inline-block;
        padding: 6px 18px;
        border-radius: 40px;
        font-weight: bold;
        color: white;
        margin-top: 8px;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        font-size: 0.8rem;
        color: #666;
        border-top: 1px solid #ddd;
    }
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    .api-instruction {
        background: #fef7e0;
        border-left: 4px solid #d62c1e;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Helper functions (authentication, API calls)
# ----------------------------------------------------------------------
def check_password():
    """Returns True if password is correct."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔐 Enter password to unlock SCORPION ♏️", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔐 Enter password to unlock SCORPION ♏️", type="password", on_change=password_entered, key="password")
        st.error("❌ Wrong password. Try again.")
        return False
    else:
        return True

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image(image, prompt):
    """Analyze image using OpenAI Vision."""
    base64_img = encode_image(image)
    try:
        client = OpenAI(api_key=st.secrets["openai_api_key"])
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",  # or "gpt-4o" if available
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_img}"}
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        if "401" in str(e) or "invalid_api_key" in str(e):
            return "⚠️ **API Key Error** – Your OpenAI API key is missing or incorrect.\n\n" + get_api_instructions()
        return f"⚠️ Image analysis error: {str(e)}"

def transcribe_video(video_file):
    # Placeholder – integrate AssemblyAI or Whisper for real transcription
    return f"[Video analysis not yet implemented] {video_file.name} – You can use a service like AssemblyAI for full transcription."

def get_api_instructions():
    return """
    ### How to set up your OpenAI API key

    1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys) and create an API key (starts with `sk-`).
    2. In your Streamlit app, click the **"Manage app"** button (gear icon) in the top right.
    3. Go to **Settings → Secrets**.
    4. Add the following two lines:
