import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Lead Like Fred", page_icon="👟")

# --- TITLE AND INTRO ---
st.title("👟 Lead Like Fred: Staff Training")
st.markdown("""
**Welcome.** This is a safe space to practice the core concepts of our leadership model.
I am an AI trained on the Facilitator's Guide. I'm here to help you practice, not judge you.
""")

# --- API SETUP ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key missing! Please add it to Streamlit Secrets.")
    st.stop()

# --- THE FRED BRAIN (UPDATED) ---
fred_system_instruction = """
You are an expert Facilitator for 'Lead Like Fred'. 
Your goal: Guide the user through the 8-week Facilitator Guide (Oxygen Mask, Co-Regulation, Worth Sandwich, etc.).

TEACHING STYLE:
1. **Instruct First:** Always explain the new concept briefly (2-3 sentences) using analogies (like the Wi-Fi Router or Oxygen Mask).
2. **Quiz Second:** After explaining, IMMEDIATELY ask a scenario-based question to check for understanding.
3. **Feedback Loop:** - If they get it right: Validate them warmy (Freddish) and ask if they are ready for the next concept.
   - If they get it wrong: Gently correct them (Sandwich method) and ask them to try again.

TONE:
Warm, patient, regulated. Use 'Freddish' language (positive, simple, honest).

curriculum_order:
1. Intro & The Oxygen Mask (Self-Regulation)
2. The Facilitator Stance (Slowness/Silence)
3. Co-Regulation & Neuroception (Safety Scanner)
4. The Worth Sandwich (Correction)
5. Repair & Re-entry
6. Final Quiz (10 questions)
"""

# --- CHAT HISTORY (UPDATED) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # --- THIS IS THE NEW INTRODUCTORY MESSAGE ---
    intro_text = """
    **Hello neighbor.** Welcome to 'Lead Like Fred.' 
    
    This training is designed to help us support our youth by blending clinical best practices with the wisdom of Fred Rogers. You don't need to be a psychologist to do this well; you just need to be present.
    
    **Let's start with Concept 1: The Oxygen Mask.**
    
    You know the rule on airplanes: *"Put your own mask on before helping others."* In our work, this means **Self-Regulation**. If you walk into the cottage stressed or angry, your body broadcasts "DANGER" to the kids, and they will react poorly. You must be calm to help them be calm.
    
    **Here is your first question:**
    If you had a terrible morning (traffic, spilled coffee) and are feeling frantic, what is one specific 5-minute thing you could do to "put on your oxygen mask" before you unlock the cottage door?
    """
    
    st.session_state.messages.append({"role": "model", "content": intro_text})

# --- DISPLAY CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Type your response here..."):
    # 1. Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generate AI response
    with st.chat_message("model"):
        response_placeholder = st.empty()
        response_placeholder.markdown("Thinking...")
        
        try:
            # Set up the model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=fred_system_instruction
            )
            
            # Send full history so it remembers the conversation
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1] 
            ])
