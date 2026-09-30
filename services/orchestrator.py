import uuid
from datetime import datetime,timezone
from services.pdf_service import extract_pdf_text
from services.llm_service import evaluate_with_gemini
from services.validation_service import normalize
from services.scoring_service import score_and_rank
from utils.db import create_run,update_run_status,persist_supplier_results
def execute_rfp_run(entries,criteria,api_key,model,progress_callback=None):
 run_id=str(uuid.uuid4());created_at=datetime.now(timezone.utc).isoformat();create_run(run_id,created_at,"PROCESSING");audit=[];results=[]
 try:
  for index,entry in enumerate(entries):
   name=entry["supplier_name"].strip();audit.append({"supplier":name,"step":"PDF_EXTRACTION","status":"STARTED"})
   text,pages=extract_pdf_text(entry["pdf"],True);audit[-1].update({"status":"COMPLETED","pages":pages,"characters":len(text)})
   audit.append({"supplier":name,"step":"LLM_EVALUATION","status":"STARTED"});raw=evaluate_with_gemini(api_key,model,name,text,criteria);audit[-1]["status"]="COMPLETED"
   evaluation,warnings=normalize(raw,name,criteria);audit.append({"supplier":name,"step":"VALIDATION","status":"COMPLETED","warnings":warnings})
   results.append({"supplier_name":name,"submission_date":entry["submission_date"],"experience_rating":float(entry["experience_rating"]),"document_pages":pages,"evaluation":evaluation,"warnings":warnings})
   if progress_callback:progress_callback(index+1,len(entries),name)
  ranked=score_and_rank(results,criteria);run={"rfp_run_id":run_id,"created_at":created_at,"status":"COMPLETED","tie_break_order":["PPI descending","submission date ascending","experience rating descending","supplier name ascending"],"audit_trail":audit,"suppliers":ranked}
  persist_supplier_results(run);update_run_status(run_id,"COMPLETED");return run
 except Exception as exc:update_run_status(run_id,"FAILED",str(exc));raise
