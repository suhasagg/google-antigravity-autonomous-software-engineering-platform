from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 database_url:str="postgresql+asyncpg://postgres:postgres@localhost:5432/antigravity"
 redis_url:str="redis://localhost:6379/0";kafka_bootstrap:str="localhost:9092";api_key:str="change-me"
 workspace_root:str="/tmp/antigravity-workspaces";artifact_root:str="/tmp/antigravity-artifacts";mcp_mode:str="mock";model_mode:str="deterministic"
 max_parallel_tasks:int=8;sandbox_timeout_seconds:int=120
 model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
