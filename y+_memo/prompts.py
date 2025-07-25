# Save your long prompt template as a Python multi-line string.
startup_data = {
    "company_name": "Lume",
    "one_liner": "Put your health data to work.",
    "website": "join-lume.com",
    "source": "n/a",
    "founder_1": "Katie Kirsch",
    "bio_1": "4x founder and startup veteran. Stanford Engineer, Harvard Business School MBA, Certified leadership coach, Wears a WHOOP, uses EightSleep mattress",
    "linkedin_1": "https://www.linkedin.com/in/kirschkatie/",
    "founder_2": "Ari Gootnick",
    "bio_2": "4x startup operator. Managed 100+ coaches at On Deck and Summit. Certified yoga and breathwork instructor. Wears an Oura Ring.",
    "linkedin_2": "https://www.linkedin.com/in/arigoot/",
    "market_category": "Data Health",
    "launch_year": "2024",
    "hq_location": "San Francisco, CA",
    "team_size": "3",
    "cash_status": "-$10k in cash",
    "burn_rate": "$30k/month",
    "revenue": "$278k ARR",
    "stage": "Series A",
    "previous_funding": "13,000 Seed",
    "use_of_capital": "Fundraising to build the first proprietary work x wearable data and AI product, and acquire our first 50,000 users.",
}

base_prompt = """
You are an investment analyst at Y+ Ventures. Your job is to write a clean, structured investment memo for internal review, using the company information and evaluation criteria below. Use bullet points where appropriate and write in a clear, objective tone. Return the memo in Markdown format.

Y+ Ventures is committed to aggressively pursuing investments with unicorn-scale outcomes. Your memo should reflect this priority and evaluate each company through a lens grounded in data from *The Unicorn Report*. Key heuristics to inform your reasoning:

- **Early capital matters:** Unicorns raise their first VC round ~7 months sooner than peers; companies raising in their founding year are 38% more likely to hit $1B valuation.
- **Check size is predictive:** 
  - Seed round > $12.5M → 10.3% unicorn probability  
  - Series A > $30M → ~10% unicorn probability  
- **Round progression is a strong signal:** Most unicorns go through 5+ rounds; survival to Series D+ strongly correlates with success.
- **Median time to unicorn status is ~7 years**, with 75% reaching it within 9 years.
- **Team quality is paramount:** Team dynamics are the #1 cited reason for both success (56%) and failure (55%).
- **Valuation signals matter:** Unicorns consistently raise at higher post-money valuations than peers at each round.
- **Exit outcomes are asymmetric:** Over 50% of unicorns exit via IPO; only 3% fail outright.

Your analysis should identify whether the company has the ambition, velocity, and structure to scale to a $1B+ outcome within a 7–10 year window and return the fund.

[INPUT: Company Information]

- Company Name: {{company_name}}
- One-liner: {{one_liner}}
- Website: {{website}}
- Source: {{source}} (e.g., referred by X from Y firm)
- Founders: {{founder_1}} – {{bio_1}} ({{linkedin_1}}); {{founder_2}} – {{bio_2}} ({{linkedin_2}})
- Market Category: {{market_category}}
- Launch Year: {{launch_year}}
- Location: {{hq_location}}
- Team Size: {{team_size}}
- Current Cash: {{cash_status}}
- Burn Rate: {{burn_rate}}
- Revenue: {{revenue}}
- Stage: {{stage}}
- Raising: {{round_size}} at {{valuation}} post-money
- Previously Raised: {{previous_funding}}
- Use of Capital: {{use_of_capital}}
- Required Exit for Return the Fund: {{rtf_required}}

[INPUT: Scorecard Evaluation (1-5)]

- Founders: {{score_founders}} (Weight: {{weight_founders}})
- Team: {{score_team}} ({{weight_team}})
- Market: {{score_market}} ({{weight_market}})
- Problem: {{score_problem}} ({{weight_problem}})
- Solution: {{score_solution}} ({{weight_solution}})
- Business: {{score_business}} ({{weight_business}})
- Financials: {{score_financials}} ({{weight_financials}})
- Fundability: {{score_fundability}} ({{weight_fundability}})

[INPUT: Analyst Commentary]

- Investment Recommendation: {{recommendation}} (e.g., Invest / Pass / Further Due Diligence)
- Key Reasons: {{bullet_point_1}}, {{bullet_point_2}}, {{bullet_point_3}}

- Pre-Mortem:
  - End Picture: {{premortem_end_picture}}
  - Roadmap: {{premortem_roadmap}}
  - Key Risks: {{premortem_risks}}

- Pre-Parade:
  - De-risk Factors: {{preparade_de_risk}}

- Team Commentary: {{team_notes}}
- Market Commentary: {{market_notes}}
- Problem Commentary: {{problem_notes}}
- Solution Commentary: {{solution_notes}}
- Business Commentary: {{business_notes}}
- Financial Commentary: {{financial_notes}}

[OUTPUT FORMAT]

# Y+ Ventures Investment Memo – {{company_name}}

## Business Summary  
**Overview:** {{one_liner}}  
**Website:** {{website}}  
**Source:** {{source}}  
**Founders:** {{founder summary}}  
**Market Category:** {{market_category}}  
**Launch Year:** {{launch_year}}  
**Location:** {{hq_location}}  
**Stage:** {{stage}}  
**Raising:** ${{round_size}} at ${{valuation}} post  
**Use of Capital:** {{use_of_capital}}  
**RTF Target Exit:** ${{rtf_required}}  

## Investment Recommendation  
**Decision:** {{recommendation}}  
**Rationale:**  
- {{bullet_point_1}}  
- {{bullet_point_2}}  
- {{bullet_point_3}}  

## Strategic Framing  
This section sets the stage for evaluating both the potential pitfalls and the mitigating factors that can ensure success. It is divided into two parts to help you envision the ideal outcome, understand the necessary steps to get there, and consider what factors lower risk.

**Pre-Mortem:**  
- *End Picture:* {{premortem_end_picture}}  
  *Description:* Describe in detail the ultimate successful outcome for the company. Explain the envisioned state when all milestones are achieved, capturing the impact, scale, and market position. For example, "A scalable platform recognized as the industry standard for accessible therapy."
- *Roadmap:* {{premortem_roadmap}}  
  *Description:* Outline the critical phases and initiatives required to reach the end picture. Include strategic milestones, key growth targets, and the timeline of activities. This roadmap should provide a clear path that connects current status to long-term goals.
- *Risks:* {{premortem_risks}}  
  *Description:* Identify and elaborate on the potential challenges and obstacles that could derail the plan. Highlight both internal and external risks such as competitive pressure, regulatory issues, operational limitations, or market dynamics that must be addressed.

**Pre-Parade:**  
- *De-risk Factors:* {{preparade_de_risk}}  
  *Description:* Summarize the strengths, preemptive measures, and strategic advantages that reduce or mitigate the identified risks. These de-risk factors may include a strong founding team, strategic partnerships, early market traction, or innovative product features that provide a competitive edge.
 

## Evaluation Deep Dive

### Team  
{{team_notes}}

### Market  
{{market_notes}}

### Problem  
{{problem_notes}}

### Solution  
{{solution_notes}}

### Business  
{{business_notes}}

### Financials  
{{financial_notes}}

## Scorecard Summary  
| Category     | Score | Weight |
|--------------|-------|--------|
| Founders     | {{score_founders}} | {{weight_founders}} |
| Team         | {{score_team}}     | {{weight_team}} |
| Market       | {{score_market}}   | {{weight_market}} |
| Problem      | {{score_problem}}  | {{weight_problem}} |
| Solution     | {{score_solution}} | {{weight_solution}} |
| Business     | {{score_business}} | {{weight_business}} |
| Financials   | {{score_financials}} | {{weight_financials}} |
| Fundability  | {{score_fundability}} | {{weight_fundability}} |

## Appendix  
*Raw notes from diligence can be found in CRM or internal doc links.*
"""

def format_prompt(data, base_prompt):
    # Simple replacement – in production, consider using a templating engine
    formatted = base_prompt
    for key, value in data.items():
        formatted = formatted.replace("{{" + key + "}}", str(value))
    return formatted

# For now, you might combine company data with some default score values:
default_scorecard = {
    "score_founders": "4",
    "weight_founders": "1.0",
    "score_team": "4",
    "weight_team": "0.9",
    "score_market": "3",
    "weight_market": "0.8",
    "score_problem": "4",
    "weight_problem": "0.7",
    "score_solution": "3",
    "weight_solution": "0.8",
    "score_business": "3",
    "weight_business": "0.7",
    "score_financials": "2",
    "weight_financials": "0.6",
    "score_fundability": "4",
    "weight_fundability": "0.9",
    # Default commentary can be added as needed
    "recommendation": "Further Due Diligence",
    "bullet_point_1": "Strong team with proven track record.",
    "bullet_point_2": "Market opportunity is significant.",
    "bullet_point_3": "Product differentiation needs more clarity.",
    "premortem_end_picture": "Scalable product with competitive positioning.",
    "premortem_roadmap": "Expand market reach within 2 years.",
    "premortem_risks": "Competitive pressure and regulatory risks.",
    "preparade_de_risk": "Early partnerships mitigate risks.",
    "team_notes": "Founders have deep industry expertise.",
    "market_notes": "Market size is large but fragmented.",
    "problem_notes": "Addressing a clear pain point.",
    "solution_notes": "Innovative solution, though execution risk remains.",
    "business_notes": "Business model is solid with room for optimization.",
    "financial_notes": "Financials are early-stage but promising.",
}

# Merge the dictionaries:
combined_data = {**startup_data, **default_scorecard}

# Format the prompt:
final_prompt = format_prompt(combined_data, base_prompt)
print(final_prompt)
