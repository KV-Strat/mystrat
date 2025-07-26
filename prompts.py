def strategy_prompt(company, competitors, industry):
    return f"""
You are a strategy consultant.

Company: {company}
Competitors: {competitors}
Industry: {industry}

Step 1: Do a SWOT analysis for {company} in {industry}
step 2: Identify some strengths, weaknesses,opportunities and threats in comparison of {competitors}
step 3: Identify threats from new entrants
step 4: Consolidate everything into 4 categories strengths, weaknesses, opportunities and threats
step 5: Only show step 4

Respond in markdown format.
"""
