import streamlit as st
from swot_generator import generate_strategy
from export import create_ppt

Test_text = """
# Amplitude: Strategic Analysis

## Step 1: SWOT Analysis for Amplitude

### Strengths
- **Comprehensive Product Suite**: Amplitude offers a robust set of analytics tools that provide deep insights into user behavior, enabling businesses to make data-driven decisions.
- **Strong Brand Reputation**: Known for its innovation in product analytics, Amplitude has established a strong brand presence and trust in the industry.
- **Scalability**: Amplitude's platform is scalable, making it suitable for both small startups and large enterprises.

### Weaknesses
- **High Pricing**: Amplitude's comprehensive features come at a premium price, which may deter smaller companies or startups with limited budgets.
- **Complexity**: The depth of the platform can be overwhelming for new users or those without a technical background, potentially increasing the learning curve.

### Opportunities
- **Growing Demand for Data-Driven Insights**: As businesses continue to prioritize data-driven decision-making, the demand for advanced analytics tools like Amplitude is increasing.
- **Expansion into Emerging Markets**: There is potential for growth by expanding into underpenetrated markets where digital adoption is accelerating.
- **AI and Machine Learning Integration**: Enhancing the platform with AI and machine learning could provide more predictive and prescriptive analytics capabilities.

### Threats
- **Intense Competition**: Competitors like Mixpanel and Heap are continuously evolving, which could impact Amplitude's market share.
- **Data Privacy Regulations**: Increasing regulations around data privacy and security could pose operational challenges and increase compliance costs.
- **Economic Uncertainty**: Economic downturns could lead to reduced IT budgets, affecting investments in analytics tools.

## Step 2: Recent Developments

### Amplitude
1. **New Feature Launches**: Amplitude has recently launched new features focusing on enhancing user engagement and retention metrics, providing more granular insights.
2. **Strategic Partnerships**: Amplitude has entered into strategic partnerships with cloud service providers to enhance data integration capabilities and improve service delivery.
3. **AI-Driven Enhancements**: Amplitude has started integrating AI-driven analytics to offer predictive insights, helping businesses anticipate user behavior changes.
### Competitors
1. **Mixpanel's New Interface**: Mixpanel has introduced a revamped user interface aimed at improving usability and providing more intuitive data visualization tools.
2. **Heap's Funding Round**: Heap has recently closed a significant funding round to invest in product development and expand its market reach.
3. **Heap's Automation Features**: Heap has launched new automation features that allow users to automatically capture and analyze user interactions without manual tagging.

## Step 3: Strategic Recommendations for Amplitude

1. **Enhance User Experience with Simplified Onboarding**: To address the complexity issue, Amplitude should focus on simplifying the user onboarding process. This could include providing more intuitive tutorials, personalized onboarding sessions, and enhanced customer support for new users.

2. **Expand AI and Machine Learning Capabilities**: Invest in expanding AI and machine learning features to offer more advanced predictive analytics. This would differentiate Amplitude by providing unique insights into potential future user behaviors, setting it apart from competitors.

3. **Target Emerging Markets with Tailored Solutions**: Develop tailored solutions aimed at emerging markets, focusing on affordability and ease of use. This approach could capture new customer segments and establish Amplitude as a leader in these growing regions, leveraging its scalable platform. 

By implementing these strategies, Amplitude can strengthen its market position, enhance its competitive edge, and drive growth in the dynamic product analytics industry.

"""

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
       #output= Test_text

       st.markdown("### 💡 Strategy Output")
       st.markdown(output)
       #output = test_text
       #testertext=test_text
       #print(testertext)

       # Save PowerPoint
       filename = f"{company}_strategy_summary.pptx"
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


