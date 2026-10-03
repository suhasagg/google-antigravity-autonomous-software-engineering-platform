import uuid
from datetime import datetime
from sqlalchemy import String,Text,Integer,Boolean,DateTime,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func
from app.db import Base
def uid():return uuid.uuid4()
class Run(Base):
 __tablename__="runs";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[str]=mapped_column(String(128),index=True);principal_id:Mapped[str]=mapped_column(String(256));repository:Mapped[str]=mapped_column(Text);goal:Mapped[str]=mapped_column(Text);status:Mapped[str]=mapped_column(String(32),index=True,default="CREATED");plan:Mapped[dict|None]=mapped_column(JSONB,nullable=True);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class TaskRecord(Base):
 __tablename__="tasks";__table_args__=(UniqueConstraint("run_id","task_key"),);id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);run_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),index=True);task_key:Mapped[str]=mapped_column(String(128));role:Mapped[str]=mapped_column(String(32));status:Mapped[str]=mapped_column(String(32),index=True,default="PENDING");request:Mapped[dict]=mapped_column(JSONB,default=dict);result:Mapped[dict|None]=mapped_column(JSONB,nullable=True);attempt:Mapped[int]=mapped_column(Integer,default=0);fencing_token:Mapped[int]=mapped_column(Integer,default=0)
class Approval(Base):
 __tablename__="approvals";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);run_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),index=True);task_key:Mapped[str]=mapped_column(String(128));action_hash:Mapped[str]=mapped_column(String(64));status:Mapped[str]=mapped_column(String(32),default="PENDING")
class Outbox(Base):
 __tablename__="outbox";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);event_type:Mapped[str]=mapped_column(String(128),index=True);aggregate_id:Mapped[str]=mapped_column(String(128));payload:Mapped[dict]=mapped_column(JSONB);published:Mapped[bool]=mapped_column(Boolean,default=False,index=True)
class Idempotency(Base):
 __tablename__="idempotency";__table_args__=(UniqueConstraint("tenant_id","scope","key"),);id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);tenant_id:Mapped[str]=mapped_column(String(128));scope:Mapped[str]=mapped_column(String(128));key:Mapped[str]=mapped_column(String(256));request_hash:Mapped[str]=mapped_column(String(64));result:Mapped[dict|None]=mapped_column(JSONB,nullable=True)
class Artifact(Base):
 __tablename__="artifacts";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);run_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),index=True);kind:Mapped[str]=mapped_column(String(64));path:Mapped[str]=mapped_column(Text);sha256:Mapped[str]=mapped_column(String(64));meta:Mapped[dict]=mapped_column(JSONB,default=dict)
class Audit(Base):
 __tablename__="audit";id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid);run_id:Mapped[uuid.UUID|None]=mapped_column(UUID(as_uuid=True),nullable=True,index=True);actor:Mapped[str]=mapped_column(String(256));event_type:Mapped[str]=mapped_column(String(128));data:Mapped[dict]=mapped_column(JSONB,default=dict);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
