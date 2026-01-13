import streamlit as st
from openai import OpenAI

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Jim’s Objection Coach", layout="centered")
st.title("🚗 Jim’s Franchise Objection Coach")
st.caption("Locked scripts first • AI fallback for new/unique objections")

# ---------------------------
# Locked scripts (always available)
# ---------------------------
LOCKED = {
    "Income / Money": {
        "phone": "Totally fair. Income here is effort-based, but the model is simple: consistent jobs, quality work, upsells and repeat customers. Early success comes from consistency, not perfection.",
        "sms": "Fair question. Income is effort-based but the model is proven — consistency early is key.",
        "follow": "Is it weekly stability, earning ceiling, or the first few months that worries you most?",
        "next": "Walk through a realistic first-30-days plan and book territory review."
    },
    "No Experience": {
        "phone": "Most franchisees start with no experience. Training covers everything and confidence builds quickly once you’re on the tools.",
        "sms": "No experience needed — full training and support provided.",
        "follow": "Which part worries you most — skills, quoting, or day-to-day running?",
        "next": "Explain training schedule and first-week support."
    },
    "Not a Salesperson": {
        "phone": "You don’t need to be a salesperson. The Jim’s brand already has trust — your job is clear communication and quality service.",
        "sms": "You don’t need sales skills — brand trust does the heavy lifting.",
        "follow": "Is quoting price or closing the booking the uncomfortable part?",
        "next": "Teach simple quote + close script."
    },
    "Need More Time": {
        "phone": "Totally understand — it’s a big decision. Let’s work out what information would help you feel confident either way.",
        "sms": "Totally understand. What info would help you feel confident either way?",
        "follow": "If you had to decide in the next 7 days, what would you need?",
        "next": "Agree on decision timeline and next call."
    },
    "Risk / Fear": {
        "phone": "That fear is normal. The difference here is you’re not alone — you’re buying a proven system with training and ongoing support.",
        "sms": "Normal concern. Proven system + training reduces risk.",
        "follow": "What would failure look like to you personally?",
        "next": "Walk through first 90-day support structure."
    },
    "Cost": {
        "phone": "Fair question. Is it the upfront cost, early cashflow, or return that concerns you most?",
        "sms": "Is it upfront cost, early cashflow, or ROI that worries you?",
        "follow": "Which part is the biggest stress for you?",
        "next": "Break down cost vs realistic earning pathway."
    },
}

# ---------------------------
# Sidebar settings
# ---------------------------
with st.sidebar:
    st.header("Settings")
    ai_enabled = st.toggle("Enable AI fallback", value=True)
    model_name = st.text_input("Model", value="gpt-5.2")
    tone = st.selectbox("Tone", ["Straight-talking (AU)", "More supportive", "More assertive"])
    st.caption("Tip: Locked scripts always work. AI is optional.")

# ---------------------------
# Secrets / key handling
# ---------------------------
api_key = st.secrets.get("OPENAI_API_KEY", "").strip()

def get_client() -> OpenAI:
    # OpenAI recommends loading keys from env/secrets, not hard-coding. :contentReference[oaicite:2]{index=2}
    return OpenAI(api_key=api_key)

# ---------------------------
# Locked script UI
# ---------------------------
st.subheader("✅ Locked scripts")
choice = st.selectbox("Select a common objection:", list(LOCKED.keys()))

st.markdown("### 📞 Phone")
st.write(LOCKED[choice]["phone"])

st.markdown("### 💬 SMS")
st.code(LOCKED[choice]["sms"])

st.markdown("### ❓ Follow-up question")
st.write(LOCKED[choice]["follow"])

st.markdown("### ➡️ Next step")
st.write(LOCKED[choice]["next"])

st.divider()

# ---------------------------
# Key test (so we stop guessing)
# ---------------------------
st.subheader("🔑 Key test (recommended)")
st.caption("This checks whether your OpenAI key is valid from this Streamlit app.")

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("Test OpenAI key"):
        if not api_key:
            st.error("No OPENAI_API_KEY found in Streamlit Secrets.")
        else:
            try:
                client = get_client()
                # Calls the Models endpoint; if this 401s, it’s key/org/billing, not your app. :contentReference[oaicite:3]{index=3}
                client.models.list()
                st.success("✅ Key is valid and working")
            except Exception as e:
                st.error(f"❌ Key test failed: {e}")

with col2:
    # Safe, non-sensitive debug
    st.write("Key loaded:", bool(api_key))
    st.write("Key prefix:", api_key[:7] if api_key else "")
    st.write("Key length:", len(api_key))

st.divider()

# ---------------------------
# AI fallback UI
# ---------------------------
st.subheader("🤖 AI fallback (new/unique objections)")
objection_text = st.text_area(
    "Paste/type the prospect’s exact objection (anything weird/unusual):",
    placeholder="e.g. 'I’m worried I won’t get enough bookings in my area…'"
)

def ai_response(objection: str, tone_choice: str) -> str:
    system = (
        "You are a franchise sales objection coach for Jim’s Car Detailing (Australia). "
        "Be concise, confident, and ethical. Do not guarantee income. "
        "Where relevant, mention outcomes are effort-based."
    )
    prompt = f"""
TONE: {tone_choice}

Prospect objection:
\"\"\"{objection}\"\"\"

Return exactly these sections:
PHONE TALK TRACK (2–4 sentences)
SMS VERSION (1–2 sentences)
FOLLOW-UP QUESTION (1 sentence)
NEXT STEP (1 line)
"""
    client = get_client()
    # Responses API is recommended for new projects. :contentReference[oaicite:4]{index=4}
    resp = client.responses.create(
        model=model_name,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.output_text

if st.button("Generate AI response", type="primary"):
    if not ai_enabled:
        st.warning("AI fallback is turned OFF in Settings.")
    elif not objection_text.strip():
        st.warning("Paste/type an objection first.")
    elif not api_key:
        st.error("Missing OPENAI_API_KEY in Streamlit Secrets.")
    else:
        try:
            with st.spinner("Generating…"):
                out = ai_response(objection_text.strip(), tone)
            st.success("Done")
            st.write(out)
        except Exception as e:
            st.error(f"AI request failed: {e}")
            st.info(
                "If this is a 401 invalid_api_key, it’s almost always an OpenAI key/org/billing issue. "
                "Use the 'Test OpenAI key' button above to confirm."
            )
