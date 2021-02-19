import os
from dao.base import Session, engine, Base, borrar_todo
from dao.pizzas import Pizza
from dao.ingredientes import Ingrediente
from dao.pizza_ing import PizzaIng
from dao.equipo_pizza import EquipoPizza
from dao.equipos import Equipo
import querys as q
import numpy as np
import pandas as pd

caso = 'e'


def crear_equipos2(total_pizzas, nEq2, nEq3, nEq4):
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

    equipos.sort()

    return equipos

def crear_equipos(total_pizzas, nEq2, nEq3, nEq4):
    pizzas_restantes = total_pizzas
    equipos = []

    for n in range(nEq4+nEq3+nEq2):
        if nEq4>0 and ((pizzas_restantes - 4) > 4 or (pizzas_restantes - 4) == 0 \
            or ((pizzas_restantes - 4) == 3 and int(nEq3) > 0) \
            or ((pizzas_restantes - 4) == 2 and int(nEq2) > 0)):
            equipos.append(4)
            pizzas_restantes = pizzas_restantes - 4
            nEq4 = nEq4 -1

        if nEq3>0 and ((pizzas_restantes - 3) > 3 or (pizzas_restantes - 3) == 0 \
            or ((pizzas_restantes - 3) == 2 and int(nEq2) > 0)):
            equipos.append(3)
            pizzas_restantes = pizzas_restantes - 3
            nEq3 = nEq3 -1

        if nEq2>0 and ((pizzas_restantes - 2) > 2 or (pizzas_restantes - 2) == 0):
            equipos.append(2)
            pizzas_restantes = pizzas_restantes - 2
            nEq2 = nEq2 -1

    return equipos


def calcular_mejores_pizzas(num_pizzas, total_ingredientes, df_pizzas):

    #ordeno las pizzas por numero de ingredientes
    #df_pizzas = df_pizzas.sort_values(by=[0], ascending=False)
    #print(df_pizzas.head())

    #Recogemos el numero de ingredientes del primer elemento
    ingredientes_pz1 = df_pizzas.iloc[0,1]
    #Guardamos el ID del primer elemento
    idx1 = df_pizzas.iloc[0,0]
    indices = []
    indices.append(idx1)
    #Preparamos lista sin la pizza escogida y la ordenamos al reves
    df_sublista = df_pizzas.loc[df_pizzas['id_pizza'] != idx1].sort_values(by=['num_ing'], ascending=True)
    #la ordenamos al reves
    #df_sublista.sort_values(by=['num_ing'], ascending=True, inplace= True)
    if num_pizzas >= 3:
        idx2 = df_sublista.iloc[0,0]
        df_sublista = df_sublista.loc[df_pizzas['id_pizza'] != idx2]
        indices.append(idx2)
    if num_pizzas == 4:
        idx3 = df_sublista.iloc[0,0]
        df_sublista = df_sublista.loc[df_pizzas['id_pizza'] != idx3]
        indices.append(idx3)


    max_num_ing = 0
    max_ids_pizzas = None
    max_vueltas = 100
    for index, row in df_sublista.iterrows():
        indices_selec = indices.copy()
        indices_selec.append(row.id_pizza)
        ids_pizzas = ''
        #df_sel = df_pizzas.loc[(df_pizzas['id_pizza'] == idx1) | (df_pizzas['id_pizza'] == row.id_pizza)]
        df_sel = df_pizzas[df_pizzas.id_pizza.isin(indices_selec)]
        ids_pizzas = df_sel['id_pizza']
        num_ing = sum(df_sel.max()[2:])
        #print(ids_pizzas, '-', q.ingredientes_diferentes(engine.connect(), ids_pizzas))
        if num_ing > max_num_ing:
            max_num_ing = num_ing
            max_ids_pizzas = ids_pizzas
        if max_num_ing == total_ingredientes or max_vueltas == 0:
            break
        max_vueltas = max_vueltas - 1
    
    
    #print('El maximo de ingredientes es ', max_num_ing, 'con las pizzas', max_ids_pizzas)
    return max_ids_pizzas

def generar_salida(lista_equipo_salida):
    output_file = open(name_output_file, 'w')

    output_file.write(str(len(lista_equipo_salida)) + '\n')

    for equipo in lista_equipo_salida:
        output_file.write(equipo + '\n')


    



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
pizzas_ing = []
print('Numero total de pizzas',nPizzas)

# Leemos todas las pizzas. Las metemos en una lista cada una, ignorando el primer elemento
# El motivo de ignorar el primer elemento, es que nos dice cuantos ingredientes son, pero por 
# ahorrar espacio no lo metemos y siempre podemos calcular con la funcion "len"
num_pizza = 0
ingredientes = dict()
for pizza_line in datafile.readlines():
    pizza = pizza_line.split()
    pizzas_ing.append(pizza[1:])
    pizzas.append(int(pizza[0]))
    #print('La pizza',num_pizza,' tiene ',len(pizza), ' ingredientes:', pizza)

    for ingrediente in pizza[1:]:
        #Comprobamos si ya tenemos el ingrediente o es nuevo
        if ingrediente not in ingredientes:
            #print(ingrediente, len(ingredientes), 'en pizza',num_pizza, 'con este contenido',pizza[1:])
            ingredientes[ingrediente] = len(ingredientes)

    num_pizza = num_pizza + 1
    if num_pizza % 500 == 0:
        pass
        #print('Se han cargado ',num_pizza, ' pizzas')

print('Total de ingredientes entre todas las pizzas',len(ingredientes))

#print('Lista de ingredientes',ingredientes)

#Preparo un DataFranme con todas las pizzas y sus ingredientes por columnas
df_pizzas = pd.DataFrame(pizzas, columns=['num_ing'])
for ing in ingredientes.keys():
    df_pizzas[ing] = 0
#print(df_pizzas.head())
for i in range(len(df_pizzas)):
    for ing in pizzas_ing[i]:
        df_pizzas.loc[i,ing]=1



#ordeno las pizzas por numero de ingredientes
df_pizzas.sort_values(by=['num_ing'], ascending=False, inplace= True)

#guardo el indice como columna
df_pizzas.reset_index(inplace=True)
df_pizzas = df_pizzas.rename(columns = {'index':'id_pizza'})

#print(df_pizzas.head())
#print(df_pizzas.dtypes)

#Se crean los equipos a partir de la cabecera
lista_equipos = crear_equipos(nPizzas, nEq2, nEq3, nEq4)

#recorremos los equipos para calcular sus pizzas
total_ingredientes = len(ingredientes)
procesados = 0
equipos_salida = []

for num_pizzas in lista_equipos:

    #Calculamos las mejor combinacion de pizzas para el equipo 
    ids_pizzas = calcular_mejores_pizzas(num_pizzas, total_ingredientes, df_pizzas)

    lista_pizzas = ''
    if ids_pizzas is not None:
        #Asignamos las pizzas al equipo
        #for id_pizza in ids_pizzas:
        for id_pizza in ids_pizzas:
            lista_pizzas = lista_pizzas + ' ' + str(id_pizza)
            #eliminamos las pizzas seleccionadas
            df_pizzas = df_pizzas[df_pizzas['id_pizza'] != id_pizza]

    equipos_salida.append(str(num_pizzas) + lista_pizzas)

    procesados = procesados + 1
    if procesados % 100 == 0:
        print('Se han procesado',procesados, 'de', len(lista_equipos))

generar_salida(equipos_salida)
