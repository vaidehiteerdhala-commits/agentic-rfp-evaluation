import sqlite3
from db.seed_db import init_db
def test_database_seed_and_schema(tmp_path):
 db=tmp_path/"test.db";init_db(db);con=sqlite3.connect(db);count=con.execute("SELECT COUNT(*) FROM evaluation_criteria WHERE is_active=1").fetchone()[0];total=con.execute("SELECT SUM(weight) FROM evaluation_criteria WHERE is_active=1").fetchone()[0];tables={r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")};con.close();assert count==5;assert total==100;assert {"rfp_runs","supplier_results","criterion_results","run_warnings"}.issubset(tables)
