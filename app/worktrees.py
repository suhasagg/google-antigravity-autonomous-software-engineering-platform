from pathlib import Path
import subprocess,uuid,shutil
from app.config import settings
def run(args,cwd=None,timeout=60):
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=timeout)
 if p.returncode:raise RuntimeError(p.stderr or p.stdout)
 return p.stdout
class WorktreeManager:
 def create(self,repo,base_ref,run_id,task_key):
  root=Path(settings.workspace_root);root.mkdir(parents=True,exist_ok=True)
  dest=root/f"{run_id}-{task_key}-{uuid.uuid4().hex[:8]}";branch=f"agent/{run_id}/{task_key}"
  run(["git","worktree","add","-b",branch,str(dest),base_ref],repo)
  return {"path":str(dest),"branch":branch}
 def diff(self,path):return run(["git","diff","--binary"],path)
 def cleanup(self,repo,path):
  try:run(["git","worktree","remove","--force",path],repo)
  except Exception:shutil.rmtree(path,ignore_errors=True)
