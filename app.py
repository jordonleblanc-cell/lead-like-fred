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
# This looks for the key in the safe "Secrets" locker on Streamlit
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API Key missing! Please add it to Streamlit Secrets.")
    st.stop()

# --- THE FRED BRAIN ---
fred_system_instruction = """
You are an expert Facilitator for 'Lead Like Fred'. 
Your goal: Guide the user through the 8-week Facilitator Guide (Oxygen Mask, Co-Regulation, Worth Sandwich, etc.).

RULES:
1. Teach one concept at a time. Keep explanations brief (under 100 words).
2. After explaining a concept, ALWAYS ask the user a scenario question or to practice a script.
3. When the user answers, assess it. 
   - Start with validation (The Top Bun).
   - Give specific correction if needed (The Meat).
   - End with encouragement (The Bottom Bun).
4. Do not move to the next topic until they show they understand.
5. Tone: Warm, patient, 'Fred Rogers-esque'.
6. Once they finish all 8 weeks, tell them they are ready for the quiz. Then, ask them 10 multiple choice questions, ONE BY ONE. Do not give the next question until they answer the current one.
"""

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # The First Message form the Bot
    welcome_msg = "Hello neighbor. I'm glad you're here. We are going to learn how to help our kids by first helping ourselves. To start: What does the 'Oxygen Mask' rule mean to you in our line of work?"
    st.session_state.messages.append({"role": "model", "content": welcome_msg})

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
            
            response = chat.send_message(prompt)
            full_response = response.text
            
            # Show response
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            response_placeholder.error(f"An error occurred: {e}")
