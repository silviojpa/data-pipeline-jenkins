Passo a Passo: Pipeline de Análise de Dados com Python, Jenkins e GitHub
Este guia detalhado explica como configurar um pipeline de CI/CD para automatizar a análise e visualização de dados. Sempre que você atualizar o código ou os dados no seu repositório GitHub, o Jenkins irá processar tudo e gerar um novo gráfico automaticamente.

Passo 1: Preparar o Projeto Local
Comece criando a seguinte estrutura de arquivos em um diretório no seu computador.

data-pipeline-jenkins/
├── pipeline.py
├── dados.csv
├── requirements.txt
└── .gitignore

requirements.txt: Este arquivo lista as bibliotecas Python que precisam ser instaladas.

pandas==2.2.2
matplotlib==3.8.4

dados.csv: Um arquivo de dados simples para o projeto.

data,vendas
2024-01-01,150
2024-01-02,180
2024-01-03,200
2024-01-04,165
2024-01-05,210

pipeline.py: O script Python que realiza a análise e cria o gráfico.

import pandas as pd
import matplotlib.pyplot as plt

# Lê os dados do arquivo CSV
print("Dados lidos com sucesso.")
df = pd.read_csv('dados.csv')

# Converte a coluna 'data' para o formato de data
df['data'] = pd.to_datetime(df['data'])

# Calcula o total de vendas
total_vendas = df['vendas'].sum()
print(f"O total de vendas é: {total_vendas}")

# Cria o gráfico de linha das vendas
plt.figure(figsize=(10, 6))
plt.plot(df['data'], df['vendas'], marker='o')
plt.title('Vendas Diárias')
plt.xlabel('Data')
plt.ylabel('Vendas')
plt.grid(True)
plt.tight_layout()

# Salva o gráfico como um arquivo PNG
plt.savefig('grafico_vendas.png')
print("Gráfico 'grafico_vendas.png' gerado com sucesso!")

.gitignore: Impede que arquivos temporários e o gráfico gerado sejam enviados ao GitHub.

venv/
__pycache__/
*.pyc
grafico_vendas.png

Passo 2: Configurar o Repositório no GitHub
Crie um novo repositório no GitHub (exemplo: data-pipeline-jenkins).

Inicie um repositório Git localmente (git init), adicione os arquivos (git add .), faça o primeiro commit (git commit -m "primeiro commit") e suba para o GitHub (git push).

Passo 3: Conectar o Jenkins ao GitHub (usando ngrok)
Se seu Jenkins está rodando em uma máquina local, você precisa usar o ngrok para que o GitHub possa se comunicar com ele.

Instale o ngrok no seu servidor Ubuntu (onde o Jenkins está):

sudo snap install ngrok

Autentique o ngrok:
Acesse o painel do ngrok, copie seu token pessoal e execute o comando:

ngrok config add-authtoken <SEU_TOKEN_AQUI>

Inicie o túnel ngrok:
Execute o comando para criar um túnel para a porta do Jenkins (8082):

ngrok http 8082

Copie a URL https://...ngrok.io que será exibida.

Configure o Webhook no GitHub:

No seu repositório, vá em Settings (Configurações) > Webhooks.

Clique em Add webhook (Adicionar webhook).

No campo Payload URL, cole a URL do ngrok e adicione /github-webhook/ no final. O endereço completo ficará assim: https://abcd1234.ngrok-free.app/github-webhook/.

Deixe o Content type como application/json.

Marque a opção Just the push event (Apenas o evento push) e clique em Add webhook.

Passo 4: Criar o Job no Jenkins
No painel do Jenkins, clique em New Item (Novo Item).

Dê um nome ao job (exemplo: pipeline-analise-dados) e selecione Freestyle project.

Em Source Code Management (Gerenciamento de Código Fonte), selecione Git e adicione a URL do seu repositório GitHub.

Em Build Triggers (Gatilhos de Construção), marque GitHub hook trigger for GITScm polling.

Em Build Steps (Passos de Construção), clique em Add build step e selecione Execute shell (Executar shell).

Adicione os comandos para instalar as dependências e executar o script Python.

python3 -m pip install -r requirements.txt
python3 pipeline.py

Em Post-build Actions (Ações de pós-construção), clique em Add post-build action e selecione Archive the artifacts (Arquivar os artefatos).

No campo Files to archive (Arquivos para arquivar), digite grafico_vendas.png.

Clique em Save (Salvar).

Passo 5: Executar e Verificar o Pipeline
Faça uma pequena alteração em um dos seus arquivos (por exemplo, adicione uma nova linha no dados.csv).

Faça o git commit e git push para o GitHub.

O webhook irá acionar o Jenkins, que iniciará um novo build automaticamente.

Na página do seu job, procure a seção "Artefatos da construção". O arquivo grafico_vendas.png estará disponível para visualização e download.
