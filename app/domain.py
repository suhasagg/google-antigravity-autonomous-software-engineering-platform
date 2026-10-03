from pydantic import BaseModel,Field
from typing import Any,Literal
class EngineeringGoal(BaseModel):
 tenant_id:str="demo";principal_id:str="engineer";repository:str;goal:str;base_ref:str="HEAD";context:dict[str,Any]=Field(default_factory=dict)
class Task(BaseModel):
 key:str;role:Literal["research","coding","debug","test","review","merge"];description:str;depends_on:list[str]=Field(default_factory=list);risk:Literal["READ","WRITE","HIGH"]="READ";command:list[str]|None=None
class Plan(BaseModel):objective:str;tasks:list[Task];version:int=1
class Skill(BaseModel):id:str;description:str;role:str;risk:str="READ";command:list[str]|None=None
