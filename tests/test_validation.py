import pytest
from services.validation_service import normalize,validate_criteria_configuration
C=[{"criterion_id":1,"name":"A","weight":60,"max_score":10},{"criterion_id":2,"name":"B","weight":40,"max_score":10}]
def test_missing_clipping_and_max():
 out,w=normalize({"criteria":[{"criterion_id":1,"score":15,"max_score":99}]},"S",C);assert out["criteria"][0]["score"]==10;assert out["criteria"][1]["score"]==0;assert any("clipped" in x for x in w);assert any("Missing criterion 2" in x for x in w)
def test_duplicate_unknown_and_non_numeric():
 raw={"criteria":[{"criterion_id":1,"score":"bad"},{"criterion_id":1,"score":9},{"criterion_id":99,"score":2}]};out,w=normalize(raw,"S",C);assert out["criteria"][0]["score"]==0;assert any("Duplicate" in x for x in w);assert any("Unknown" in x for x in w)
def test_invalid_weight_total():
 with pytest.raises(ValueError):validate_criteria_configuration([{**C[0],"weight":50},C[1]])
