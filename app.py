import streamlit as st
from swot_generator import generate_strategy
from export import create_ppt

# App title
st.title("🧠 AI Strategy Copilot")
st.subheader("Generate SWOTs and strategic recommendations instantly")

# Input fields
company = st.text_input("Company name", "Amplitude")
competitors = st.text_input("Competitors (comma-separated)", "Mixpanel, Heap")
industry = st.text_input("Industry", "Product Analytics")

# Submit button
if st.button("Generate Strategy"):
    with st.spinner("Analyzing market..."):
        output = generate_strategy(company, competitors, industry)

        st.markdown("### 💡 Strategy Output")
        st.markdown(output)

        # Save PowerPoint
        filename = f"{company}_strategy_summary.pptx"
        create_ppt(output, filename)

        with open(filename, "rb") as f:
            st.download_button(
                label="📥 Download Strategy Deck (PPTX)",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
