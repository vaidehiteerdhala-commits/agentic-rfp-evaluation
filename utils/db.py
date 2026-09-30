import sqlite3,json
from db.seed_db import init_db,DB_PATH
def connection(db_path=DB_PATH):
 init_db(db_path);con=sqlite3.connect(db_path);con.row_factory=sqlite3.Row;return con
def active_criteria(db_path=DB_PATH):
 with connection(db_path) as con:return [dict(r) for r in con.execute("SELECT * FROM evaluation_criteria WHERE is_active=1 ORDER BY criterion_id")]
def create_run(run_id,created_at,status,db_path=DB_PATH):
 with connection(db_path) as con:con.execute("INSERT INTO rfp_runs(rfp_run_id,created_at,status) VALUES(?,?,?)",(run_id,created_at,status));con.commit()
def update_run_status(run_id,status,error_message=None,db_path=DB_PATH):
 with connection(db_path) as con:con.execute("UPDATE rfp_runs SET status=?,error_message=? WHERE rfp_run_id=?",(status,error_message,run_id));con.commit()
def persist_supplier_results(run,db_path=DB_PATH):
 with connection(db_path) as con:
  for s in run["suppliers"]:
   con.execute("INSERT INTO supplier_results(rfp_run_id,supplier_name,submission_date,experience_rating,absolute_score,ppi,final_rank,result_json) VALUES(?,?,?,?,?,?,?,?)",(run["rfp_run_id"],s["supplier_name"],s["submission_date"],s["experience_rating"],s["absolute_score"],s["ppi"],s["final_rank"],json.dumps(s)))
   for d in s["scorecard"]:con.execute("INSERT INTO criterion_results(rfp_run_id,supplier_name,criterion_id,score,benchmark,gap,relative_percent,weight,evidence,justification) VALUES(?,?,?,?,?,?,?,?,?,?)",(run["rfp_run_id"],s["supplier_name"],d["criterion_id"],d["score"],d["benchmark"],d["gap"],d["relative_percent"],d["weight"],d["evidence"],d["justification"]))
   for warning in s.get("warnings",[]):con.execute("INSERT INTO run_warnings(rfp_run_id,supplier_name,warning) VALUES(?,?,?)",(run["rfp_run_id"],s["supplier_name"],warning))
  con.commit()
def recent_runs(limit=10,db_path=DB_PATH):
 with connection(db_path) as con:return [dict(r) for r in con.execute("SELECT * FROM rfp_runs ORDER BY created_at DESC LIMIT ?",(limit,))]
