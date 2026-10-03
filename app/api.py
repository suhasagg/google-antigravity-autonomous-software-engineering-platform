from fastapi import APIRouter,Depends
from app.security import auth
from app.domain import EngineeringGoal
from app.skills import all_skills
from app.runtime import EngineeringRuntime
router=APIRouter(prefix="/v1",dependencies=[Depends(auth)])
@router.get("/skills")
async def skills():return [x.model_dump() for x in all_skills()]
@router.post("/engineering/run")
async def run(g:EngineeringGoal):return await EngineeringRuntime().execute(g)
