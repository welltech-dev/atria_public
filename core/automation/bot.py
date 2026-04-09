# import de bibliotecas

import streamlit as st
from openai import OpenAI
from logger import salvar_conversa

from serve import carregar_perfil_usuario

user_id = ""  # vem obriga
perfil = carregar_perfil_usuario(user_id)

login_usuario = perfil["login"]  # SEM fallback


modelo = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title('Primeza Segura - ChatBot com IA')

if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = [
        {
            "role": "system",
            "content": """
                Você é o bot_Primeza, assistente do sistema Primeza Segura.

                Regras:
                - Quando a mensagem envolver dados bancários, responda em JSON estruturado.
                - Quando for conversa normal, responda em texto.
                - Nunca invente dados financeiros.
                - Sempre aguarde confirmação antes de executar operações sensíveis.

                Formato JSON padrão:
                {
                "tipo": "consulta | operacao | erro",
                "descricao": "...",
                "dados": {}
                }
            """
        }
    ]


for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    st.chat_message(role).write(content)

mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")

if mensagem_usuario:
    st.chat_message("user").write(mensagem_usuario)
    mensagem = {"role": "user", "content": mensagem_usuario}
    st.session_state["lista_mensagens"].append({mensagem})

    salvar_conversa(login_usuario, "user", mensagem_usuario)

    # resposta da IA
    resposta_modelo = modelo.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="gpt-4o"
    )

    resposta_ia = resposta_modelo.choices[0].message.content

    # exibir a resposta da IA na tela
    st.chat_message("assistant").write(resposta_ia)
    mensagem_ia = {"role": "assistant", "content": resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem_ia)

'''
 criar chatbot : okay

 integrar server.py: okay

 injetar cadastro no system: okay

 salvar conversa no CSV: okay

 regras por plano/nível: okay
 '''


# Criar rota para o chatbot no server

'''@app.route("/api/chat", methods=["POST"])
def chat():
    mensagem = request.json["mensagem"]
    resposta = bot_primeza(mensagem)
    return jsonify({"resposta": resposta})'''