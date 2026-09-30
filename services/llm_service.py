import json
import random
import time

from google import genai


def _is_retryable_error(error):
    """
    Retry only temporary API failures.

    429 means too many requests.
    5xx errors indicate temporary server-side failures.
    """
    message = str(error).lower()

    retryable_markers = [
        "429",
        "resource_exhausted",
        "too many requests",
        "500",
        "502",
        "503",
        "504",
        "unavailable",
        "high demand",
        "internal server error",
        "deadline exceeded",
        "timeout",
    ]

    return any(marker in message for marker in retryable_markers)


def evaluate_with_gemini(
    api_key,
    model,
    supplier_name,
    document_text,
    criteria,
    max_attempts=5,
):
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an evidence-grounded RFP evaluation agent.

Evaluate supplier {supplier_name!r}.

RULES:
1. Use ONLY facts contained in the supplied proposal.
2. Do not use external knowledge.
3. Return exactly one result for every active criterion.
4. Scores must be numeric and between zero and database max_score.
5. Evidence must identify the page marker and quote or state a precise
   proposal fact.
6. If relevant evidence is missing, score conservatively and explicitly
   state that evidence is missing.
7. Return one valid JSON object only.
8. Do not return markdown, code fences, or explanatory text outside JSON.

REQUIRED JSON STRUCTURE:
{{
  "supplier_name": "...",
  "criteria": [
    {{
      "criterion_id": 1,
      "score": 0,
      "max_score": 10,
      "justification": "...",
      "evidence": "[PAGE 1] ..."
    }}
  ],
  "risks": ["..."],
  "overall_summary": "..."
}}

ACTIVE CRITERIA:
{json.dumps(criteria, indent=2)}

SUPPLIER PROPOSAL:
{document_text[:70000]}
"""

    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0,
                },
            )

            if not response.text:
                raise ValueError("The LLM returned an empty response.")

            return json.loads(response.text)

        except Exception as error:
            last_error = error

            if not _is_retryable_error(error):
                raise

            if attempt == max_attempts:
                break

            base_delay_seconds = 2 ** attempt
            jitter_seconds = random.uniform(0.5, 2.0)
            wait_seconds = min(
                base_delay_seconds + jitter_seconds,
                30,
            )

            time.sleep(wait_seconds)

    raise RuntimeError(
        "Gemini remained temporarily unavailable after "
        f"{max_attempts} attempts. Please wait a few minutes and "
        f"run the evaluation again. Last API error: {last_error}"
    )
