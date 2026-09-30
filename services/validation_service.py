def validate_criteria_configuration(criteria):
 if not criteria:raise ValueError("No active criteria are configured.")
 total=sum(float(c["weight"]) for c in criteria)
 if abs(total-100)>0.001:raise ValueError(f"Active criterion weights total {total}, not 100%.")
 ids=[int(c["criterion_id"]) for c in criteria]
 if len(ids)!=len(set(ids)):raise ValueError("Duplicate active criterion IDs exist.")
 if any(float(c["max_score"])<=0 for c in criteria):raise ValueError("All maximum scores must be positive.")
def normalize(raw,supplier_name,criteria):
 validate_criteria_configuration(criteria);warnings=[]
 if not isinstance(raw,dict):warnings.append("LLM output was not a JSON object; all criteria defaulted to zero.");raw={}
 items=raw.get("criteria",[])
 if not isinstance(items,list):warnings.append("Criteria was not a list; all criteria defaulted to zero.");items=[]
 active={int(c["criterion_id"]):c for c in criteria};accepted={}
 for pos,item in enumerate(items,1):
  if not isinstance(item,dict):warnings.append(f"Criterion item {pos} was not an object and was ignored.");continue
  try:cid=int(item.get("criterion_id"))
  except Exception:warnings.append(f"Criterion item {pos} had an invalid ID and was ignored.");continue
  if cid not in active:warnings.append(f"Unknown criterion {cid} was ignored.");continue
  if cid in accepted:warnings.append(f"Duplicate criterion {cid} was ignored after the first occurrence.");continue
  try:
   if isinstance(item.get("score"),bool):raise ValueError
   score=float(item.get("score"))
  except Exception:warnings.append(f"Criterion {cid} had a non-numeric score and defaulted to zero.");score=0.0
  maximum=float(active[cid]["max_score"]);clipped=min(max(score,0.0),maximum)
  if clipped!=score:warnings.append(f"Criterion {cid} score {score} clipped to {clipped}.")
  try:model_max=float(item.get("max_score"))
  except Exception:model_max=None
  if model_max!=maximum:warnings.append(f"Criterion {cid} max_score normalized to database value {maximum}.")
  evidence=str(item.get("evidence") or "Not provided.").strip();justification=str(item.get("justification") or "Not provided.").strip()
  if evidence=="Not provided.":warnings.append(f"Criterion {cid} did not contain supporting evidence.")
  accepted[cid]={"criterion_id":cid,"score":clipped,"max_score":maximum,"justification":justification,"evidence":evidence}
 normalized=[]
 for cid,c in active.items():
  if cid not in accepted:
   warnings.append(f"Missing criterion {cid}; defaulted to zero.")
   accepted[cid]={"criterion_id":cid,"score":0.0,"max_score":float(c["max_score"]),"justification":"No valid result returned.","evidence":"Not provided."}
  normalized.append(accepted[cid])
 risks=raw.get("risks",[]) if isinstance(raw.get("risks",[]),list) else []
 return {"supplier_name":supplier_name,"criteria":normalized,"risks":risks,"overall_summary":str(raw.get("overall_summary") or "")},warnings
