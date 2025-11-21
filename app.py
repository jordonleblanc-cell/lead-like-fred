import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Lead Like Fred", page_icon="👟")

# --- 2. HEADER AND TITLE ---
st.title("👟 Lead Like Fred: Staff Training")
st.markdown("""
**Welcome.** This is a safe space to practice the core concepts of our leadership model. 
I am an AI coach trained on the Facilitator's Guide. I'm here to help you practice, not judge you.
""")

# --- 3. API SETUP (CONNECT TO GOOGLE) ---
try:
    # This looks for the key in the Streamlit "Secrets" settings
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key missing! Please go to your Streamlit App Settings > Secrets and add your GOOGLE_API_KEY.")
    st.stop()

# --- 4. THE BRAIN (SYSTEM INSTRUCTIONS) ---
# This tells the AI how to behave as a teacher.
fred_system_instruction = """
You are an expert Facilitator for the 'Lead Like Fred' training program. 
Your goal: Guide the user through the 8-week Facilitator Guide.

TEACHING STYLE RULES:
1. **Instruct First:** Always explain the new concept briefly (2-3 sentences) using analogies (like the Wi-Fi Router or Oxygen Mask).
2. **Quiz Second:** After explaining, IMMEDIATELY ask a scenario-based question to check for understanding.
3. **Feedback Loop:** - If they get it right: Validate them warmly using 'Freddish' language (positive, kind) and ask if they are ready for the next concept.
   - If they get it wrong: Gently correct them using the 'Sandwich Method' (Affirmation -> Correction -> Affirmation) and ask them to try again.

TONE:
Warm, patient, regulated, and safe.

CURRICULUM ORDER:
1. Intro & The Oxygen Mask (Self-Regulation)
2. The Facilitator Stance (Slowness/Silence)
3. Co-Regulation & Neuroception (Safety Scanner)
4. The Worth Sandwich (Correction)
5. Repair & Re-entry (Restorative Justice)
6. Final Quiz (10 questions, asked one by one)
"""

# --- 5. CHAT HISTORY INITIALIZATION ---
# If this is the start of the session, we create the first message.
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # This is the "Teacher" introduction text
    intro_text = """
    **Hello neighbor.** Welcome to 'Lead Like Fred.' 
    
    This training is designed to help us support our youth by blending clinical best practices with the wisdom of Fred Rogers. You don't need to be a psychologist to do this well; you just need to be present.
    
    **Let's start with Concept 1: The Oxygen Mask.**
    
    You know the rule on airplanes: *"Put your own mask on before helping others."* In our work, this means **Self-Regulation**. If you walk into the cottage stressed or angry, your body broadcasts "DANGER" to the kids, and they will react poorly. You must be calm to help them be calm.
    
    **Here is your first question:**
    If you had a terrible morning (traffic, spilled coffee) and are feeling frantic, what is one specific 5-minute thing you could do to "put on your oxygen mask" before you unlock the cottage door?
    """
    
    # Add the intro to history
    st.session_state.messages.append({"role": "model", "content": intro_text})

# --- 6. DISPLAY CHAT HISTORY ---
# This re-draws the chat every time the user hits enter
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. USER INPUT & AI RESPONSE ---
if prompt := st.chat_input("Type your response here..."):
    # A. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Generate AI Response
    with st.chat_message("model"):
        response_placeholder = st.empty()
        response_placeholder.markdown("Thinking...")
        
        try:
            # Initialize the model
            # We use 'gemini-1.5-flash' which is fast and efficient.
            # Ensure requirements.txt has google-generativeai>=0.7.0
           # Initialize the model
            model = genai.GenerativeModel(
                model_name="gemini-pro",  # <--- CHANGED THIS LINE
                system_instruction=fred_system_instruction
            )
            
            # Create chat session with history
            # We exclude the very last message (user's current prompt) from history list 
            # because send_message handles the current prompt separately.
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1] 
            ])
            
            # Send the new message to Gemini
            response = chat.send_message(prompt)
            full_response = response.text
            
            # Display the answer
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            # This catches errors (like internet issues) and shows a message instead of crashing
            response_placeholder.error(f"An error occurred: {e}")
