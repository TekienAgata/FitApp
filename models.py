from sqlalchemy import Column, Integer, String, Text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
        }
