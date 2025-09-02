import streamlit as st
import uuid
from swot_generator import generate_strategy
from export import create_ppt

# App title

# -------- session state
if "step" not in st.session_state:
st.session_state.step = 0
if "state" not in st.session_state:
st.session_state.state = {
"analysis_id": str(uuid.uuid4()),
"company": "",
"product": "",
"geo": None,
"notes": None,
"frameworks": ["SWOT", "Ansoff"],
"results": {"SWOT": {"S":[],"W":[],"O":[],"T":[]},
"Ansoff": {"market_penetration":[],"market_development":[],"product_development":[],"diversification":[]}},
"recs": [],
"export": {"type": "ppt", "path": None}
}


state = st.session_state.state


# -------- helpers
def next_step():
st.session_state.step += 1


def prev_step():
st.session_state.step = max(0, st.session_state.step - 1)


st.title("Strategy Copilot")
st.progress((st.session_state.step+1)/5, text="Step %d of 5" % (st.session_state.step+1))


# -------- step 0: inputs
if st.session_state.step == 0:
st.subheader("Inputs")
state["company"] = st.text_input("Company *", state["company"], max_chars=80)
state["product"] = st.text_input("Product/Line *", state["product"], max_chars=80)
state["geo"] = st.selectbox("Geography (optional)", ["", "US", "EU", "APAC"], index=0)
state["notes"] = st.text_area("Notes (optional)", value=state["notes"] or "", height=100)


col1, col2 = st.columns([1,1])
with col1:
if st.button("Continue", type="primary", use_container_width=True):
if not state["company"].strip() or not state["product"].strip():
st.error("Company and Product are required.")
else:
next_step()
with col2:
st.button("Cancel", on_click=lambda: st.session_state.update(step=0))


# -------- step 1: framework selection
elif st.session_state.step == 1:
st.subheader("Select frameworks")
available = ["SWOT", "Ansoff", "Benchmark", "Fit Matrix"]
selected = st.multiselect("Choose 1–4", available, default=state["frameworks"])
if not selected:
st.warning("Select at least one framework.")
state["frameworks"] = selected or state["frameworks"]


col1, col2 = st.columns([1,1])
with col1:
st.write("(Download link placeholder)")


       #output = test_text
       #testertext=test_text
       #print(testertext)

       # Save PowerPoint
       #filename = f"{company}_{product}_strategy_summary.pptx"
       # filename = "test_strategy_summary1.pptx"
       #print("output:", output)
      # create_ppt(output, filename)
      # with open(filename, "rb") as f:
       #    st.download_button(
       #        label="📥 Download Strategy Deck (PPTX)",
       #        data=f,
        #       file_name=filename,
        #       mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        #   )
