from pydantic import BaseModel,Field
class CriterionResult(BaseModel):
 criterion_id:int
 score:float
 max_score:float
 justification:str=""
 evidence:str=""
class EvaluationResult(BaseModel):
 supplier_name:str
 criteria:list[CriterionResult]=Field(default_factory=list)
 risks:list[str]=Field(default_factory=list)
 overall_summary:str=""
