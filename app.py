import json
from datetime import date
import pandas as pd
import streamlit as st
from utils.db import active_criteria,recent_runs
from services.validation_service import validate_criteria_configuration
from services.orchestrator import execute_rfp_run
st.set_page_config(page_title="Agentic RFP Evaluator",layout="wide",page_icon="🤖")
st.title("Agentic RFP Evaluation and Supplier Ranking")
st.caption("Evidence-grounded LLM evaluation with deterministic validation, peer benchmarking and ranking")
criteria=active_criteria()
try:validate_criteria_configuration(criteria)
except Exception as exc:st.error(str(exc));st.stop()
tab1,tab2,tab3=st.tabs(["New evaluation","How ranking works","Recent runs"])
with tab1:
 st.subheader("1. Active criteria loaded from SQLite");st.dataframe(pd.DataFrame(criteria)[["criterion_id","name","description","weight","max_score"]],use_container_width=True,hide_index=True);st.success(f'Total active weight: {sum(c["weight"] for c in criteria):.0f}%')
 st.subheader("2. Supplier proposals and metadata");count=st.number_input("Number of suppliers",2,8,4,1);entries=[]
 for i in range(int(count)):
  with st.expander(f"Supplier {i+1}",expanded=i==0):
   a,b,c=st.columns(3);name=a.text_input("Supplier name",key=f"name{i}");submitted=b.date_input("Submission date",date.today(),key=f"date{i}");experience=c.slider("Historical experience rating",0.0,10.0,5.0,0.5,key=f"exp{i}");pdf=st.file_uploader("Supplier proposal PDF",type=["pdf"],key=f"pdf{i}");entries.append({"supplier_name":name,"submission_date":submitted.isoformat(),"experience_rating":experience,"pdf":pdf})
 model=st.sidebar.text_input("Gemini model","gemini-2.5-flash");api_key=st.secrets.get("GEMINI_API_KEY","");st.sidebar.info("Store the API key only in Streamlit Secrets. Never commit it to GitHub.")
 if st.button("Evaluate all suppliers",type="primary"):
  errors=[];names=[]
  if not api_key:errors.append("GEMINI_API_KEY is not configured in Streamlit Secrets.")
  for i,e in enumerate(entries,1):
   key=e["supplier_name"].strip().casefold()
   if not key:errors.append(f"Supplier {i}: name is required.")
   elif key in names:errors.append(f"Supplier {i}: duplicate supplier name.")
   else:names.append(key)
   if e["pdf"] is None:errors.append(f"Supplier {i}: PDF is required.")
  if errors:
   for error in errors:st.error(error)
  else:
   status=st.status("Running agentic workflow",expanded=True);progress=st.progress(0)
   def callback(done,total,name):status.write(f"Completed extraction, evaluation and validation for {name}");progress.progress(done/total)
   try:st.session_state["run"]=execute_rfp_run(entries,criteria,api_key,model,callback);status.update(label="Workflow completed",state="complete")
   except Exception as exc:status.update(label="Workflow failed",state="error");st.error(str(exc))
 if "run" in st.session_state:
  run=st.session_state["run"];st.divider();st.subheader("3. Completed run");a,b,c=st.columns(3);a.metric("Run ID",run["rfp_run_id"][:8]+"...");b.metric("Status",run["status"]);c.metric("Suppliers",len(run["suppliers"]))
  board=pd.DataFrame([{k:s[k] for k in ["final_rank","supplier_name","absolute_score","ppi","submission_date","experience_rating"]} for s in run["suppliers"]]);st.subheader("Leaderboard");st.dataframe(board,use_container_width=True,hide_index=True);st.info("Tie-break order: higher PPI, earlier submission date, higher experience rating, supplier name ascending.")
  st.subheader("Supplier drill-down")
  for s in run["suppliers"]:
   with st.expander(f'Rank {s["final_rank"]}: {s["supplier_name"]} | Absolute {s["absolute_score"]} | PPI {s["ppi"]}'):
    for d in s["scorecard"]:
     leader=" 🏆" if d["is_benchmark_leader"] else "";st.markdown(f'**{d["criterion_name"]}{leader}**: {d["score"]}/{d["max_score"]} | Benchmark {d["benchmark"]} | Gap {d["gap"]:.2f} | Relative {d["relative_percent"]:.2f}% | Weight {d["weight"]}%');st.caption(f'Evidence: {d["evidence"]}');st.write("Justification:",d["justification"])
    if s["warnings"]:st.warning("Validation warnings: "+" | ".join(s["warnings"]))
    st.write("Risks:",s["evaluation"]["risks"]);st.write("Summary:",s["evaluation"]["overall_summary"])
  st.download_button("Download complete run as JSON",json.dumps(run,indent=2),f'{run["rfp_run_id"]}.json',"application/json")
with tab2:st.markdown("""### Deterministic formulas
- **Absolute score** = sum((validated score / maximum score) × criterion weight)
- **Benchmark** = highest validated score for each criterion
- **Gap** = supplier score - benchmark
- **Relative performance** = supplier score / benchmark × 100; if benchmark is zero, use 100%
- **PPI** = weighted average of relative-performance percentages

The LLM evaluates proposal evidence only. Python performs all calculations and determines the final rank.""")
with tab3:st.subheader("Persisted RFP runs");st.dataframe(pd.DataFrame(recent_runs()),use_container_width=True,hide_index=True)
