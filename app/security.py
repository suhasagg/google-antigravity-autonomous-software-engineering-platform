import hmac,hashlib,json
from fastapi import Header,HTTPException
from app.config import settings
async def auth(x_api_key:str=Header(...)):
 if not hmac.compare_digest(x_api_key,settings.api_key):raise HTTPException(401,"invalid credential")
def action_hash(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
