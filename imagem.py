import streamlit as st
from streamlit_camera_input_live import camera_input_live
import requests
import base64

def describe_image(image_bytes, api_key):
    url = "https://api.groq.com/v1/model/inference"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # Convert image bytes to base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    data = {
        "prompt": "Descreva a imagem fornecida.",
        "image": image_base64,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("description", "Não foi possível obter uma descrição.")
    else:
        return f"Erro na solicitação: {response.status_code}"

def ask_about_image(question, api_key):
    url = "https://api.groq.com/v1/model/inference"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": question,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("answer", "Desculpe, não consegui responder à pergunta.")
    else:
        return f"Erro na solicitação: {response.status_code}"

# Chave de API da Groq
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

st.title("Converse sobre o que vê pela câmera")
st.write("Capture uma imagem e faça perguntas sobre ela!")

# Capturar a imagem da câmera
image = camera_input_live()

if image is not None:
    st.image(image, caption="Imagem capturada", use_column_width=True)
    
    # Descrever a imagem
    image_bytes = image.getvalue()  # Obtém os bytes da imagem
    description = describe_image(image_bytes, GROQ_API_KEY)
    
    st.write(f"Descrição: {description}")
    
    # Permitir que o usuário faça perguntas sobre a imagem
    user_question = st.text_input("Faça uma pergunta sobre a imagem:")
    
    if user_question:
        answer = ask_about_image(user_question, GROQ_API_KEY)
        st.write(f"Resposta: {answer}")
