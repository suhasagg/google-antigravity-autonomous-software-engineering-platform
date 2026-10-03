import httpx
from app.config import settings
class MCPGateway:
 async def list_tools(self):return [{"name":"repo.search"},{"name":"ci.status"},{"name":"issue.lookup"}] if settings.mcp_mode=="mock" else []
 async def call(self,name,args):
  if settings.mcp_mode=="mock":return {"tool":name,"status":"SUCCEEDED","result":{"echo":args}}
  raise RuntimeError("configure deployment-specific MCP endpoint and authentication")
