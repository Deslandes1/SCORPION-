import streamlit as st
import openai
import base64
import io
from PIL import Image
import os
import time

# Page configuration
st.set_page_config(
    page_title="SCORPION ♏️ - AI App Builder",
    page_icon="♏️",
    layout="wide"
)

# ----------------------------------------------------------------------
# Authentication (simple password check using session state)
# ----------------------------------------------------------------------
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input
        st.text_input("🔐 Enter password to unlock SCORPION ♏️", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct
        st.text_input("🔐 Enter password to unlock SCORPION ♏️", type="password", on_change=password_entered, key="password")
        st.error("❌ Wrong password. Try again.")
        return False
    else:
        return True

# ----------------------------------------------------------------------
# Load OpenAI API key from secrets
# ----------------------------------------------------------------------
openai.api_key = st.secrets["openai_api_key"]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def encode_image(image):
    """Convert PIL Image to base64 string for OpenAI vision."""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image(image, prompt):
    """Send image + prompt to OpenAI Vision."""
    base64_img = encode_image(image)
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

def transcribe_video(video_file):
    """Simulate video transcription (in real app, use AssemblyAI or similar)."""
    # For demo, we just return a placeholder.
    return f"[Video transcription placeholder] {video_file.name} – content not transcribed automatically. You can use a service like AssemblyAI for full transcription."

def generate_code(prompt, media_summary=None):
    """Use OpenAI to generate code or answer the user."""
    system_msg = """You are SCORPION ♏️, an AI that builds applications and analyzes data. 
    You generate code, answer questions, and write reports. 
    Always respond in a clear, structured format.
    If asked to build an app, provide the full code with explanations.
    If media is provided, incorporate its analysis into your response."""
    
    user_msg = prompt
    if media_summary:
        user_msg += f"\n\nMedia analysis:\n{media_summary}"
    
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

# ----------------------------------------------------------------------
# Main app
# ----------------------------------------------------------------------
if not check_password():
    st.stop()  # Stop execution if not authenticated

# ---- Header with flag, symbol, company info ----
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    # Haitian flag (blue-red)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Flag_of_Haiti.svg/320px-Flag_of_Haiti.svg.png", width=100)
with col2:
    st.markdown("<h1 style='text-align: center;'>♏️ SCORPION ♏️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><em>Your AI app builder and analyst</em></p>", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style='text-align: right;'>
        <b>GlobalInternet.py</b><br>
        Owner: Gesner Deslandes<br>
        📧 deslndes78@gmail.com<br>
        📱 Moncash: (509) 4738-5663<br>
        <i>© 2026 – All rights reserved</i>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---- Sidebar with instructions ----
with st.sidebar:
    st.markdown("## 🧠 How to use")
    st.markdown("""
    1. **Type your request** in the chat box below.
    2. **Upload images/videos** (optional) – Scorpion will analyze them.
    3. Click **Send**.
    4. Download the response as a report.
    """)
    st.markdown("---")
    st.markdown("### 🚀 Examples")
    st.markdown("""
    - "Build a Python calculator app with a GUI."
    - "Analyze this image and tell me what you see."
    - "Create a web page for a restaurant (HTML/CSS)."
    - "Write a business plan for a tech startup."
    """)

# ---- Initialize session state for conversation ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Display previous messages ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Input area ----
with st.form("input_form"):
    user_input = st.text_area("💬 What would you like SCORPION to build or analyze?", height=100)
    uploaded_files = st.file_uploader("📎 Upload images or videos (optional)", type=["jpg", "jpeg", "png", "mp4", "mov"], accept_multiple_files=True)
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Process uploaded files
    media_summary = []
    for file in uploaded_files:
        if file.type.startswith("image/"):
            # Open image with PIL
            img = Image.open(file)
            # For demo, just describe it with a generic prompt
            # In a real app, you might ask for a detailed description
            with st.spinner(f"Analyzing {file.name}..."):
                result = analyze_image(img, "Describe this image in detail.")
            media_summary.append(f"Image {file.name}: {result}")
        elif file.type.startswith("video/"):
            # Video analysis placeholder (you can integrate a real service)
            with st.spinner(f"Processing video {file.name}..."):
                result = transcribe_video(file)
            media_summary.append(f"Video {file.name}: {result}")
    
    # Combine all media analysis into a single string
    media_text = "\n\n".join(media_summary) if media_summary else None

    # Show user message in chat
    user_display = user_input
    if uploaded_files:
        file_names = ", ".join([f.name for f in uploaded_files])
        user_display += f"\n\n*Uploaded files: {file_names}*"
    st.session_state.messages.append({"role": "user", "content": user_display})
    with st.chat_message("user"):
        st.markdown(user_display)

    # Get AI response
    with st.spinner("♏️ SCORPION is thinking..."):
        try:
            response = generate_code(user_input, media_text)
        except Exception as e:
            response = f"⚠️ Error: {str(e)}. Check your OpenAI API key or internet connection."

    # Append AI response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
        
        # Provide download button for the response
        report_text = f"SCORPION ♏️ Report\n\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\nRequest: {user_input}\n\nResponse:\n{response}"
        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name=f"scorpion_report_{int(time.time())}.txt",
            mime="text/plain"
        )

# ---- Footer ----
st.divider()
st.markdown("<p style='text-align: center;'>Powered by OpenAI & Streamlit | Built by GlobalInternet.py</p>", unsafe_allow_html=True)
