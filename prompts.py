def strategy_prompt(company, competitors, industry):
    return f"""
You are a senior strategy consultant.

Company: {company}
Competitors: {competitors}
Industry: {industry}

Step 1: Generate a SWOT analysis for {company}.
Step 2: Identify 3 recent developments for {company} and its competitors.
Step 3: Recommend 3 strategic moves for {company} to differentiate in this market.

Respond in markdown format.
"""