from swot_generator import generate_strategy
from export import create_ppt

company = "Amplitude"
competitors = "Mixpanel, Heap"
industry = "Product Analytics"

output = generate_strategy(company, competitors, industry)
print(output)
create_ppt(output, filename=f"{company}_strategy_summary.pptx")