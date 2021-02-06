import os

name_data_file = 'data\\a_example'
datafile = open(name_data_file, 'r')

cabecera = datafile.readline().split()
print('Numero total de pizzas',cabecera[0])
print('Numero equipos 2 personas',cabecera[1])
print('Numero equipos 3 personas',cabecera[2])
print('Numero equipos 4 personas',cabecera[3])

for pizza_line in datafile.readlines():
    pizza = pizza_line.split()
    print('Pizza con ',pizza[0], ' ingredientes:', pizza[1:])
