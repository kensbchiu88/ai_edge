
from typing import List
from app.db.schemas.label import Label


class LabelRepository:
    def __init__(self, session):
        self.session = session

    def save_label(self, label):
        self.session.add(label)
        self.session.commit()
        self.session.refresh(label)
        return label

    def get_labels_by_streaming_id(self, streaming_data_id):
        return self.session.query(Label).filter(Label.streaming_data_id == streaming_data_id).all()
    
    def delete_labels_by_streaming_id(self, streaming_data_id):
        self.session.query(Label).filter(Label.streaming_data_id == streaming_data_id).delete()
        self.session.commit()
    
    def save(self, labels: List[Label]):
        self.session.bulk_save_objects(labels)
        self.session.commit()