import json
from google import genai
def evaluate_with_gemini(api_key,model,supplier_name,document_text,criteria):
 client=genai.Client(api_key=api_key)
 prompt=f"""You are an evidence-grounded RFP evaluation agent. Evaluate supplier {supplier_name!r}.
RULES:
1. Use ONLY facts in the supplied proposal. Do not use external knowledge.
2. Return exactly one result for every active criterion.
3. Scores must be numeric and between zero and database max_score.
4. Evidence must identify the page marker and quote or state a precise proposal fact.
5. If evidence is missing, score conservatively and explicitly say it is missing.
6. Return one valid JSON object only, with no markdown or commentary.
SCHEMA:
{{"supplier_name":"...","criteria":[{{"criterion_id":1,"score":0,"max_score":10,"justification":"...","evidence":"[PAGE 1] ..."}}],"risks":["..."],"overall_summary":"..."}}
ACTIVE CRITERIA:
{json.dumps(criteria,indent=2)}
PROPOSAL:
{document_text[:70000]}"""
 response=client.models.generate_content(model=model,contents=prompt,config={"response_mime_type":"application/json","temperature":0})
 if not response.text:raise ValueError("The LLM returned an empty response.")
 return json.loads(response.text)
