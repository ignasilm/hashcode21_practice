from sqlalchemy import Column, Integer
from dao.base import Base
from sqlalchemy.sql import text

class Pizza(Base):
    __tablename__ = 'PIZZAS'

    mapa_campos = {}
    
    id = Column(Integer, primary_key=True)
    num_ing = Column(Integer)
    
    def __init__(self, id, num_ing ):
        self.id = id
        self.num_ing = num_ing
    
    def combinaciones_pizzas(con):
        query = text('select p1.id as id1, p2.id as id2, p3.id as id3 \
                      from PIZZAS p1 \
                      cross join PIZZAS p2 \
                      cross join PIZZAS p3 \
                      where p1.id <> p2.id and p1.id <> p3.id and p2.id <> p3.id \
                            and p2.id > p1.id \
                            and p3.id > p2.id;')
        combinaciones = con.execute(query)
        return combinaciones
