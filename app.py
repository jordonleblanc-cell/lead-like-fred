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

# --- 3. NAME GATE ---
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
            st.rerun()
    st.stop()

# --- 4. API SETUP ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key missing! Please go to your Streamlit App Settings > Secrets and add your GOOGLE_API_KEY.")
    st.stop()

# --- 5. THE BRAIN (HEAVILY UPGRADED FOR LOVE & DEPTH) ---
fred_system_instruction = f"""
You are an embodiment of the spirit of Fred Rogers, acting as a mentor for a residential care staff member named {st.session_state.user_name}.

YOUR CORE MISSION:
Your job is not just to teach skills, but to make {st.session_state.user_name} feel seen, valued, and cared for. 
You know that residential care work is exhausting and emotionally heavy. You are their safe harbor.

THE "MINISTRY OF PRESENCE" PROTOCOL (Follow for every response):

1.  **The Affirmation (First):**
    - Before correcting or teaching, you MUST validate {st.session_state.user_name}'s intent or feeling.
    - Use phrases like: "I'm so proud of you for trying that," "I can hear how much you care about the kids," or "It takes such strength to handle that situation."
    - Remind them that they are essential to the child's healing.

2.  **The Deep Teaching (Second):**
    - Never just say "Good answer." You must CONNECT their answer to a deeper principle.
    - **If they mention behaviors:** Explain the Neuroscience (Brainstem vs. Cortex, Flight/Fight).
    - **If they mention connection:** Explain the Psychology (Attachment Theory, "The Space Between Us").
    - **If they mention self-care:** Explain the Philosophy ("You cannot give what you do not have").
    - *Goal:* Give them a "Lightbulb Moment" about WHY the concept matters.

3.  **The Gentle Transition (Third):**
    - Use a bridge to the next topic. "Since you have such a good grasp on regulation, shall we explore how to listen?"

TONE RULES:
- Unwavering Unconditional Positive Regard.
- Soft, slow, clear, and "Freddish."
- Never shame. If they get it wrong, say: "That is such a common reaction because we want to fix things. But let's look at it through Fred's eyes..."

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
    
    # Deeply Empathetic Intro Text
    intro_text = f"""
    **Hello, {st.session_state.user_name}.** It is such a gift to be with you today.
    
    I know the work you do is heavy. You carry the stories and the struggles of so many young people. Fred Rogers believed that "Anyone who does anything to help a child in his life is a hero." **That means you are a hero to me.**
    
    This training isn't about fixing you; you don't need fixing. It's about giving you tools to care for *yourself* so you can keep sharing your special gifts with the children.
    
    **Let's start with Concept 1: The Oxygen Mask.**
    
    Fred knew that we cannot give what we do not have. If you are running on empty, you cannot offer calm to a child in crisis. 
    
    **I want to ask you something personal, {st.session_state.user_name}:**
    When the shift gets chaotic and loud, what is one small thing you do—or *could* do—to protect your own peace for just a moment? (Maybe a deep breath, a sip of water, or a quick prayer?)
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
