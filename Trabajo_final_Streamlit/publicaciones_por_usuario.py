import streamlit as st
from sqlalchemy.orm import sessionmaker
from db import get_session
from genera_data import Usuario

st.set_page_config(page_title="Publicaciones de Usuario", layout="wide")

# ----------------------------- #
# Consulta: Publicaciones por Usuario
# ----------------------------- #

st.header("Publicaciones hechas por un Usuario")

# Entrada de nombre del usuario
nombre_usuario = st.text_input("Escriba el nombre del usuario que desea consultar:")

# Botón para activar la búsqueda
if st.button("Buscar publicaciones"):
    session = get_session()
    
    usuario = session.query(Usuario).filter_by(usuarioNombre=nombre_usuario).first()

    if usuario:
        st.success(f"Usuario encontrado: {usuario.usuarioNombre}")
        
        if usuario.publicaciones:
            st.subheader("Publicaciones:")
            filas = [{"ID Publicación": p.id, "Contenido": p.publicacion} for p in usuario.publicaciones]
            st.table(filas)
        else:
            st.warning("⚠El usuario no tiene publicaciones hasta el momento.")
    else:
        st.error("Usuario no existe en la base de datos.")
    
    session.close()
