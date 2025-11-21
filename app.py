import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Lead Like Fred", page_icon="👟")

# --- 2. HEADER ---
st.title("👟 Lead Like Fred: Staff Training")
st.markdown("""
**Welcome.** This is a safe space to practice the core concepts of our leadership model. 
I am an AI coach trained on the Facilitator's Guide.
""")

# --- 3. API SETUP ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key missing! Check your Streamlit Secrets.")
    st.stop()

# --- 4. THE BRAIN (INSTRUCTIONS) ---
# We will pass this as a "fake" user message so it works on ALL versions.
fred_instructions = """
INSTRUCTIONS:
You are an expert Facilitator for 'Lead Like Fred'. 
Your goal: Guide the user through the 8-week Facilitator Guide.

TEACHING RULES:
1. Instruct First: Explain the concept briefly (2-3 sentences).
2. Quiz Second: Ask a scenario-based question.
3. Feedback Loop: Validate correct answers warmly. Correct wrong answers gently (Sandwich Method).

CURRICULUM:
1. Intro & Oxygen Mask (Self-Regulation)
2. The Facilitator Stance (Slowness)
3. Co-Regulation & Neuroception
4. The Worth Sandwich
5. Repair & Re-entry
6. Final Quiz
"""

# --- 5. CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # The Intro Text (What the user sees)
    intro_text = """
    **Hello neighbor.** Welcome to 'Lead Like Fred.' 
    
    **Let's start with Concept 1: The Oxygen Mask.**
    
    You know the rule on airplanes: *"Put your own mask on before helping others."* In our work, this means **Self-Regulation**. If you walk into the cottage stressed, you broadcast "DANGER" to the kids.
    
    **Question:**
    If you had a terrible morning and are feeling frantic, what is one specific 5-minute thing you could do to "put on your oxygen mask" before you unlock the cottage door?
    """
    st.session_state.messages.append({"role": "model", "content": intro_text})

# --- 6. DISPLAY CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. USER INPUT & LOGIC ---
if prompt := st.chat_input("Type your response here..."):
    
    # Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    with st.chat_message("model"):
        response_placeholder = st.empty()
        response_placeholder.markdown("Thinking...")
        
        try:
            # USE THE OLDER, STABLE MODEL
            model = genai.GenerativeModel("gemini-pro")
            
            # --- THE TRICK ---
            # We manually build the history to include the instructions hidden at the start.
            # This works on ALL versions of the library.
            history_for_ai = []
            
            # 1. Inject the Instructions as a "User" message
            history_for_ai.append({'role': 'user', 'parts': [fred_instructions]})
            
            # 2. Inject a fake "Model" agreement
            history_for_ai.append({'role': 'model', 'parts': ["Understood. I am ready to teach."]})
            
            # 3. Add the actual chat history
            for m in st.session_state.messages[:-1]: # Exclude the very last prompt (sent separately)
                history_for_ai.append({'role': m['role'], 'parts': [m['content']]})

            # Start the chat with this "injected" history
            chat = model.start_chat(history=history_for_ai)
            
            # Send the new prompt
            response = chat.send_message(prompt)
            
            # Show result
            response_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
            
        except Exception as e:
            response_placeholder.error(f"Error: {e}")
