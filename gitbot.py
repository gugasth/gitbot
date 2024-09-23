import requests
import smtplib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
from email.mime.text import MIMEText
from dotenv import load_dotenv



# Função para listar todos os repositórios do usuário
def listar_repositorios(usuario, token=None):
    url = f"https://api.github.com/users/{usuario}/repos"
    headers = {'Authorization': f'token {token}'} if token else {}
    params = {'visibility': 'all'}  
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        repos = response.json()
        return [repo['name'] for repo in repos]
    else:
        print(f"Erro ao buscar repositórios: {response.status_code}")
        return []

# Função para verificar se houve commits em um repositório específico
def verificar_commits(usuario, repositorio, token=None):
    url = f"https://api.github.com/repos/{usuario}/{repositorio}/commits"
    headers = {'Authorization': f'token {token}'} if token else {}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        hoje = datetime.now().date()
        for commit in commits:
            data_commit = commit['commit']['author']['date'][:10]
            data_commit = datetime.strptime(data_commit, '%Y-%m-%d').date()
            if data_commit == hoje:
                return True  # Houve commit hoje
    return False  # Não houve commit hoje

# Função para enviar o e-mail de notificação
def enviar_email(destinatario, assunto, mensagem):
    message = Mail(
        from_email='gustavopaulo-guga@hotmail.com',
        to_emails=destinatario,
        subject=assunto,
        plain_text_content=mensagem
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)  
        print(response.body)          
        print(response.headers)      
    except Exception as e:
        print(str(e))

# Fluxo principal
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lê a chave API do SendGrid
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
token = os.getenv('GITHUB_TOKEN')

usuario = "gugasth"
repositorios = listar_repositorios(usuario, token)

# Verificar se houve commit em qualquer repositório
commit_realizado = any(verificar_commits(usuario, repo, token) for repo in repositorios)

if not commit_realizado:
    print('Commit não realizado.')
    enviar_email("gustavo.p07@aluno.ifsc.edu.br", "Alerta: Sem commits!", "Você não fez nenhum commit hoje.")
    print('Email enviado!')
else:
    print("Commit realizado em algum repositório.")
