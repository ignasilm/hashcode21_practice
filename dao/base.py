from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


engine = create_engine('sqlite:///bbdd/pizza_e.db', connect_args={'timeout': 15})
Session = sessionmaker(bind=engine)

Base = declarative_base()


def borrar_todo(con):
    print('Se van a borrar todos los datos.')
    tablas = ['PIZZAS', 'INGREDIENTES', 'PIZZA_ING', 'EQUIPOS', 'EQUIPO_PIZZA']

    for tabla in tablas:
        query = text('delete from ' + tabla + ';')
        borrados = con.execute(query)
        print('Se han eliminado',borrados.rowcount,'de la tabla', tabla)

