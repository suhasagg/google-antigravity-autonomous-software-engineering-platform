import asyncio,os
from pathlib import Path
from app.config import settings
ALLOWED={"python","python3","pytest","go","cargo","npm","pnpm","yarn","make","git","ruff"}
class Sandbox:
 async def exec(self,cwd,cmd,env=None):
  if not cmd or Path(cmd[0]).name not in ALLOWED:raise ValueError("command not allowed by sandbox policy")
  proc=await asyncio.create_subprocess_exec(*cmd,cwd=cwd,env={**os.environ,**(env or {})},stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,start_new_session=True)
  try:out,err=await asyncio.wait_for(proc.communicate(),settings.sandbox_timeout_seconds)
  except asyncio.TimeoutError:
   proc.kill();await proc.wait();return {"status":"TIMEOUT","code":-1,"stdout":"","stderr":"timeout"}
  return {"status":"SUCCEEDED" if proc.returncode==0 else "FAILED","code":proc.returncode,"stdout":out.decode(errors="replace")[-20000:],"stderr":err.decode(errors="replace")[-20000:]}
