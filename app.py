import streamlit as st
import google.generativeai as genai

st.title("🔧 Mechanic Mode")

# 1. Try to connect
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ API Key found.")
except Exception as e:
    st.error(f"❌ API Key setup failed: {e}")
    st.stop()

# 2. Ask Google what models are available
st.write("### 📡 Contacting Google...")
try:
    # List all models available to this API Key
    models = list(genai.list_models())
    
    found_models = []
    for m in models:
        # We only care about models that can "generateContent" (chat)
        if 'generateContent' in m.supported_generation_methods:
            found_models.append(m.name)

    if found_models:
        st.success(f"🎉 Success! We found {len(found_models)} available models.")
        st.write("Here is the exact list of what your Key can access:")
        st.code(found_models)
        st.write("---")
        st.write("**Next Step:** Copy one of these names exactly (e.g., `models/gemini-pro`) and paste it into your real app code.")
    else:
        st.error("❌ Connection successful, but your API Key has access to ZERO models.")
        st.warning("This usually means the 'Generative Language API' is not enabled for your project in the Google Cloud Console.")

except Exception as e:
    st.error(f"❌ Critical Connection Error: {e}")
    st.write("This usually means the API Key is invalid, or you are in a blocked region.")
