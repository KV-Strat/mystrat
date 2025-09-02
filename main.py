import streamlit as st
import uuid
from swot_generator import generate_strategy
from export import create_ppt

# App title
st.set_page_config(page_title="ASK Strategy", layout="wide")
st.subheader("Generate strategic recommendations instantly")

# -------- session state
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
