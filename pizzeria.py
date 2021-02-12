import os
from dao.base import Session, engine, Base, borrar_todo
from dao.pizzas import Pizza
from dao.ingredientes import Ingrediente
from dao.pizza_ing import PizzaIng
from dao.equipo_pizza import EquipoPizza
from dao.equipos import Equipo
import querys as q

#name_data_file = 'data\\a_example'
#name_data_file = 'data\\b_little_bit_of_everything.in'
#name_data_file = 'data\\c_many_ingredients.in'
#name_data_file = 'data\\d_many_pizzas.in'
name_data_file = 'data\\e_many_teams.in'

#name_output_file = 'data\\respuesta_a.txt'
#name_output_file = 'data\\respuesta_b.txt'
#name_output_file = 'data\\respuesta_c.txt'
#name_output_file = 'data\\respuesta_d.txt'
name_output_file = 'data\\respuesta_e.txt'

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

def crear_equipos(cabecera):
    session = Session()
    total_pizzas = int(cabecera[0])
    pizzas_restantes = total_pizzas

    for t in range(int(cabecera[3])):
        if (pizzas_restantes - 4) > 4 or (pizzas_restantes - 4) == 0 \
            or ((pizzas_restantes - 4) == 3 and int(cabecera[2]) > 0) \
            or ((pizzas_restantes - 4) == 2 and int(cabecera[1]) > 0):
            registro_pizza = Equipo(4)
            session.add(registro_pizza)
            pizzas_restantes = pizzas_restantes - 4

    for t in range(int(cabecera[2])):
        if (pizzas_restantes - 3) > 3 or (pizzas_restantes - 3) == 0 \
            or ((pizzas_restantes - 3) == 2 and int(cabecera[1]) > 0):
            registro_pizza = Equipo(3)
            session.add(registro_pizza)
            pizzas_restantes = pizzas_restantes - 3

    for t in range(int(cabecera[1])):
        if (pizzas_restantes - 2) > 2 or (pizzas_restantes - 2) == 0:
            registro_pizza = Equipo(2)
            session.add(registro_pizza)
            pizzas_restantes = pizzas_restantes - 2

    session.commit()
    session.close()



def calcular_mejores_pizzas(num_pizzas, total_ingredientes):
    combinaciones = q.combinaciones_pizzas(engine.connect(), num_pizzas)
    max_num_ing = 0
    max_ids_pizzas = None
    max_vueltas = 100
    for row in combinaciones:
        ids_pizzas = ''
        for val in row.values():
            ids_pizzas = ids_pizzas  + str(val)  + ','
        ids_pizzas = ids_pizzas[:-1]  
        num_ing = q.ingredientes_diferentes(engine.connect(), ids_pizzas)
        #print(ids_pizzas, '-', q.ingredientes_diferentes(engine.connect(), ids_pizzas))
        if num_ing > max_num_ing:
            max_num_ing = num_ing
            max_ids_pizzas = ids_pizzas
        if max_num_ing == total_ingredientes or max_vueltas == 0:
            break
        max_vueltas = max_vueltas - 1
    #print('El maximo de ingredientes es ', max_num_ing, 'con las pizzas', max_ids_pizzas)
    return max_ids_pizzas

def generar_salida():
    output_file = open(name_output_file, 'w')

    lista_equipo_salida = q.lista_equipo_salida(engine.connect())
    output_file.write(str(len(lista_equipo_salida)) + '\n')

    for equipo in lista_equipo_salida:
        lista_pizzas = q.lista_pizzas_equipo_salida(engine.connect(), equipo)
        linea = str(len(lista_pizzas))
        for pizza in lista_pizzas:
            linea = linea + ' ' + str(pizza)
        output_file.write(linea + '\n')


    


#Limpiamos la BBDD de ejecuciones anteriores
inicializar_bbdd()

#Leemos el fichero para cargarlo en BBDD y devuelve los datos de la cabecera
cabecera  = cargar_datos()
total_pizzas = cabecera[0]
pizzas_restantes = total_pizzas

#Se crean en BBDD los equipos a partir de la cabecera
crear_equipos(cabecera)

#recorremos los equipos para calcular sus pizzas
session = Session()
total_ingredientes = q.total_ingredientes(engine.connect())
lista_equipos = q.listado_equipos(engine.connect())
procesados = 0

for id_equipo, num_pizzas in lista_equipos:

    #Calculamos las mejor combinacion de pizzas para el equipo 
    ids_pizzas = calcular_mejores_pizzas(num_pizzas, total_ingredientes)

    if ids_pizzas is not None:
        #Asignamos las pizzas al equipo
        for id_pizza in ids_pizzas.split(','):
            registro = EquipoPizza(id_equipo, id_pizza)
            session.add(registro)
            session.commit()

    procesados = procesados + 1
    if procesados % 100 == 0:
        print('Se han procesado',procesados, 'de', len(lista_equipos))

generar_salida()
