import streamlit as st

st.set_page_config(
    page_title="Jim’s Objection Coach",
    layout="centered"
)

st.title("🚗 Jim’s Franchise Objection Coach")
st.caption("Instant answers for franchise sales objections")

plays = {
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
    }
}

choice = st.selectbox("Select the objection:", list(plays.keys()))

st.subheader("📞 Phone Response")
st.write(plays[choice]["phone"])

st.subheader("💬 SMS Version")
st.code(plays[choice]["sms"])

st.subheader("❓ Follow-Up Question")
st.write(plays[choice]["follow"])

st.subheader("➡️ Next Step")
st.write(plays[choice]["next"])
