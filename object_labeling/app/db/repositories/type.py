from app.db.schemas.type import Type


class TypeRepository:
    def __init__(self, session):
        self.session = session

    def get_types(self):
        return self.session.query(Type).all()