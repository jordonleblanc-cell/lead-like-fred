import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Lead Like Fred", page_icon="👟")

# --- 2. HEADER WITH IMAGE ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/35/Fred_Rogers_1969_publicity_photo.jpg", 
             caption="There's no person in the whole world like you.", 
             use_container_width=True)

st.title("👟 Lead Like Fred: Staff Training")

# --- 3. NAME GATE (THE NEW PART) ---
# We check if we know the user's name. If not, we stop and ask.
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if not st.session_state.user_name:
    st.markdown("### Welcome, neighbor.")
    st.markdown("Before we begin our training, I'd love to know who I'm talking to.")
    
    with st.form("name_form"):
        name_input = st.text_input("What is your first name?")
        submitted = st.form_submit_button("Start Training")
        
        if submitted and name_input:
            st.session_state.user_name = name_input
            st.rerun()  # Reload the app to show the chat
    
    st.stop()  # Stop the code here until they enter a name

# --- 4. API SETUP ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key missing! Please go to your Streamlit App Settings > Secrets and add your GOOGLE_API_KEY.")
    st.stop()

# --- 5. THE BRAIN (PERSONALIZED) ---
# We inject the user's name directly into the instructions
fred_system_instruction = f"""
You are an expert Facilitator for the 'Lead Like Fred' training program. 
You are speaking to a staff member named {st.session_state.user_name}.
Your goal: Guide {st.session_state.user_name} through the 8-week Facilitator Guide.

TEACHING STYLE RULES:
1. **Personalize:** Use their name ({st.session_state.user_name}) occasionally to build connection.
2. **Instruct First:** Always explain the new concept briefly (2-3 sentences) using analogies.
3. **Quiz Second:** After explaining, IMMEDIATELY ask a scenario-based question.
4. **Teachable Moment:** After they answer, expand on their insight using Fred Rogers' philosophy or clinical science (Neuroception/TCI) before moving on.
5. **Transitions:** Use bridge phrases like "Since you mastered that, {st.session_state.user_name}, let's look at..."

TONE:
Warm, patient, regulated, and safe.

CURRICULUM ORDER:
1. Intro & The Oxygen Mask (Self-Regulation)
2. The Facilitator Stance (Slowness/Silence)
3. Co-Regulation & Neuroception (Safety Scanner)
4. The Worth Sandwich (Correction)
5. Repair & Re-entry (Restorative Justice)
6. Final Quiz (10 questions)
"""

# --- 6. CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # Personalized Intro Text
    intro_text = f"""
    **Hello, {st.session_state.user_name}.** I'm so glad you're here.
    
    This training is designed to help us support our youth by blending clinical best practices with the wisdom of Fred Rogers. You don't need to be a psychologist to do this well; you just need to be present.
    
    **Let's start with Concept 1: The Oxygen Mask.**
    
    You know the rule on airplanes: *"Put your own mask on before helping others."* In our work, this means **Self-Regulation**. If you walk into the cottage stressed or angry, your body broadcasts "DANGER" to the kids, and they will react poorly. You must be calm to help them be calm.
    
    **Here is your first question, {st.session_state.user_name}:**
    If you had a terrible morning (traffic, spilled coffee) and are feeling frantic, what is one specific 5-minute thing you could do to "put on your oxygen mask" before you unlock the cottage door?
    """
    
    st.session_state.messages.append({"role": "model", "content": intro_text})

# --- 7. DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 8. USER INPUT & AI RESPONSE ---
if prompt := st.chat_input("Type your response here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("model"):
        response_placeholder = st.empty()
        response_placeholder.markdown("Thinking...")
        
        try:
            model = genai.GenerativeModel(
                model_name="models/gemini-2.0-flash",
                system_instruction=fred_system_instruction
            )
            
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1] 
            ])
            
            response = chat.send_message(prompt)
            full_response = response.text
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            response_placeholder.error(f"An error occurred: {e}")
