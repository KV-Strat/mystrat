import os
from dotenv import load_dotenv
from prompts import strategy_prompt
from openai import OpenAI

load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_strategy(company, competitors, industry):
    prompt = strategy_prompt(company, competitors, industry)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        # Handle OpenAI API errors gracefully
        return f"Error generating strategy: {str(e)}"
