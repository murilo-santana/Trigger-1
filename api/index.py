from flask import Flask
import requests
import os

app = Flask(__name__)

# Pega o token do ambiente
TOKEN = os.getenv("GH_TOKEN_5min")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Lista de workflows a serem acionados (Ajustado para 'workflow' no singular para o loop funcionar)
WORKFLOWS = [
    {"repo": "QueueListLog", "workflow": "queuelistsp5.yaml"},
    {"repo": "packed_sp5", "workflow": "main_base_to_packed.yaml"},
    {"repo": "BasePending", "workflow": "main_expedicao.yaml"},
    {"repo": "Base_Handedover", "workflow": "main_expedicao.yaml"},
    {"repo": "Base_3PL", "workflow": "main_expedicao.yaml"},
    {"repo": "Base_Packed_FerramentaFIFO", "workflow" : "main_base_to_packed.yaml"},
    {"repo": "Queuelist", "workflow" : "queue_list_sp5.yml"},
    {"repo": "base_inbound", "workflow" : "main_inbound.yaml"},
    {"repo": "Base-ended", "workflow" : "main_ended.yaml"},
    {"repo": "piso_exp", "workflow" : "piso10.yaml"},
]

# Rota principal para verificar se o app está no ar
@app.route('/')
def home():
    return "Servidor do agendador de workflows do GitHub está no ar."

# Rota que será chamada pelo Cron Job da Vercel
@app.route('/api/trigger')
def trigger_workflows():
    # Loop que executa a lógica UMA VEZ por chamada
    for wf in WORKFLOWS:
        # ALTERAÇÃO: Usuário atualizado para murilo-santana
        url = f"https://api.github.com/repos/murilo-santana/{wf['repo']}/actions/workflows/{wf['workflow']}/dispatches"
        data = {"ref": "main"}
        try:
            res = requests.post(url, headers=HEADERS, json=data)
            print(f"[OK] {wf['workflow']} -> {res.status_code}")
        except Exception as e:
            print(f"[ERRO] {wf['workflow']} -> {e}")
    
    return "Workflows acionados com sucesso!", 200
