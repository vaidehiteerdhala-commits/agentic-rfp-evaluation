import json
from db.seed_db import init_db
from utils.db import active_criteria
from services.validation_service import normalize
from services.scoring_service import score_and_rank
init_db();criteria=active_criteria();profiles=[("Apex Systems","2026-09-20",8,[9,7,6,9,7]),("BrightPath Tech","2026-09-18",5,[7,9,10,4,5]),("NexaWorks","2026-09-19",8.5,[8,10,8,8,10]),("Orbit Digital","2026-09-17",9.5,[6,7,8,7,9])];suppliers=[]
for name,date,exp,scores in profiles:
 raw={"supplier_name":name,"criteria":[{"criterion_id":c["criterion_id"],"score":score,"max_score":10.0,"justification":"Synthetic deterministic demonstration score.","evidence":"See the corresponding section in the synthetic proposal."} for c,score in zip(criteria,scores)],"risks":[],"overall_summary":"Synthetic deterministic demonstration."};evaluation,warnings=normalize(raw,name,criteria);suppliers.append({"supplier_name":name,"submission_date":date,"experience_rating":exp,"evaluation":evaluation,"warnings":warnings})
run={"rfp_run_id":"DEMO-SUCCESS-001","created_at":"2026-09-28T12:00:00Z","status":"COMPLETED","suppliers":score_and_rank(suppliers,criteria)};open("exports/sample_completed_run.json","w").write(json.dumps(run,indent=2))
bad={"supplier_name":"Validation Test Supplier","criteria":[{"criterion_id":1,"score":15,"max_score":99,"justification":"test","evidence":"test"},{"criterion_id":1,"score":8,"max_score":10},{"criterion_id":99,"score":5,"max_score":10}]};out,warnings=normalize(bad,"Validation Test Supplier",criteria);open("exports/validation_error_case.json","w").write(json.dumps({"input":bad,"normalized_output":out,"warnings":warnings},indent=2));print("Generated successful and validation demonstration exports")
