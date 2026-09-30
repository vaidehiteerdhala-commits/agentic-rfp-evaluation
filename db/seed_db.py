from pathlib import Path
import sqlite3
DB_PATH=Path(__file__).resolve().parents[1]/"data"/"rfp_evaluation.db"
CRITERIA=[
(1,"Technical Capability","Architecture, integrations, scalability and technical fit",30.0,10.0,1),
(2,"Implementation Plan","Timeline, milestones, staffing and risk plan",20.0,10.0,1),
(3,"Commercial Value","Pricing clarity, total cost and assumptions",20.0,10.0,1),
(4,"Security & Compliance","Controls, certifications, privacy and auditability",20.0,10.0,1),
(5,"Support & Experience","Support model, similar projects and references",10.0,10.0,1)]
def init_db(db_path=DB_PATH):
 db_path=Path(db_path);db_path.parent.mkdir(parents=True,exist_ok=True);con=sqlite3.connect(db_path)
 con.executescript("""
 CREATE TABLE IF NOT EXISTS evaluation_criteria(criterion_id INTEGER PRIMARY KEY,name TEXT NOT NULL,description TEXT NOT NULL,weight REAL NOT NULL,max_score REAL NOT NULL,is_active INTEGER NOT NULL);
 CREATE TABLE IF NOT EXISTS rfp_runs(rfp_run_id TEXT PRIMARY KEY,created_at TEXT NOT NULL,status TEXT NOT NULL,error_message TEXT);
 CREATE TABLE IF NOT EXISTS supplier_results(id INTEGER PRIMARY KEY AUTOINCREMENT,rfp_run_id TEXT NOT NULL,supplier_name TEXT NOT NULL,submission_date TEXT NOT NULL,experience_rating REAL NOT NULL,absolute_score REAL NOT NULL,ppi REAL NOT NULL,final_rank INTEGER NOT NULL,result_json TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS criterion_results(id INTEGER PRIMARY KEY AUTOINCREMENT,rfp_run_id TEXT NOT NULL,supplier_name TEXT NOT NULL,criterion_id INTEGER NOT NULL,score REAL NOT NULL,benchmark REAL NOT NULL,gap REAL NOT NULL,relative_percent REAL NOT NULL,weight REAL NOT NULL,evidence TEXT,justification TEXT);
 CREATE TABLE IF NOT EXISTS run_warnings(id INTEGER PRIMARY KEY AUTOINCREMENT,rfp_run_id TEXT NOT NULL,supplier_name TEXT,warning TEXT NOT NULL);
 """)
 con.executemany("""INSERT INTO evaluation_criteria VALUES(?,?,?,?,?,?) ON CONFLICT(criterion_id) DO UPDATE SET name=excluded.name,description=excluded.description,weight=excluded.weight,max_score=excluded.max_score,is_active=excluded.is_active""",CRITERIA)
 con.commit();con.close();return db_path
if __name__=='__main__':print(init_db())
