def score_and_rank(suppliers,criteria):
 by_id={int(c["criterion_id"]):c for c in criteria}
 benchmarks={cid:max((next(x["score"] for x in s["evaluation"]["criteria"] if x["criterion_id"]==cid) for s in suppliers),default=0) for cid in by_id}
 for s in suppliers:
  absolute=0.0;ppi=0.0;details=[]
  for x in s["evaluation"]["criteria"]:
   c=by_id[x["criterion_id"]];weight=float(c["weight"]);maximum=float(c["max_score"]);benchmark=benchmarks[x["criterion_id"]]
   relative=(x["score"]/benchmark*100) if benchmark>0 else 100.0
   absolute+=(x["score"]/maximum)*weight;ppi+=relative*weight/100
   details.append({**x,"criterion_name":c["name"],"weight":weight,"benchmark":benchmark,"gap":x["score"]-benchmark,"relative_percent":relative,"is_benchmark_leader":x["score"]==benchmark})
  s["absolute_score"]=round(absolute,2);s["ppi"]=round(ppi,2);s["scorecard"]=details
 suppliers.sort(key=lambda x:(-x["ppi"],x["submission_date"],-float(x["experience_rating"]),x["supplier_name"].casefold()))
 for rank,s in enumerate(suppliers,1):s["final_rank"]=rank
 return suppliers
