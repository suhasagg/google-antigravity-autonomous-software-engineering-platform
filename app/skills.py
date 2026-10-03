from app.domain import Skill
SKILLS=[
 Skill(id="repo.inspect",description="Inspect repository structure",role="research"),
 Skill(id="git.search",description="Search tracked code",role="research"),
 Skill(id="test.pytest",description="Run Python tests",role="test",command=["pytest","-q"]),
 Skill(id="lint.ruff",description="Run Ruff",role="test",command=["ruff","check","."]),
 Skill(id="git.diff",description="Collect candidate patch",role="review"),
 Skill(id="benchmark.make",description="Run repository benchmark target",role="test",command=["make","benchmark"])
]
def all_skills():return SKILLS
def get_skill(i):return next((s for s in SKILLS if s.id==i),None)
