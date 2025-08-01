import os
from dotenv import load_dotenv
from prompts import strategy_prompt
import streamlit as st
import openai

load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_strategy(company, product):
    prompt = strategy_prompt(company, product)
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        # Handle OpenAI API errors gracefully
        return f"Error generating strategy: {str(e)}"
