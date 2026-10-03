from pathlib import Path
import hashlib,json
from app.config import settings
def save(run_id,name,data):
 root=Path(settings.artifact_root)/str(run_id);root.mkdir(parents=True,exist_ok=True)
 p=root/name
 if isinstance(data,(dict,list)):p.write_text(json.dumps(data,indent=2,default=str),encoding="utf-8")
 else:p.write_text(str(data),encoding="utf-8")
 return {"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"size":p.stat().st_size}
