import streamlit as st
from sqlalchemy.orm import sessionmaker
from db import get_session
from genera_data import Usuario

st.set_page_config(page_title="Reacciones por Usuario", layout="wide")

# ----------------------------- #
# Consulta: Reacciones a publicaciones por Usuario
# ----------------------------- #

st.header("Reacciones a las publicaciones de un Usuario")

# Entrada de nombre del usuario
nombre_usuario = st.text_input("Escriba el nombre del usuario que desea consultar:")

# Botón para activar la búsqueda
if st.button("Buscar reacciones"):
    session = get_session()
    
    # se hace una consulta para saber si el usuario existe en la base de datos
    usuario = session.query(Usuario).filter_by(usuarioNombre=nombre_usuario).first()

    if usuario: # Verificar si el usuario tiene publicaciones
        st.success(f"Reacciones a las publicaciones de {usuario.usuarioNombre}:")

        if usuario.publicaciones:
            # recorrer cada publicación del usuario
            for publicacion in usuario.publicaciones:
                st.markdown(f"**Publicación:** {publicacion.publicacion}")
                
                # verificar si la publicación tiene reacciones
                if publicacion.reacciones:
                    reacciones = [{"Emoción": reaccion.tipo_emocion} for reaccion in publicacion.reacciones]
                    st.table(reacciones)
                else:
                    # si no tiene reacciones imprime lo siguiente
                    st.write("No tiene reacciones")
        else:
            # si no tiene publicaciones el usuario imprime lo siguiente
            st.warning("El usuario no tiene publicaciones.")
    else:
        # si no existe el usuario
        st.error("Usuario no encontrado.")
    
    session.close()
