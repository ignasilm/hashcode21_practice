from sqlalchemy import Column, Integer
from dao.base import Base

class PizzaIng(Base):
    __tablename__ = 'PIZZA_ING'

    mapa_campos = {}
    
    id = Column(Integer, primary_key=True)
    id_pizza = Column(Integer)
    id_ingrediente = Column(Integer)
    
    def __init__(self, id_pizza, id_ingrediente):
        self.id_pizza = id_pizza
        self.id_ingrediente = id_ingrediente
    
