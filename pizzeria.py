import os
from dao.base import Session, engine, Base, borrar_todo
from dao.pizzas import Pizza
from dao.ingredientes import Ingrediente
from dao.pizza_ing import PizzaIng
from dao.equipo_pizza import EquipoPizza
from dao.equipos import Equipo

name_data_file = 'data\\a_example'
#name_data_file = 'data\\b_little_bit_of_everything.in'
#name_data_file = 'data\\c_many_ingredients.in'
#name_data_file = 'data\\d_many_pizzas.in'
#name_data_file = 'data\\e_many_teams.in'


def inicializar_bbdd():
    print('Iniciamos ejecucion de pizzeria')

    Base.metadata.create_all(engine)

    #Borramos todos los datos de las tablas
    session = Session()
    borrar_todo(engine.connect())
    session.commit()
    session.close()

    

def cargar_datos():
    datafile = open(name_data_file, 'r')

    cabecera = datafile.readline().split()
    print('Numero total de pizzas',cabecera[0])

    session = Session()
    num_pizza = 0
    for pizza_line in datafile.readlines():
        pizza = pizza_line.split()
        #print('La pizza',num_pizza,' tiene ',pizza[0], ' ingredientes:', pizza[1:])

        registro_pizza = Pizza(num_pizza, pizza[0])
        session.add(registro_pizza)
        for ingrediente in pizza[1:]:
            #Comprobamos si ya tenemos el ingrediente o es nuevo
            registro_ing = session.query(Ingrediente).filter(Ingrediente.ingrediente == ingrediente).first()
            if registro_ing is not None:
                pass
                #print('Ingrediente ya existe:',registro_ing.ingrediente, '-',registro_ing.id)
            else:
                registro_ing = Ingrediente(ingrediente)
                session.add(registro_ing)
                registro_ing = session.query(Ingrediente).filter(Ingrediente.ingrediente == ingrediente).first()
                #print('Nuevo ingrediente insertado:',registro_ing.ingrediente, '-',registro_ing.id)

            registro_pizza_ing = PizzaIng(registro_pizza.id, registro_ing.id)
            session.add(registro_pizza_ing)
        
        num_pizza = num_pizza + 1
        if num_pizza % 500 == 0:
            session.commit()
            print('Se han cargado ',num_pizza, ' pizzas')
    
    session.commit()
    session.close()

    return cabecera





inicializar_bbdd()
cabecera  = cargar_datos()
combinaciones = Pizza.combinaciones_pizzas(engine.connect())

for row in combinaciones:
    print(row.items())

print('Numero equipos 2 personas',cabecera[1])
print('Numero equipos 3 personas',cabecera[2])
print('Numero equipos 4 personas',cabecera[3])
