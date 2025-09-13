"""
Streamlit Step‑1 wizard for Strategy Copilot — now wired to generate.py
- Adds on_generate_click() with robust error handling
- Uses OpenAIProvider automatically if OPENAI_API_KEY is set; otherwise offline fallback
- Produces a downloadable JSON export (PPT export can be added next)
"""

from __future__ import annotations
from export_ppt import build_ppt_from_state
import json
import uuid
from datetime import datetime
import os
import streamlit as st
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
if "OPENAI_PROJECT" in st.secrets:  # optional
    os.environ["OPENAI_PROJECT"] = st.secrets["OPENAI_PROJECT"]

try:
    # These come from the generate.py you added in canvas
    from generate import StrategyGenerator, OpenAIProvider
except Exception:  # graceful dev-mode without the module
    StrategyGenerator = None  # type: ignore
    OpenAIProvider = None  # type: ignore

APP_NAME = "ASK Strategy"

# -------------------- Page & Session Setup --------------------
st.set_page_config(page_title=APP_NAME, layout="wide")

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
        "results": {
            "SWOT": {"S": [], "W": [], "O": [], "T": []},
            "Ansoff": {
                "market_penetration": [],
                "market_development": [],
                "product_development": [],
                "diversification": [],
            },
        },
        "recs": [],
        "export": {"type": "ppt", "path": None},
    }

state = st.session_state.state

# -------------------- Helpers --------------------

def _get_generator() -> "StrategyGenerator":
    """Return a StrategyGenerator. Falls back to offline if OpenAI not configured."""
    if StrategyGenerator is None or state.get("offline_mode", False):
        st.info(
            "`generate.py` not found/importable. The app will still run with a minimal mock.",
            icon="ℹ️",
        )
        # Very small fallback shim
        class _MockGen:
            def generate_selected_frameworks(self, **kwargs):
                return {
                    "SWOT": {
                        "S": ["Clear value proposition", "Growing customer base"],
                        "W": ["Limited brand awareness"],
                        "O": ["Upsell existing accounts"],
                        "T": ["Price pressure from rivals"],
                    },
                    "Ansoff": {
                        "market_penetration": ["Bundle add‑ons"],
                        "market_development": ["Enter 1–2 adjacent regions"],
                        "product_development": ["Launch analytics‑lite"],
                        "diversification": ["Vertical solution pack"],
                    },
                }

            def generate_recommendations(self, results, **kwargs):
                return [
                    {"title": "OEM bundle program", "impact": 5, "effort": 3, "rationale": "Derived from analysis."},
                    {"title": "Managed calibration add‑on", "impact": 4, "effort": 3, "rationale": "Derived from analysis."},
                    {"title": "Managed calibration add‑on 12", "impact": 1, "effort": 2, "rationale": "Derived from analysis."}
                ]

        return _MockGen()  # type: ignore

    # Real generator path
    provider = None
    try:
        import os

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and OpenAIProvider is not None:
            provider = OpenAIProvider(model="gpt-4o-mini", api_key=api_key)
            st.caption("LLM mode: OpenAI (gpt-4o-mini)")
        else:
            st.caption("LLM mode: Offline fallback (no OPENAI_API_KEY detected)")
    except Exception as e:
        st.caption(f"LLM init issue → Offline fallback: {e}")

    return StrategyGenerator(provider)


def _list_to_text(items):
    return "\n".join(items or [])


def _text_to_list(txt):
    return [x.strip(" \t-•") for x in (txt or "").splitlines() if x.strip()]


# -------------------- Actions --------------------

def on_generate_click():
     # Choose provider based on toggle
    provider = None if state.get("offline_mode") else "openai"
    
    if not state["company"].strip() or not state["product"].strip():
        st.error("Company and Product are required before generation.")
        return
    if not state["frameworks"]:
        st.error("Select at least one framework.")
        return

    gen = _get_generator()
    try:
        with st.spinner("Generating analysis…"):
            results = gen.generate_selected_frameworks(
                company=state["company"],
                product=state["product"],
                frameworks=state["frameworks"],
                notes=state.get("notes"),
                geo=state.get("geo") or None,
                peers=["Rival A", "Rival B"],
            )
            state["results"].update(results)
            # Auto-generate recommendations
            state["recs"] = gen.generate_recommendations(state["results"])
        st.toast("Analysis generated.", icon="✅")
        st.session_state.step = 2
        st.rerun()
    except Exception as e:
        st.error(f"Generation failed: {e}")


# -------------------- UI --------------------
st.title(APP_NAME)
st.progress((st.session_state.step + 1) / 5, text=f"Step {st.session_state.step + 1} of 5")

# Step 0 — Inputs
if st.session_state.step == 0:
    st.subheader("Inputs")
    state["company"] = st.text_input("Company *", state["company"], max_chars=80, placeholder="e.g., ACME Robotics")
    state["product"] = st.text_input("Product/Line *", state["product"], max_chars=80, placeholder="e.g., Edge IoT Sensors")
    state["geo"] = st.selectbox("Geography (optional)", ["", "US", "EU", "APAC"], index=0)
    state["notes"] = st.text_area("Notes (optional)", value=state["notes"] or "", height=100)

    # Offline test toggle (no OpenAI calls)
    state["offline_mode"] = st.checkbox(
        "Run without OpenAI (offline mock)",
        value=state.get("offline_mode", True),
        help="Use a local mock generator so you can test without API keys/costs."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue", type="primary", use_container_width=True):
            if not state["company"].strip() or not state["product"].strip():
                st.error("Company and Product are required.")
            else:
                st.session_state.step = 1
                st.rerun()
    with col2:
        st.button("Cancel", use_container_width=True)

# Step 1 — Framework selection
elif st.session_state.step == 1:
    st.subheader("Select frameworks")
    available = ["SWOT", "Ansoff", "Benchmark", "Fit Matrix"]
    selected = st.multiselect("Choose 1–4", options=available, default=state.get("frameworks", ["SWOT", "Ansoff"]))
    state["frameworks"] = selected

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=lambda: st.session_state.update(step=0), use_container_width=True)
    with col2:
        st.button("Generate analysis", type="primary", on_click=on_generate_click, use_container_width=True)

# Step 2 — Analysis review
elif st.session_state.step == 2:
    st.subheader("Analysis")
    fws = state.get("frameworks", [])
    if not fws:
        st.warning("No frameworks selected. Go back and choose at least one.")
    else:
        tabs = st.tabs(fws)
        for idx, name in enumerate(fws):
            with tabs[idx]:
                if name == "SWOT":
                    cols = st.columns(4)
                    S = _list_to_text(state["results"].get("SWOT", {}).get("S", []))
                    W = _list_to_text(state["results"].get("SWOT", {}).get("W", []))
                    O = _list_to_text(state["results"].get("SWOT", {}).get("O", []))
                    T = _list_to_text(state["results"].get("SWOT", {}).get("T", []))
                    with cols[0]:
                        new_S = st.text_area("Strengths", value=S, height=140)
                    with cols[1]:
                        new_W = st.text_area("Weaknesses", value=W, height=140)
                    with cols[2]:
                        new_O = st.text_area("Opportunities", value=O, height=140)
                    with cols[3]:
                        new_T = st.text_area("Threats", value=T, height=140)
                    if st.button("Save SWOT edits", key="save_swot"):
                        state["results"]["SWOT"] = {
                            "S": _text_to_list(new_S),
                            "W": _text_to_list(new_W),
                            "O": _text_to_list(new_O),
                            "T": _text_to_list(new_T),
                        }
                        st.toast("SWOT saved.", icon="💾")

                elif name == "Ansoff":
                    cols = st.columns(4)
                    an = state["results"].get("Ansoff", {})
                    with cols[0]:
                        mp = st.text_area("Market Penetration", value=_list_to_text(an.get("market_penetration", [])), height=140)
                    with cols[1]:
                        md = st.text_area("Market Development", value=_list_to_text(an.get("market_development", [])), height=140)
                    with cols[2]:
                        pd = st.text_area("Product Development", value=_list_to_text(an.get("product_development", [])), height=140)
                    with cols[3]:
                        dv = st.text_area("Diversification", value=_list_to_text(an.get("diversification", [])), height=140)
                    if st.button("Save Ansoff edits", key="save_ansoff"):
                        state["results"]["Ansoff"] = {
                            "market_penetration": _text_to_list(mp),
                            "market_development": _text_to_list(md),
                            "product_development": _text_to_list(pd),
                            "diversification": _text_to_list(dv),
                        }
                        st.toast("Ansoff saved.", icon="💾")

                elif name == "Benchmark":
                    st.write("Benchmark (read‑only preview). Add editing in Step 2.")
                    st.dataframe(state["results"].get("Benchmark", {}).get("table", []), use_container_width=True)

                elif name == "Fit Matrix":
                    st.write("Fit Matrix (read‑only preview). Add editing in Step 2.")
                    st.json(state["results"].get("Fit", {}))

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=lambda: st.session_state.update(step=1), use_container_width=True)
    with col2:
        st.button("Add recommendations", type="primary", on_click=lambda: st.session_state.update(step=3), use_container_width=True)

# Step 3 — Recommendations
elif st.session_state.step == 3:
    st.subheader("Recommendations")

    # Add a quick adder
    with st.form("rec_form", clear_on_submit=True):
        title = st.text_input("Add recommendation")
        c1, c2 = st.columns(2)
        impact = c1.slider("Impact", 1, 5, 4)
        effort = c2.slider("Effort", 1, 5, 2)
        rationale = st.text_area("Rationale (optional)")
        submitted = st.form_submit_button("Add")
        if submitted and title.strip():
            state["recs"].append({"title": title.strip(), "impact": impact, "effort": effort, "rationale": rationale.strip()})
            st.toast("Recommendation added.", icon="➕")

    st.dataframe(state["recs"], use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=lambda: st.session_state.update(step=2), use_container_width=True)
    with col2:
        st.button("Export", type="primary", on_click=lambda: st.session_state.update(step=4), use_container_width=True)

# Step 4 — Export (JSON stub)
elif st.session_state.step == 4:
    st.subheader("Export")
    export_type = st.radio("Choose format", ["PowerPoint", "JSON"], index=1)

    if export_type == "PowerPoint":
        bio, fname = build_ppt_from_state(state)
        st.download_button(
            "Download PPTX",
            data=bio.getvalue(),
            file_name=fname,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
        )
    else:

        # Assemble export payload
        payload = {
            "analysis_id": state["analysis_id"],
            "company": state["company"],
            "product": state["product"],
            "geo": state["geo"],
            "notes": state["notes"],
            "frameworks": state["frameworks"],
            "results": state["results"],
            "recs": state["recs"],
            "exported_at": datetime.utcnow().isoformat() + "Z",
        }
        pretty = json.dumps(payload, indent=2, ensure_ascii=False)

        # Filename pattern
        safe_company = (state["company"] or "company").replace(" ", "_")
        safe_product = (state["product"] or "product").replace(" ", "_")
        fname = f"{safe_company}_{safe_product}_{datetime.now().strftime('%Y%m%d')}_strategy.json"

        st.download_button(
        "Download JSON",
        data=pretty.encode("utf-8"),
        file_name=fname,
        mime="application/json",
        use_container_width=True,
    )

    st.caption("PowerPoint export will add slides for: Title, Agenda, SWOT, Ansoff, Benchmark, Top‑5 Recs.")

    st.button("Back", on_click=lambda: st.session_state.update(step=3))
