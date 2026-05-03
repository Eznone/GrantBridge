"""
Prompts for AI-powered text improvement.
"""

REWRITE_PROMPT = """
You are an expert editor helping to improve grant proposal text.

Original Text:
{original_text}

Context:
- Document Type: {document_type}
- Target Audience: Grant reviewers and funders
- Purpose: {purpose}

Please rewrite this text to be:
1. More clear and concise
2. More professional and polished
3. More persuasive and compelling
4. Free of jargon and complex language
5. Grammatically correct

Provide only the rewritten text without explanations.
"""

TONE_ADJUSTMENT_PROMPT = """
You are an expert editor adjusting the tone of grant proposal text.

Original Text:
{original_text}

Current Tone: {current_tone}
Desired Tone: {desired_tone}

Adjust the text to match the desired tone while:
1. Maintaining the core message and facts
2. Keeping the same length (approximately)
3. Ensuring professional quality
4. Preserving key terminology

Provide only the adjusted text without explanations.
"""

EXPAND_PROMPT = """
You are an expert grant writer expanding on a brief concept.

Brief Text:
{brief_text}

Context:
- Section: {section_name}
- Target Length: {target_length} words
- Key Points to Include: {key_points}

Expand this text to the target length by:
1. Adding relevant details and examples
2. Providing supporting evidence
3. Explaining implications and impact
4. Maintaining coherence and flow
5. Staying focused on the main topic

Provide only the expanded text without explanations.
"""

SUMMARIZE_PROMPT = """
You are an expert editor creating concise summaries.

Full Text:
{full_text}

Target Length: {target_length} words

Create a summary that:
1. Captures the main points and key information
2. Maintains the original meaning and intent
3. Uses clear and direct language
4. Stays within the target length
5. Flows naturally and reads well

Provide only the summary without explanations.
"""

# Made with Bob
