import streamlit as st
import json
import os
import base64

# 1. SETUP PAGE
st.set_page_config(page_title="JOMAR Intelligence", layout="wide")

# 2. SIDEBAR LOGIC (Inventory)
with st.sidebar:
    st.header("?? JOMAR Lab")
    
    # Locate the brain file
    brain_path = "jomar_brain.json"
    if not os.path.exists(brain_path):
        brain_path = "data/jomar_brain.json"
    
    if os.path.exists(brain_path):
        try:
            with open(brain_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            names = [item['name'] for item in data]
            st.success(f"Brain Loaded: {len(names)} Formulas")
            
            selected = st.selectbox("Quick Load:", names)
            if st.button("Consult on this Formula"):
                st.session_state.messages.append({"role": "user", "content": f"Analyze the formula for {selected}"})
        except Exception as e:
            st.error(f"Brain Error: {e}")
    else:
        st.warning("?? Brain file missing. Please run Step 2 (Builder).")

# 3. MAIN CHAT INTERFACE
st.title("JOMAR PERFUME INTELLIGENCE")
st.caption("AI Master Perfumer | Vision & Data Enabled")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FILE UPLOADER (VISION) ---
uploaded_file = st.file_uploader("?? Upload Context (Photo, PDF, Excel)", type=["png", "jpg", "jpeg", "pdf", "xlsx"])

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. CHAT LOGIC
if prompt := st.chat_input("Ask JOMAR..."):
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get AI Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("Thinking...")
        
        try:
            from jomar_brain import run_jomar_expert
            
            # --- IMAGE ENCODING LOGIC ---
            image_data = None
            final_prompt = prompt
            
            if uploaded_file:
                # Check if it is an image
                if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                    # Convert image to Base64 code for the AI
                    image_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                    final_prompt = f"[IMAGE UPLOADED] {prompt}"
                else:
                    # Just filename for non-images
                    final_prompt = f"[FILE UPLOADED: {uploaded_file.name}] {prompt}"
            
            # Run the Brain
            response = run_jomar_expert(final_prompt, image_base64=image_data)
            
            placeholder.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            placeholder.error(f"System Error: {e}")