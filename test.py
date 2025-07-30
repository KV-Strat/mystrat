import streamlit as st
from swot_generator import generate_strategy
from export import create_ppt

# App title
st.title("🧠 AI Strategy Sunil")
st.subheader("Generate strategic recommendations instantly")

# Input fields
company = st.text_input("Company name", "Salesforce")
product = st.text_input("Product", Sales Cloud)

# Submit button
if st.button("Generate Strategy"):
    with st.spinner("Analyzing industries..."):
       output = generate_strategy(company, product)
       #output= Test_text

       st.markdown("### 💡 Strategy Output")
       st.markdown(output)
       #output = test_text
       #testertext=test_text
       #print(testertext)

       # Save PowerPoint
       filename = f"{company}_{product}_strategy_summary.pptx"
       # filename = "test_strategy_summary1.pptx"
       #print("output:", output)
       create_ppt(output, filename)
       with open(filename, "rb") as f:
           st.download_button(
               label="📥 Download Strategy Deck (PPTX)",
               data=f,
               file_name=filename,
               mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
           )


