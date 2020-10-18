"""
En el siguiente codigo fuente se realizan la resolucion del ejercicio_profundizacion.py
"""

__author__ = "Pablo Ruiz Diaz"
__email__ = "rd.pablo@gmail.com.ar"
__version__ = "1.0"

import sqlite3
import csv

def fetch(id):
    conn = sqlite3.connect('libreria_sql.db')
    c = conn.cursor()

    if id != 0:
        c.execute("""
            SELECT * FROM libreria WHERE id = ?; 
            """, [id])
    else:
        c.execute("""
            SELECT * FROM libreria; 
            """)
        
    while True:
        row = c.fetchone()

        if row is None:
            break
            
        print(row)

    conn.close()


def search_author(book_title):
    conn = sqlite3.connect('libreria_sql.db')
    c = conn.cursor()

    c.execute("""
        SELECT author FROM libreria WHERE title = ?; 
        """, [book_title])
    
    author = c.fetchall()
    conn.close()

    return author


def update(new_title,id):
    conn = sqlite3.connect('libreria_sql.db')
    c = conn.cursor()

    c.execute("""
            UPDATE libreria SET title = ? WHERE id = ?;
            """, [new_title, id])

    conn.commit()
    conn.close()


def delete(id):
    conn = sqlite3.connect('libreria_sql.db')
    c = conn.cursor()

    c.execute("""
            DELETE FROM libreria WHERE id = ?
            """, [id])
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    
    conn = sqlite3.connect('libreria_sql.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS libreria;')

    c.execute("""
                CREATE TABLE libreria (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [title] TEXT NOT NULL,
                [pags] INTEGER,
                [author] TEXT );
                """)
    
    with open('libreria.csv', 'r', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
    
        for row in reader:
            copy_title = row['titulo']
            copy_pags = row['cantidad_paginas']
            copy_author = row['autor']

            c.execute("""
                    INSERT INTO libreria (title, pags, author)
                    VALUES (?,?,?);
                    """, [copy_title, copy_pags, copy_author])
    
    conn.commit()
    conn.close()
    
    while True:
        function = float(input("""Comente que funcion quiere realizar:
            1 -> imprimir en pantalla filas de su base de datos
            2 -> retornar el nombre del autor que pertenece al título del libro
            3 -> modifquar el título de un libro según el "id"
            4 -> borrar libros que ya no se venden en la librería por nombre del libro
            0 -> finalizar operaciones
            """))
        
        if function == 0:
            break
        
        elif function == 1:
            id = int(input('Ingrese "id" que quiere visualizar (0 para ver todo)\n\t'))

            if id < 0:
                print('Error')
                continue

            fetch(id)

            input('Enter para continuar')

        elif function == 2:
            book_title = str(input('Ingrese Titulo del Libro:\n\t'))

            author = search_author(book_title)

            print(author)
            
            input('Enter para continuar')

        elif function == 3:
            id = int(input('Ingrese "id" de libro que quiere modificar\n\t'))
            new_title = str(input('Ingrese nuevo titulo del libro a modificar\n\t'))

            update(new_title,id)

            input('Enter para continuar')

        elif function == 4:
            id = int(input('Ingrese "id" de libro que quiere borrar\n\t'))
            
            delete(id)

            input('Enter para continuar')
        
        else:
            print('Warning!!!\n\tFuncion desconocida.')
            input('Enter para continuar')