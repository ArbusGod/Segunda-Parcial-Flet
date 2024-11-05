import sqlite3 as sq
import os
from random import randrange

def conectarBanco():
    database = sq.connect('assets/database/productos.db')
    cursor = database.cursor()
    return database, cursor

nombre_productos = os.listdir('assets/img')
i = 0

lista_productos = []

with open('descripcion.txt', mode='r', encoding='UTF-8') as arquivo:
    descripcion_productos = arquivo.readlines()
    for producto in descripcion_productos:
        nombre_producto = []
        if producto[:11] == 'Descripcion':
            nombre = nombre_productos[i]
            descripcion = (producto[12:].replace('\n', '')).strip()
            precio = randrange(200, 600)

            nombre_producto = [nombre, descripcion, precio]
            lista_productos.append(nombre_producto)
            i += 1

database, cursor = conectarBanco()

try:
    # for producto in lista_productos:
    #    cursor.execute(
    #        'INSERT INTO productos (nombre, descripcion, precio) VALUES (?, ?, ?)',
    #        (producto[0], producto[1], producto[2])
    #    )
    # database.commit()

    # Consultar los datos añadidos
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    for prod in productos:
        print(prod)
except sq.Error as e:
    print(f"Ocurrió un error: {e}")
finally:
    if database:
        database.close()
