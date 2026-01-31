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
            
            adk_event = ADKEvent.model_validate(event_dict)
            
            # author 추출
            author = adk_event.author
            # author가 'user'이면 'user', 그 외는 'model'로 표시
            role = 'user' if author == 'user' else 'model'
            
            # error_message 추출
            error_message = adk_event.error_message if hasattr(adk_event, 'error_message') else None
            
            # content 파싱
            if adk_event.content and adk_event.content.parts:
                for part in adk_event.content.parts:
                    # text가 있으면 처리
                    if part.text:
                        # output_schema로 생성된 JSON 응답인지 확인
                        try:
                            # JSON 파싱 시도
                            json_data = json.loads(part.text)
                            # response_message와 response_image_url이 있으면 output_schema 응답
                            if isinstance(json_data, dict) and ('response_message' in json_data or 'response_image_url' in json_data):
                                message = json_data.get('response_message')
                                image_url = json_data.get('response_image_url')
                                
                                # message가 있으면 추가
                                if message:
                                    events_response.append(EventGetResponse(
                                        role=role,
                                        content=EventContent(
                                            message=message,
                                            image_upload_url=None,
                                            image_upload_mime_type=None
                                        ),
                                        error_message=error_message
                                    ))
                                
                                # image가 있으면 별도로 추가
                                if image_url:
                                    events_response.append(EventGetResponse(
                                        role=role,
                                        content=EventContent(
                                            message=None,
                                            image_upload_url=image_url,
                                            image_upload_mime_type="image/png"  # 기본값
                                        ),
                                        error_message=error_message
                                    ))
                            else:
                                # JSON이지만 output_schema 형식이 아님 - 일반 텍스트로 처리
                                events_response.append(EventGetResponse(
                                    role=role,
                                    content=EventContent(
                                        message=part.text,
                                        image_upload_url=None,
                                        image_upload_mime_type=None
                                    ),
                                    error_message=error_message
                                ))
                        except (json.JSONDecodeError, ValueError):
                            # JSON이 아니면 일반 텍스트로 처리
                            events_response.append(EventGetResponse(
                                role=role,
                                content=EventContent(
                                    message=part.text,
                                    image_upload_url=None,
                                    image_upload_mime_type=None
                                ),
                                error_message=error_message
                            ))
                    
                    # file_data가 있으면 image로
                    elif part.file_data:
                        events_response.append(EventGetResponse(
                            role=role,
                            content=EventContent(
                                message=None,
                                image_upload_url=part.file_data.file_uri,
                                image_upload_mime_type=part.file_data.mime_type
                            ),
                            error_message=error_message
                        ))
            
            # error_message만 있는 경우
            elif error_message:
                events_response.append(EventGetResponse(
                    role=role,
                    content=None,
                    error_message=error_message
                ))
                
        except Exception as e:
            logger.error(f"Failed to parse event_data for event {db_event.id}: {e}")
            events_response.append(EventGetResponse(
                role="unknown",
                content=None,
                error_message=f"Failed to parse event: {str(e)}"
            ))
    
    return events_response