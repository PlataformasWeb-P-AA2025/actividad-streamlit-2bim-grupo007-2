from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del
# archivo genera_tablas
from genera_data import Usuario, Publicacion, Reaccion

# se importa información del archivo configuracion
from configuracion import cadena_base_datos

import pandas as pd

# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# ------------------ #
# INGRESAR USUARIOS  #
# ------------------ #

# Ruta usuarios 
# /home/nahomi/Downloads/Proyecto-Final-B1/trabjo-final-1bim-grupo-007/DATA/usuarios_red_x.csv
# Leo el csv con la informacion de usuario
usuarios_csv = pd.read_csv("DATA/usuarios_red_x.csv")

# print(usuarios_csv.usuario)

# Ingresar datos usuario, con ayuda de un ciclo for
# como es una sola columna entonces no es necesario trabajar con 
# iterrows, solo puedo llamar como a esa columna para crear el 
# objeto tipo usuario, y agregarlo para enviarlo a la BD

for u in usuarios_csv.usuario:
        usuario = Usuario(
                usuarioNombre = u
                )

        session.add(usuario)
        print(usuario)


# --------------------- #
# INGRESAR PUBLICACION  #
# --------------------- #

# Ruta publicaciones 
# /home/nahomi/Downloads/Proyecto-Final-B1/trabjo-final-1bim-grupo-007/DATA/usuarios_publicaciones.csv
# Leo el csv de publicaciones
publicaciones_csv = pd.read_csv("DATA/usuarios_publicaciones.csv", delimiter='|')

# Recupero todos los datos de la tabla de Usuarios
usuarios_db = session.query(Usuario).all()

# print(usuarios_db)

# Lo que hago en este for es primero utilizar el iterrow 
# para recorrer cada fila del dataframe, como aqui si hay 
# dos columnas entonces no puedo trabajar sin el. 
# Luego de eso recorro todos los usuarios recuperados
# de la BD, y esto lo hago para poder iterrelacionar de forma
# correcta el usuario que se lee del csv con el recuperado de la BD.
# Asi evito incogruencias, y de paso me evito crear el objeto usuario
# desde cero.

for index, row in publicaciones_csv.iterrows():
        # row[0] es el usuario, row [1] es la publicacion
        for e in usuarios_db:
                if (row[0] == e.usuarioNombre):
                        # print(f"Son iguales {row[0]} con {e.usuarioNombre}")
                        publicacion = Publicacion(
                                        publicacion = row[1],
                                        usuario = e
                                )
                        print(f"Objeto creado {publicacion}")
                        session.add(publicacion)
                        break


# ---------------- #
# INGRESAR EMOCION #
# ---------------- #

# Ruta publicaciones 
# /home/nahomi/Downloads/Proyecto-Final-B1/trabjo-final-1bim-grupo-007/DATA/usuarios_publicaciones.csv
# Leo el csv de publicaciones
emociones_csv = pd.read_csv("DATA/usuario_publicacion_emocion.csv", delimiter='|')

# Recupero todos los datos de la tabla de Publicacion
publicacion_db = session.query(Publicacion).all()

# lista = [] # Esto solo era para comprobar

for index, row in emociones_csv.iterrows():
        # print(row['Usuario'], row['comentario'], row['tipo emocion'])

        # Asi como en publicacion, busco en todos los usuarios ya registrados
        # en la BD con ayuda de un ciclo for, y guardo en una variable el objeto
        for e in usuarios_db:
                if (row['Usuario'] == e.usuarioNombre):
                        # print(f"Son iguales {row[0]} con {e.usuarioNombre}")
                        usuarioEncontrado = e
                        # print(usuarioEncontrado)
                        break

        # Hago lo mismo con publicacion, busco y cuando encuentro la coincidencia
        # guardo en una variable el objeto
        for e in publicacion_db:
                if (row['comentario'] == e.publicacion):
                        # print(f"Son iguales {row[0]} con {e.publicacion}")
                        publicacionEncontrada = e
                        # print(publicacionEncontrada)
                        break

        # Creo el objeto tipo Reaccion y lo inicializo con las variables 
        # del csv y las enocontradas 
        reaccion = Reaccion(
                        tipo_emocion = row['tipo emocion'],
                        comentario = row['comentario'],
                        usuario = usuarioEncontrado,
                        publicacion = publicacionEncontrada
                )

        # print(f"Objeto creado {reaccion}")
        # lista.append(reaccion)

        session.add(reaccion)

# print(len(lista))

session.commit()