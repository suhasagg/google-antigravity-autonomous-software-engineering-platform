from pathlib import Path
class ResearchAgent:
 async def run(self,repo_info,goal):return {"summary":f"Repository has {repo_info['files']} files. Goal: {goal}","head":repo_info["head"],"languages":repo_info["languages"]}
class CodingAgent:
 async def run(self,worktree,goal,research):
  # Safe reference behavior: create an agent proposal artifact instead of silently rewriting arbitrary source.
  p=Path(worktree)/".antigravity";p.mkdir(exist_ok=True)
  f=p/"PROPOSAL.md";f.write_text(f"# Candidate engineering proposal\n\nGoal: {goal}\n\nResearch: {research}\n",encoding="utf-8")
  return {"changed":[str(f.relative_to(worktree))],"note":"Candidate change produced in isolated worktree"}
class DebugAgent:
 async def run(self,test_result):return {"diagnosis":"Inspect failing stderr/stdout and create targeted repair task","test_result":test_result}
class ReviewerAgent:
 async def run(self,diff,test_result):
  passed=test_result.get("status")=="SUCCEEDED"
  return {"decision":"PASS" if passed and diff.strip() else "REPAIR","tests_passed":passed,"diff_bytes":len(diff.encode()),"risks":[] if passed else ["tests_failed"]}
