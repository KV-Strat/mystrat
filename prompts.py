def strategy_prompt(company, competitors, industry):
    return f"""
You are a senior strategy consultant.

Company: {company}
Competitors: {competitors}
Industry: {industry}

Step 1: Generate a SWOT analysis for {company} in comparison with {competitors}

Respond in markdown format.
"""
