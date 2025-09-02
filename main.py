import streamlit as st
import uuid
from swot_generator import generate_strategy
from export import create_ppt

# App title
# app.py — single‑file wizard skeleton for Step 1
st.set_page_config(page_title="Strategy ASK", layout="wide")
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
st.title("Strategy ASK")
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
        st.button("Back", on_click=prev_step, use_container_width=True)
    with col2:
        st.button("Generate analysis", type="primary", on_click=next_step, use_container_width=True)

# -------- step 2: analysis review (placeholder editors)
elif st.session_state.step == 2:
       st.subheader("Analysis")
       tabs = st.tabs(state["frameworks"]) if state["frameworks"] else []
for i, name in enumerate(state["frameworks"]):
       with tabs[i]:
              if name == "SWOT":
                     S = st.tags(label="Strengths", value=state["results"]["SWOT"]["S"]) if hasattr(st, "tags") else st.text_area("Strengths (comma‑sep)")
                     # NOTE: replace with your preferred editable control(s)
              elif name == "Ansoff":
                     st.write("Ansoff 2×2 placeholder — populate cells after generation")
              else:
                     st.write(f"{name} placeholder")
col1, col2 = st.columns([1,1])
with col1:
       st.button("Back", on_click=prev_step, use_container_width=True)
with col2:
       st.button("Add recommendations", type="primary", on_click=next_step, use_container_width=True)

# -------- step 3: recommendations & what‑if
elif st.session_state.step == 3:
       st.subheader("Recommendations")
       st.caption("Prioritize by impact × effort")
       with st.form("recs_form"):
              title = st.text_input("Add recommendation")
              colA, colB = st.columns(2)
              impact = colA.slider("Impact", 1, 5, 4)
              effort = colB.slider("Effort", 1, 5, 2)
              rationale = st.text_area("Rationale (optional)")
              if st.form_submit_button("Add") and title.strip():
                     state["recs"].append({"title": title, "impact": impact, "effort": effort, "rationale": rationale})
       if state["recs"]:
              st.table(state["recs"])
       col1, col2 = st.columns([1,1])
       with col1:
              st.button("Back", on_click=prev_step, use_container_width=True)
       with col2:
              st.button("Export", type="primary", on_click=next_step, use_container_width=True)

# -------- step 4: export
elif st.session_state.step == 4:
       st.subheader("Export")
       export_type = st.radio("Choose format", ["PowerPoint", "PDF"], index=0)
       state["export"]["type"] = "ppt" if export_type == "PowerPoint" else "pdf"
       st.button("Build export", type="primary") # hook your generator here
       st.info("When built, show a download link below.")
       st.write("(Download link placeholder)")
