import streamlit as st
from db import get_session

# Importa las clases que definiste en genera_data.py
from genera_data import Usuario, Publicacion, Reaccion

# Se importa el operador and
from sqlalchemy import and_, func

import pandas as pd

# ----------------------- #
# 5 consultas adicionales #
# ----------------------- #

st.set_page_config(page_title="Consultas Adicionales", layout="wide")

# Usuarios que reaccionaron a sus propias publicaciones

# Se unen las tablas Usuario, Publicacion y Reaccion
# el filter comprueba que el usuario_id de la reaccion sea igual al id
# del usuario que hizo la publicacion

def usuarios_egocentricos():

	st.header("Usuarios que reaccionaron a sus propias publicaciones")
	session = get_session()
	usuarios_egocentricos = session.query(Usuario).join(Publicacion).join(Reaccion).filter(Reaccion.usuario_id == Usuario.id).order_by(Reaccion.usuario_id).all()

	if not usuarios_egocentricos:
		st.info("No hay usuarios")
		session.close()
		return

	for u in usuarios_egocentricos: 
		with st.expander(f"ID {u.id} → {u.usuarioNombre}", expanded=False):
        	# Mostrar atributos básicos
			st.write(f"**ID:** {u.id}")
			st.write(f"**Nombre Usuario:** {u.usuarioNombre}")

        	# Si el usuario tiene publicaciones relacionadas, listarlas
			if u.publicaciones:
				st.write("**Publicaciones asociadas:**")
				# Usamos st.table para mostrar una tabla sencilla con el id y publicacion
				filas = []
				for c in u.publicaciones:
					filas.append({
                    	"Publicacion ID": c.id,
                    	"Publicacion": c.publicacion,
                    	"Nro. Reacciones": len(c.reacciones)
                	})
					st.table(filas)
			else:
				st.write("_No hay publicaciones asociadas a este usuario._")
	session.close()

# Emociones mas comunes por usuario
# Primero defino lo que quiero recuperar, el nombre del usuario,
# el tipo de emocion, y el conteo de esta emocion.
# Con ayuda de func, cuento por usuario cada reaccion que tuvo.
# Para que se entienda mejor, agrupo primero los estudiantes y sus reacciones
# y luego dentro de esta agrupacion, cuento las veces que uso cada emocion
def emociones_usuarios():

	st.header("Emociones mas comunes por usuario")
	session = get_session()
	emociones_usuarios = session.query(Usuario.usuarioNombre, 
									Reaccion.tipo_emocion,
									func.count(Reaccion.tipo_emocion).label('conteo')).\
						join(Reaccion).\
						group_by(Usuario.id, Reaccion.tipo_emocion,).\
						order_by(Usuario.usuarioNombre, func.count(Reaccion.tipo_emocion).desc()).all()
	
	if not emociones_usuarios:
		st.info("No hay emociones")
		session.close()
		return

	# Agrupar resultados por usuario
	datos_agrupados = {}

	# Lo que hago es agrupar las emociones por usuarios en un diccionario
	# Luego imprimo el streamlit el expander y la tabla hecha con pandas
	# (st.dataframe)
	for usuario, emocion, conteo in emociones_usuarios:
		if usuario not in datos_agrupados:
			datos_agrupados[usuario] = []
		datos_agrupados[usuario].append({"Tipo de emoción": emocion, "Conteo": conteo})

	# Mostrar resultados organizados
	for usuario, emociones in datos_agrupados.items():
		with st.expander(f"Nombre Usuario: {usuario}", expanded=False):
			df = pd.DataFrame(emociones)
			st.dataframe(df, use_container_width=True)
	session.close()

# Usuarios sin publicaciones pero con reacciones
# Primero especifico que solo quiero el usuario
# luego el outerjoin me ayuda a unir con publicaciones
# asi no existan. Despues se ve que el usuario tenga al menos 
# una reaccion con ayuda del join. Finalmente se filtran 
# a los que no tienen publicacion
def usuarios_reaccionadores():

	st.header("Usuarios sin publicaciones pero con reacciones")
	session = get_session()
	usuarios_reaccionadores = session.query(Usuario).\
						outerjoin(Publicacion).\
						join(Reaccion).\
						filter(Publicacion.id == None).all()

	if not usuarios_reaccionadores:
		st.info("No hay usuarios que hayan reaccionado y no pulicado")
		session.close()
		return

	for u in usuarios_reaccionadores: 
		with st.expander(f"ID {u.id} → {u.usuarioNombre}", expanded=False):
        	# Mostrar atributos básicos
			st.write(f"**ID:** {u.id}")
			st.write(f"**Nombre Usuario:** {u.usuarioNombre}")

        	# Si el usuario tiene reacciones relacionadas, listarlas
			if u.reacciones:
				st.write("**Reacciones asociadas:**")
				# Usamos st.table para mostrar una tabla sencilla con el id y publicacion
				filas = []
				for c in u.reacciones:
					filas.append({
                    	"Reaccion ID": c.id,
                    	"Tipo emocion": c.tipo_emocion,
                    	"Publicacion a la que reacciono": c.comentario
                	})
					st.table(filas)
			else:
				st.write("_No hay reacciones asociadas a este usuario._")
	session.close()

# Publicaciones con mas reacciones
# Especifico que solo quiero la Publicacion junto a el numero de reacciones
# el outer me ayuda a tener en cuenta hasta aquellas publicaciones sin
# reacciones. Se cuentan las reacciones de cada publicacion, se agrupan y se ordenan
def publicaciones_top():

	st.header("Publicaciones con mas reacciones")
	session = get_session()
	publicaciones_top = session.query(
								Publicacion,
								func.count(Reaccion.id).label("num_reacciones")
							).outerjoin(Reaccion).\
							group_by(Publicacion.id).\
							order_by(func.count(Reaccion.id).desc()).all()

	if not publicaciones_top:
		st.info("No hay usuarios que hayan reaccionado y no pulicado")
		session.close()
		return

	for u in publicaciones_top: 
		with st.expander(f"ID {u.Publicacion.id} → {u.Publicacion.publicacion}", expanded=False):
        	# Mostrar atributos básicos
			st.write(f"**ID:** {u.Publicacion.id}")
			st.write(f"**Publicacion:** {u.Publicacion.publicacion}")
			st.write(f"**Publicacion hecha por:** {u.Publicacion.usuario.usuarioNombre}")
			st.write(f"**Numero de reacciones:** {u.num_reacciones}")

	session.close()

# Usuarios sin ninguna reaccion ni publicacion
# Como en los anteriores, hago un outerjoin para considerar aquellos que no estan
# en la tabla, y luego filtro sus id
def usuarios_fantasmas():

	st.header("Usuarios sin ninguna reaccion ni publicacion")
	session = get_session()
	usuarios_fantasmas = session.query(Usuario).\
						outerjoin(Publicacion).\
						outerjoin(Reaccion).\
						filter(
							and_(
									Publicacion.id == None, 
									Reaccion.id == None
								)
						).all()

	if not usuarios_fantasmas:
		st.info("No hay usuarios que no hayan reaccionado ni pulicado")
		session.close()
		return

	for u in usuarios_fantasmas: 
		with st.expander(f"ID {u.id} → {u.usuarioNombre}", expanded=False):
        	# Mostrar atributos básicos
			st.write(f"**ID:** {u.id}")
			st.write(f"**Nombre Usuario:** {u.usuarioNombre}")
			st.write(f"El usuario {u.usuarioNombre} no tiene ninguna publicacion o reaccion")

	session.close()

def main():
    st.title("Explorador de objetos SQLAlchemy en Streamlit")

    entidad = st.sidebar.selectbox(
        "Elija la consulta que quiere visualizar:",
        (
            "1",
            "2",
            "3",
            "4",
            "5"
        ),
    )

    if entidad == "1":
        usuarios_egocentricos()
    if entidad == "2":
        emociones_usuarios()
    if entidad == "3":
        usuarios_reaccionadores()
    if entidad == "4":
        publicaciones_top()
    if entidad == "5":
        usuarios_fantasmas()


if __name__ == "__main__":
    main()
