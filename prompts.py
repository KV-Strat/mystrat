def strategy_prompt(company, product):
    return f"""
You are a strategy engine.

Company: {company}
Product: {product}

Step 1: List its top 5 core capabilities (functional or technical).
Step 2: Based on those capabilities, identify 5 industries that are best suited to adopt this product.
Step 3: For each industry, explain in 1–2 sentences why the product is a strong fit based on its capabilities.
Step 4: Return your answer in markdown format with clear headings: "Core Capabilities", "Best-Fit Industries".
"""
