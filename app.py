import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Jim’s Objection Coach", layout="centered")
st.title("🚗 Jim’s Franchise Objection Coach")
st.caption("Locked scripts first • AI fallback for new/odd objections")

# --- Locked plays (your proven responses) ---
PLAYS = {
    "Income / Money": {
        "phone": "Totally fair. Income here is effort-based, but the model is simple: consistent jobs, quality work, upsells and repeat customers. Early success comes from consistency, not perfection.",
        "sms": "Fair question. Income is effort-based but the model is proven — consistency early is key.",
        "follow": "Is it weekly stability, earning ceiling, or the first few months that worries you most?",
        "next": "Walk through a realistic first-30-day plan and book territory review."
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

# --- AI settings ---
ai_enabled = st.toggle("Enable AI fallback for new objections", value=True)
model_name = st.text_input("AI model", value="gpt-5.2")

# Streamlit secrets: OPENAI_API_KEY
api_key = st.secrets.get("OPENAI_API_KEY", None)

# --- UI ---
choice = st.selectbox("Select a known objection (locked script):", list(PLAYS.keys()))
st.divider()

st.subheader("📞 Phone Response (Locked)")
st.write(PLAYS[choice]["phone"])

st.subheader("💬 SMS Version (Locked)")
st.code(PLAYS[choice]["sms"])

st.subheader("❓ Follow-Up Question (Locked)")
st.write(PLAYS[choice]["follow"])

st.subheader("➡️ Next Step (Locked)")
st.write(PLAYS[choice]["next"])

st.divider()
st.subheader("🤖 AI Fallback (for anything else)")

objection_text = st.text_area(
    "Paste/type the prospect’s exact objection here (or any weird/unique objection):",
    placeholder="e.g. 'I’m worried I won’t get enough bookings in my area…'"
)

tone = st.selectbox("Tone", ["Straight-talking (AU)", "More supportive", "More assertive"])
format_pref = st.selectbox("Output format", ["Phone + SMS + Follow-up + Next step", "Just SMS", "Just Phone talk track"])

def generate_ai_response(objection: str) -> str:
    # OpenAI Responses API (recommended for new projects) :contentReference[oaicite:2]{index=2}
    client = OpenAI(api_key=api_key)
    system_rules = (
        "You are a franchise sales objection coach for Jim’s Car Detailing (Australia). "
        "Write concise, ethical replies. No income guarantees. Keep it confident and practical."
    )

    instructions = f"""
TONE: {tone}

Given this objection from a franchise prospect:
\"\"\"{objection}\"\"\"

Return:
- PHONE TALK TRACK (2–4 sentences)
- SMS VERSION (1–2 sentences)
- FOLLOW-UP QUESTION (1 sentence)
- NEXT STEP (1 line)

Constraints:
- No hype or guarantees
- Mention effort-based outcomes where relevant
- Keep it simple and human
"""

    resp = client.responses.create(
        model=model_name,
        input=[
            {"role": "system", "content": system_rules},
            {"role": "user", "content": instructions},
        ],
    )
    return resp.output_text

if st.button("Generate AI response", type="primary"):
    if not ai_enabled:
        st.warning("AI fallback is turned OFF. Toggle it on above if you want AI replies.")
    elif not objection_text.strip():
        st.warning("Type/paste an objection first.")
    elif not api_key:
        st.error("No OPENAI_API_KEY found in Streamlit Secrets. Add it in Settings → Secrets.")
    else:
        with st.spinner("Generating…"):
            try:
                ai_out = generate_ai_response(objection_text.strip())
                st.subheader("✅ AI Response")
                if format_pref == "Just SMS":
                    st.code(ai_out)
                elif format_pref == "Just Phone talk track":
                    st.write(ai_out)
                else:
                    st.write(ai_out)
            except Exception as e:
                st.error(f"AI request failed: {e}")
