from app.domain import Plan,Task
class EngineeringPlanner:
 def plan(self,goal,repo):
  return Plan(objective=goal.goal,tasks=[
   Task(key="research",role="research",description="Understand repository and relevant code"),
   Task(key="code",role="coding",description="Implement smallest safe candidate change",depends_on=["research"],risk="WRITE"),
   Task(key="test",role="test",description="Run repository tests in isolated worktree",depends_on=["code"],command=["pytest","-q"]),
   Task(key="review",role="review",description="Review diff, test evidence and risk",depends_on=["test"]),
   Task(key="merge",role="merge",description="Prepare candidate integration",depends_on=["review"],risk="HIGH")
  ])
