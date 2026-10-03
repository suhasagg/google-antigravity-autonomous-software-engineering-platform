import asyncio
class SubagentManager:
 async def fanout(self,jobs,limit=4):
  sem=asyncio.Semaphore(limit)
  async def one(fn):
   async with sem:return await fn()
  return await asyncio.gather(*(one(j) for j in jobs))
