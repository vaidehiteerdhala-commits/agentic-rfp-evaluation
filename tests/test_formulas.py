from services.scoring_service import score_and_rank
C=[{"criterion_id":1,"name":"A","weight":60,"max_score":10},{"criterion_id":2,"name":"B","weight":40,"max_score":10}]
def s(n,d,e,a,b):return {"supplier_name":n,"submission_date":d,"experience_rating":e,"evaluation":{"criteria":[{"criterion_id":1,"score":a,"max_score":10,"justification":"","evidence":""},{"criterion_id":2,"score":b,"max_score":10,"justification":"","evidence":""}]}}
def test_formulas():
 out=score_and_rank([s("A","2026-01-01",5,10,5),s("B","2026-01-02",5,5,10)],C);a=next(x for x in out if x["supplier_name"]=="A");assert a["absolute_score"]==80;assert a["ppi"]==80;assert a["scorecard"][1]["benchmark"]==10;assert a["scorecard"][1]["gap"]==-5
def test_submission_date_tie_break():assert score_and_rank([s("Later","2026-01-02",10,8,8),s("Earlier","2026-01-01",1,8,8)],C)[0]["supplier_name"]=="Earlier"
def test_experience_tie_break():assert score_and_rank([s("Low","2026-01-01",2,8,8),s("High","2026-01-01",9,8,8)],C)[0]["supplier_name"]=="High"
def test_name_tie_break():assert score_and_rank([s("Zulu","2026-01-01",9,8,8),s("Alpha","2026-01-01",9,8,8)],C)[0]["supplier_name"]=="Alpha"
def test_zero_benchmark():assert score_and_rank([s("A","2026-01-01",5,0,0),s("B","2026-01-02",5,0,0)],C)[0]["ppi"]==100
