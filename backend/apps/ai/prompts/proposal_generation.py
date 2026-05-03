"""
Prompts for AI-powered proposal generation.
"""

EXECUTIVE_SUMMARY_PROMPT = """
You are an expert grant writer creating an executive summary for a grant proposal.

ORGANIZATION INFORMATION:
Name: {org_name}
Mission: {org_mission}
Focus Areas: {org_categories}

GRANT INFORMATION:
Title: {grant_title}
Funder: {grant_funder}
Amount Requested: ${amount_requested}
Focus Areas: {grant_categories}

PROJECT INFORMATION:
{project_info}

Write a compelling executive summary (250-300 words) that:
1. Clearly states the problem being addressed
2. Describes the proposed solution
3. Highlights the organization's qualifications
4. Emphasizes the expected impact
5. Aligns with the funder's priorities

The summary should be professional, concise, and persuasive.
"""

PROJECT_DESCRIPTION_PROMPT = """
You are an expert grant writer creating a detailed project description.

ORGANIZATION INFORMATION:
Name: {org_name}
Mission: {org_mission}
Focus Areas: {org_categories}

GRANT INFORMATION:
Title: {grant_title}
Funder: {grant_funder}
Amount Requested: ${amount_requested}

PROJECT OVERVIEW:
{project_overview}

Write a comprehensive project description (800-1000 words) that includes:

1. PROBLEM STATEMENT
   - Clearly define the problem or need
   - Provide relevant statistics and evidence
   - Explain why this problem is important

2. GOALS AND OBJECTIVES
   - State specific, measurable goals
   - List clear objectives with timelines
   - Explain expected outcomes

3. METHODS AND STRATEGIES
   - Describe the approach and methodology
   - Explain why this approach is effective
   - Detail the implementation timeline

4. EVALUATION PLAN
   - Describe how success will be measured
   - List key performance indicators
   - Explain data collection methods

5. SUSTAINABILITY
   - Explain how the project will continue after funding
   - Describe potential future funding sources
   - Highlight long-term impact

The description should be detailed, evidence-based, and compelling.
"""

BUDGET_JUSTIFICATION_PROMPT = """
You are an expert grant writer creating a budget justification.

ORGANIZATION INFORMATION:
Name: {org_name}
Annual Budget: ${org_budget}

GRANT INFORMATION:
Title: {grant_title}
Amount Requested: ${amount_requested}

BUDGET BREAKDOWN:
{budget_items}

Write a clear budget justification (400-500 words) that:

1. Explains each major budget category
2. Justifies why each expense is necessary
3. Shows how costs were calculated
4. Demonstrates cost-effectiveness
5. Aligns expenses with project activities
6. Addresses any matching funds or in-kind contributions

The justification should be transparent, reasonable, and well-documented.
"""

# Made with Bob
