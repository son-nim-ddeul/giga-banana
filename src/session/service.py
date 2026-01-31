from sqlalchemy.orm import Session
from .models import Session, Event
from .schemas import EventContent, EventGetResponse
import json
import logging
from google import genai


logger = logging.getLogger(__name__)

def get_list_sessions(db: Session, user_id: str):
    return db.query(Session).filter(Session.user_id == user_id).all()


def get_list_events(db: Session, session_id: str):
    events = db.query(Event).filter(Event.session_id == session_id).order_by(Event.timestamp.asc()).all()
    if not events:
        return []
    
    events_response = []
    for db_event in events:
        try:
            # event_data는 이미 dict 타입 (JSONB)
            event_dict = db_event.event_data
            
            # Event 객체로 복원
            from google.adk.events import Event as ADKEvent
            adk_event = ADKEvent.model_validate({
                **event_dict,
                "id": db_event.id,
                "invocation_id": db_event.invocation_id,
                "timestamp": db_event.timestamp.timestamp(),
            })
            
            # author 추출
            author = adk_event.author
            author_display = 'user' if author == 'user' else 'model'
            
            # error_message 추출
            error_message = adk_event.error_message if hasattr(adk_event, 'error_message') else None
            
            # content 파싱 - 실제로 표시할 내용이 있는 것만 추가
            if adk_event.content and adk_event.content.parts:
                for part in adk_event.content.parts:
                    event_content = None
                    
                    # text가 있으면 message로
                    if part.text:
                        event_content = EventContent(
                            message=part.text,
                            image_upload_url=None,
                            image_upload_mime_type=None
                        )
                    # file_data가 있으면 image로
                    elif part.file_data:
                        event_content = EventContent(
                            message=None,
                            image_upload_url=part.file_data.file_uri,
                            image_upload_mime_type=part.file_data.mime_type
                        )
                    
                    # 실제 content가 있을 때만 추가
                    if event_content:
                        events_response.append(EventGetResponse(
                            author=author_display,
                            content=event_content,
                            error_message=error_message
                        ))
            
            # error_message만 있는 경우에도 추가 (에러 표시 필요)
            elif error_message:
                events_response.append(EventGetResponse(
                    author=author_display,
                    content=None,
                    error_message=error_message
                ))
                
        except Exception as e:
            logger.error(f"Failed to parse event_data for event {db_event.id}: {e}")
            raise e
    
    return events_response