from sqlalchemy import Column, Integer
from dao.base import Base

class EquipoPizza(Base):
    __tablename__ = 'EQUIPO_PIZZA'

    mapa_campos = {}
    
    id = Column(Integer, primary_key=True)
    id_equipo = Column(Integer)
    id_pizza = Column(Integer)
    
    def __init__(self, id_equipo, id_pizza):
        self.id_equipo = id_equipo
        self.id_pizza = id_pizza
    
