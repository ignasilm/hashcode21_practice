from sqlalchemy import Column, Integer
from dao.base import Base

class Pizza(Base):
    __tablename__ = 'PIZZAS'

    mapa_campos = {}
    
    id = Column(Integer, primary_key=True)
    num_ing = Column(Integer)
    
    def __init__(self, id, num_ing ):
        self.id = id
        self.num_ing = num_ing
    
