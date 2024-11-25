
import streamlit as st
from groq import Groq

# ESTO ES NUEVO
st.set_page_config(page_title="gracias por visitarnos", page_icon="🐼")
# Título de la aplicación
st.title("bienvenidos/as")
#import streamlit as st

nombre = st.text_input("¿Cuál es tu nombre?")

# Botón para mostrar el saludo
if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! gracias por venir a Talento Tech.")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#MODELOS = ['modelo1', 'modelo2', 'modelo3']
def configurar_pagina():

    # Agregamos un título principal a nuestra página

    st.title("preguntame lo que sea")
    st.sidebar.title("cofiguracion de IA") # Creamos un sidebar con un título.
    elegirModelo =  st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

# modelo = configurar_pagina()

# mensaje = st.chat_input("Escribí tu mensaje:")

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
        return cliente.chat.completions.create(
    model=modelo,
    messages=[{"role": "user", "content": mensajeDeEntrada}],
    stream=True
)
clienteUsuario = crear_usuario_groq()

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        # inicializar_estado()

# Tomamos el mensaje del usuario por el input.
    # mensaje = st.chat_input("Escribí tu mensaje:")

# Verificamos que el mensaje no esté vacío antes de configurar el modelo
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})
    
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400,border=True)
    # Abrimos el contenedor del chat y mostramos el historial.
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()

    mensaje = st.chat_input("Escribí tu mensaje:")
    # print(mensaje)
    # Verifica que el mensaje no esté vacío antes de configurarel modelo
    area_chat()

    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")
        st.rerun()
if __name__ == "__main__":
    main()
