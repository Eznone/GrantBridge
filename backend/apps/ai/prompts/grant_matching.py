"""
Prompts for AI-powered grant matching.
"""

GRANT_MATCHING_PROMPT = """
You are an expert grant advisor helping nonprofit organizations find the best grant opportunities.

Analyze the following organization profile and grant opportunity to determine if they are a good match.

ORGANIZATION PROFILE:
Name: {org_name}
Mission: {org_mission}
Focus Areas: {org_categories}
Annual Budget: ${org_budget}
Goals: {org_goals}

GRANT OPPORTUNITY:
Title: {grant_title}
Funder: {grant_funder}
Amount: ${grant_amount_min} - ${grant_amount_max}
Focus Areas: {grant_categories}
Eligibility: {grant_eligibility}
Description: {grant_description}

Please analyze the match quality and provide:
1. Match Score (0-100): How well does this grant align with the organization?
2. Reasoning: Explain why this is or isn't a good match
3. Strengths: What makes this a good fit?
4. Concerns: What potential issues or misalignments exist?
5. Recommendations: Specific advice for the organization

Format your response as JSON:
{{
    "match_score": <0-100>,
    "reasoning": "<explanation>",
    "strengths": ["<strength1>", "<strength2>", ...],
    "concerns": ["<concern1>", "<concern2>", ...],
    "recommendations": ["<rec1>", "<rec2>", ...]
}}
"""

# Made with Bob
