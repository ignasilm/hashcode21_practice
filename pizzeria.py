import os
from dao.base import Session, engine, Base, borrar_todo
from dao.pizzas import Pizza
from dao.ingredientes import Ingrediente
from dao.pizza_ing import PizzaIng
from dao.equipo_pizza import EquipoPizza
from dao.equipos import Equipo
import querys as q
import numpy as np

caso = 'a'

   

def crear_equipos(total_pizzas, nEq2, nEq3, nEq4):
    session = Session()
    pizzas_restantes = total_pizzas
    equipos = []

    for t in range(nEq4):
        if (pizzas_restantes - 4) > 4 or (pizzas_restantes - 4) == 0 \
            or ((pizzas_restantes - 4) == 3 and int(nEq3) > 0) \
            or ((pizzas_restantes - 4) == 2 and int(nEq2) > 0):
            equipos.append(4)
            pizzas_restantes = pizzas_restantes - 4

    for t in range(nEq3):
        if (pizzas_restantes - 3) > 3 or (pizzas_restantes - 3) == 0 \
            or ((pizzas_restantes - 3) == 2 and int(nEq2) > 0):
            equipos.append(3)
            pizzas_restantes = pizzas_restantes - 3

    for t in range(nEq2):
        if (pizzas_restantes - 2) > 2 or (pizzas_restantes - 2) == 0:
            equipos.append(2)
            pizzas_restantes = pizzas_restantes - 2
    
    return equipos



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


    



#Leemos el fichero para cargarlo en BBDD y devuelve los datos de la cabecera
if caso == 'a':
    name_data_file = 'data\\a_example'
    name_output_file = 'data\\respuesta_a.txt'
elif caso == 'b':
    name_data_file = 'data\\b_little_bit_of_everything.in'
    name_output_file = 'data\\respuesta_b.txt'
elif caso == 'c':
    name_data_file = 'data\\c_many_ingredients.in'
    name_output_file = 'data\\respuesta_c.txt'
elif caso == 'd':
    name_data_file = 'data\\d_many_pizzas.in'
    name_output_file = 'data\\respuesta_d.txt'
elif caso == 'e':
    name_data_file = 'data\\e_many_teams.in'
    name_output_file = 'data\\respuesta_e.txt'

datafile = open(name_data_file, 'r')

#Declaramos variables para leer total de pizzas y total de cada tipo de equipo
nPizzas=0
nEq2=0
nEq3=0
nEq4=0
# Leemos numero pizzas, equipos de 2, 3 y 4 miembros
nPizzas, nEq2, nEq3, nEq4= map(int, datafile.readline().split())
#Declaramos una lista con las pizzas que leeremos
pizzas = []
print('Numero total de pizzas',nPizzas)

# Leemos todas las pizzas. Las metemos en una lista cada una, ignorando el primer elemento
# El motivo de ignorar el primer elemento, es que nos dice cuantos ingredientes son, pero por 
# ahorrar espacio no lo metemos y siempre podemos calcular con la funcion "len"
num_pizza = 0
ingredientes = dict()
for pizza_line in datafile.readlines():
    pizza = pizza_line.split()[1:]
    pizzas.append(pizza)
    print('La pizza',num_pizza,' tiene ',len(pizza), ' ingredientes:', pizza)

    for ingrediente in pizza:
        #Comprobamos si ya tenemos el ingrediente o es nuevo
        if ingrediente not in ingredientes:
            ingredientes[ingrediente] = len(ingredientes)

    num_pizza = num_pizza + 1
    if num_pizza % 500 == 0:
        print('Se han cargado ',num_pizza, ' pizzas')

#Se crean en BBDD los equipos a partir de la cabecera
crear_equipos(nPizzas, nEq2, nEq3, nEq4)

exit(0)

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
    if procesados % 500 == 0:
        print('Se han procesado',procesados, 'de', len(lista_equipos))

generar_salida()
