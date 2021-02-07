from sqlalchemy import Column, Integer
from dao.base import Base

class Equipo(Base):
    __tablename__ = 'EQUIPOS'

    mapa_campos = {}
    
    id = Column(Integer, primary_key=True)
    num_pizzas = Column(Integer)
    
    def __init__(self, num_pizzas ):
        self.num_pizzas = num_pizzas
    
