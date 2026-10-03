from app.domain import Plan,Task
from app.compiler import compile_plan
def test_dag():assert len(compile_plan(Plan(objective="x",tasks=[Task(key="a",role="research",description="a"),Task(key="b",role="test",description="b",depends_on=["a"])])))==2
