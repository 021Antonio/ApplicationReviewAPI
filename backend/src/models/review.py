from sqlalchemy import Column, Integer, String
from models.base import Base

class Review(Base):
    __tablename__ = "review"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    review = Column(String, index=True)
    estrelas = Column(Integer)
    serie_filme = Column(String)
