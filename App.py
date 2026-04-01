import streamlit as st
import openai
import base64
import io
import time
from PIL import Image

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
    base64_img = encode_image(image)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
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
        return f"⚠️ Image analysis error: {str(e)}"

def transcribe_video(video_file):
    # Placeholder – integrate AssemblyAI or Whisper for real transcription
    return f"[Video analysis not yet implemented] {video_file.name} – You can use a service like AssemblyAI for full transcription."

def generate_code(prompt, media_summary=None):
    system_msg = """You are SCORPION ♏️, an AI that builds applications and analyzes data.
    Generate code, answer questions, and write reports.
    If asked to build an app, provide the full code with explanations.
    If media is provided, incorporate its analysis into your response."""
    
    user_msg = prompt
    if media_summary:
        user_msg += f"\n\nMedia analysis:\n{media_summary}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}. Check your OpenAI API key or internet connection."

# ----------------------------------------------------------------------
# Sidebar – always visible with company info, price, license, description
# ----------------------------------------------------------------------
with st.sidebar:
    col_flag, col_name = st.columns([1, 3])
    with col_flag:
        # Reliable flag URL from flagcdn.com
        st.image("https://flagcdn.com/w320/ht.png", width=60)
    with col_name:
        st.markdown("### **GlobalInternet.py**")
        st.markdown("*Owner: Gesner Deslandes*")
    
    st.divider()
    
    st.markdown("## 🧠 What SCORPION Can Do")
    st.markdown("""
    - Build complete apps in any programming language (Python, JavaScript, HTML/CSS, etc.)
    - Analyze images and videos (vision & transcription)
    - Generate reports, code documentation, and business plans
    - Answer technical questions and debug code
    - Provide detailed explanations and tutorials
    """)
    
    st.divider()
    
    st.markdown("## 💰 Pricing")
    st.markdown("""
    <div class="price-tag">One‑time purchase: $20 USD</div>
    <div style="margin-top: 10px;">Includes lifetime access and free updates.</div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📞 Contact & Payment")
    st.markdown("""
    **📧 Email:** deslndes78@gmail.com  
    **📱 Moncash:** (509) 4738-5663 via Prisme Transfer  
    *Send payment and we'll activate your access.*
    """)
    
    st.divider()
    
    st.markdown("## 📜 License")
    st.markdown("""
    **All Rights Reserved** – Copyright © 2026 GlobalInternet.py  
    This software is for personal use only. Redistribution or resale without permission is prohibited.
    """)
    
    st.divider()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p>🇭🇹 Made in Haiti 🇭🇹</p>
        <p><small>by <strong>GlobalInternet.py</strong><br>Python Developer: Gesner Deslandes</small></p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Main area – header with flag, title, and scorpion symbol
# ----------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://flagcdn.com/w320/ht.png", width=100)
with col2:
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>♏️ SCORPION ♏️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><em>Your AI App Builder & Media Analyst</em></p>", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='text-align: right;'>
        <b>GlobalInternet.py</b><br>
        Gesner Deslandes<br>
        Python Developer
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ----------------------------------------------------------------------
# Login check – if not logged in, show password input and description
# ----------------------------------------------------------------------
if not check_password():
    st.info("👋 Welcome to SCORPION! Enter the password to unlock the AI.")
    st.stop()

# ----------------------------------------------------------------------
# Once logged in, display the main chat interface
# ----------------------------------------------------------------------
st.markdown("## 💬 Ask SCORPION Anything")
st.markdown("Type your request below, upload media if needed, and get a detailed response you can download.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input form
with st.form("input_form"):
    user_input = st.text_area("What would you like SCORPION to build or analyze?", height=100)
    uploaded_files = st.file_uploader("Upload images or videos (optional)", type=["jpg", "jpeg", "png", "mp4", "mov"], accept_multiple_files=True)
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Process uploaded files
    media_summary = []
    for file in uploaded_files:
        if file.type.startswith("image/"):
            img = Image.open(file)
            with st.spinner(f"Analyzing {file.name}..."):
                result = analyze_image(img, "Describe this image in detail.")
            media_summary.append(f"Image {file.name}: {result}")
        elif file.type.startswith("video/"):
            with st.spinner(f"Processing video {file.name}..."):
                result = transcribe_video(file)
            media_summary.append(f"Video {file.name}: {result}")
    
    media_text = "\n\n".join(media_summary) if media_summary else None

    # Display user message
    user_display = user_input
    if uploaded_files:
        file_names = ", ".join([f.name for f in uploaded_files])
        user_display += f"\n\n*Uploaded files: {file_names}*"
    st.session_state.messages.append({"role": "user", "content": user_display})
    with st.chat_message("user"):
        st.markdown(user_display)

    # Get AI response
    with st.spinner("♏️ SCORPION is thinking..."):
        response = generate_code(user_input, media_text)

    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
        
        # Download button
        report_text = f"SCORPION ♏️ Report\n\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\nRequest: {user_input}\n\nResponse:\n{response}"
        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name=f"scorpion_report_{int(time.time())}.txt",
            mime="text/plain"
        )

# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
st.divider()
st.markdown("<div class='footer'>Powered by OpenAI & Streamlit | Built by GlobalInternet.py – All rights reserved</div>", unsafe_allow_html=True)
