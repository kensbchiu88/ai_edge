
from app.db.schemas.streaming import Streaming


class StreamingRepository:
    def __init__(self, session):
        self.session = session

    def get_streaming(self):
        return self.session.query(Streaming).all()
    
    def get_streaming_by_uri(self, uri: str):
        return self.session.query(Streaming).filter(Streaming.uri == uri).first()
    
    def get_streaming_by_uri(self, uri):
        return self.session.query(Streaming).filter(Streaming.uri == uri).first()