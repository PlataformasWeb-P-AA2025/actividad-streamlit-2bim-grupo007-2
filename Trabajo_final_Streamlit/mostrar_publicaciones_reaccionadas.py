import streamlit as st
from sqlalchemy.orm import sessionmaker
from db import get_session
from genera_data import Usuario

st.set_page_config(page_title="Reacciones del Usuario", layout="wide")

# ----------------------------- #
# Consulta: Publicaciones en las que reaccionó un usuario
# ----------------------------- #

st.header("Publicaciones en las que un usuario reaccionó")

# Entrada de nombre del usuario
nombre_usuario = st.text_input("Escriba el nombre del usuario que desea consultar:")

# Botón para activar la búsqueda
if st.button("Buscar publicaciones con reacciones"):
    session = get_session()

    # se hace una consulta para saber si el usuario existe en la base de datos
    usuario = session.query(Usuario).filter_by(usuarioNombre=nombre_usuario).first()

    if usuario:
        st.success(f"Publicaciones en las que reaccionó {usuario.usuarioNombre}:")

        # comprobar si el usuario tiene reacciones
        if usuario.reacciones:
            # Iteramos cada reaccion del usuario
            datos = []
            for reaccion in usuario.reacciones:
                # obtener la publicacion a la que reaccionó
                pub = reaccion.publicacion
                fila = {
                    "ID Publicación": pub.id,
                    "Contenido": pub.publicacion[:50] + "..." if len(pub.publicacion) > 50 else pub.publicacion,
                    "Tipo de Reacción": reaccion.tipo_emocion,
                    "Comentario": reaccion.comentario if reaccion.comentario else "Sin comentario"
                }
                datos.append(fila)

            st.subheader("Resultados:")
            st.table(datos)
        else:
            # mensaje en caso de que el usuario no tenga reacciones
            st.warning("Este usuario no ha reaccionado a ninguna publicación.")
    else:
        # si el usuario no se encontró 
        st.error("Usuario no encontrado.")

    session.close()
