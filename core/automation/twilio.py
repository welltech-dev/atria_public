# Enviar mensagens aos clientes seja:
# Email;
# Sms.
 
# PASSO A PASSO

# Passo 1 -> vá até o site do twilio e crie uma conta e pegue o numero de telefone, eles liberam um crédito para teste.
# Passo 2 -> instale a biblioteca Twilio no seus ambiente virtual desejado.
# Passo 3 -> importe esta biblioteca para dentro do seu script.



from twilio.rest import Client  # para que fique mais profissional account_sid e auth_token deve ser integrado ao código como variável ambient.

# Passo 4 -> insira o seu id_account twilio
account_sid="seu_sid"

# Passo 5 -> insira o token de autenticação criado no site
auth_token="seu_token"

# Passo 6 -> crie uma variável de ambiente
cliente = Client(account_sid, auth_token) # com esta variável o script faz a conexão a sua conta no twilio

# passo 9 -> crie uma variável para adicionar a mensagem antes da função de enviar
avisoImportante = 'aqui eu posso incluir qualquer infomação'

# Passo 7 -> crie uma nova mensagem
mensagem = cliente.messages.create(
    #passar os parâmentros de envio, como o telefone que vai receber, o que vai enviar e a msg que vai ser enviada."
    from_='número de tefone',
    to='número de telefone',
    #Além de enviar mensagem simples de sms, pode conter uma variável dentro dela se caso necessite fazendo no seguinte:
    body=f'mensagem enviada terá uma variável especifica agora {avisoImportante}, eu posso criar uma função: para avisar o cliente sobre a situação da compra dele'
)   # cria uma nova mensagem e te volta como respostas as infos da mensagem enviada. 
# Passo 8 -> é necessário para você acompanhar o andamento do envio.
print(mensagem.body)    # aparece o sms e o numero que recebeu a mensagem

