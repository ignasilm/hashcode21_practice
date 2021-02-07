from sqlalchemy.sql import text
from dao.equipo_pizza import EquipoPizza
from dao.equipos import Equipo

def combinaciones_pizzas(con, num_pizzas):

    sql_select = 'select p1.id as id1'
    for n in range(2,num_pizzas+1):
        sql_select = sql_select + ', p' + str(n) + '.id as id' + str(n)

    sql_select = sql_select + ' FROM (SELECT pz1.id FROM PIZZAS pz1 LEFT JOIN EQUIPO_PIZZA epz1 ON pz1.id = epz1.id_pizza WHERE epz1.id_pizza is null) p1'
    for n in range(2,num_pizzas+1):
        sql_select = sql_select + ' CROSS JOIN (SELECT pz' + str(n) +'.id FROM PIZZAS pz' + str(n) +' LEFT JOIN EQUIPO_PIZZA epz' + str(n) +' ON pz' + str(n) +'.id = epz' + str(n) +'.id_pizza WHERE epz' + str(n) +'.id_pizza is null ) p' + str(n)

    if num_pizzas == 2:
        sql_select = sql_select + ' WHERE p1.id <> p2.id \
                                    and p2.id > p1.id'
    elif num_pizzas == 3:
        sql_select = sql_select + ' WHERE p1.id <> p2.id and p1.id <> p3.id and p2.id <> p3.id \
                                    and p2.id > p1.id \
                                    and p3.id > p2.id' 
    elif num_pizzas == 4:
        sql_select = sql_select + ' WHERE p1.id <> p2.id and p1.id <> p3.id and p1.id <> p4.id \
                                    and p2.id <> p3.id and p2.id <> p4.id \
                                    and p3.id <> p4.id  \
                                    and p2.id > p1.id \
                                    and p3.id > p2.id \
                                    and p4.id > p3.id' 

    #sql_select = sql_select + ' order by random() ;'
    sql_select = sql_select + ' ;'
    
    print(sql_select)
    query = text(sql_select)
    combinaciones = con.execute(query)
    return combinaciones

def ingredientes_diferentes(con, ids_pizzas):
    query = text('select count(distinct pi1.id_ingrediente) as num_ing \
                  from pizza_ing pi1 \
                  where pi1.id_pizza in (' + ids_pizzas + ');')
    result = con.execute(query)
    return result.first().num_ing

def total_ingredientes(con):
    #query = text('select count(distinct ing.id) as num_ing \
    #              from ingredientes ing;')
    query = text('SELECT count(distinct pzi1.id_ingrediente) as num_ing \
                FROM PIZZA_ING pzi1 \
                LEFT JOIN EQUIPO_PIZZA epz1 ON pzi1.id_pizza = epz1.id_pizza \
                WHERE epz1.id_pizza is null;')
    result = con.execute(query)
    return result.first().num_ing


def listado_equipos(con):
    query = text('select id, num_pizzas \
                  from equipos \
                  order by num_pizzas desc, id asc;')
    result = con.execute(query)
    lista_equipos = []
    for row in result:
        lista_equipos.append((row.id, row.num_pizzas))
    result.close()
    return lista_equipos

def lista_equipo_salida(con):
    query = text('select distinct epz.id_equipo \
                    from EQUIPO_PIZZA epz;')
    result = con.execute(query)
    lista_equipos = []
    for row in result:
        lista_equipos.append(row.id_equipo)
    result.close()
    return lista_equipos

def lista_pizzas_equipo_salida(con, id_equipo):
    query = text('select distinct epz.id_pizza \
                    from EQUIPO_PIZZA epz \
                    where epz.id_equipo = ' + str(id_equipo) + ';')
    result = con.execute(query)
    lista_pizzas = []
    for row in result:
        lista_pizzas.append(row.id_pizza)
    result.close()
    return lista_pizzas
