from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any, List


class SessionCreateRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: str
    metadata: Optional[Dict[str, Any]] = Field(None, description="세션 메타데이터")

class SessionCreateResponse(BaseModel):
    user_id: str
    session_id: str

class SessionGetResponse(BaseModel):
    session_id: str

class SessionListResponse(BaseModel):
    user_id: str
    sessions: List[SessionGetResponse]

class EventContent(BaseModel):
    message: str | None = None
    image_upload_url: str | None = None
    image_upload_mime_type: str | None = None

class EventGetResponse(BaseModel):
    role: str    
    content: EventContent | None = None
    error_message: str | None = None

class EventListResponse(BaseModel):
    events: List[EventGetResponse] = Field(..., description="이벤트 목록")