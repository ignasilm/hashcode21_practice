from sqlalchemy import Column, Integer, String
from dao.base import Base

class Ingrediente(Base):
    __tablename__ = 'INGREDIENTES'

    mapa_campos = {}
    
    id = Column(Integer, primary_key=True)
    ingrediente = Column(String(20))
    
    def __init__(self, ingrediente):
        self.ingrediente = ingrediente
    
