## Pipeline de Análise de Dados com Python, Jenkins e GitHub
Este projeto automatiza a análise e visualização de dados. Sempre que houver uma atualização no repositório, o Jenkins irá processar os dados e gerar um novo relatório visual.

# Passo 1: Preparar o Projeto Local
Crie a seguinte estrutura de arquivos em um diretório local.
````
data-pipeline-jenkins/
├── pipeline.py
├── dados.csv
├── requirements.txt
└── .gitignore
````
`requirements.txt:` Lista as bibliotecas Python necessárias.
````
pandas==2.2.2
matplotlib==3.8.4
````
`dados.csv:` O arquivo com os dados de exemplo.

````Snippet de código

data,vendas
2024-01-01,150
2024-01-02,180
... (adicione mais dados) ...
````
`pipeline.py:` O script Python para processar os dados e gerar o gráfico.

````Python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('dados.csv')
df['data'] = pd.to_datetime(df['data'])
total_vendas = df['vendas'].sum()
print(f"O total de vendas é: {total_vendas}")

plt.figure(figsize=(10, 6))
plt.plot(df['data'], df['vendas'], marker='o')
plt.title('Vendas Diárias')
plt.xlabel('Data')
plt.ylabel('Vendas')
plt.savefig('grafico_vendas.png')
print("Gráfico 'grafico_vendas.png' gerado com sucesso!")
````
`.gitignore:` Impede que arquivos desnecessários sejam enviados ao GitHub.
````
venv/
__pycache__/
*.pyc
grafico_vendas.png
````
# Passo 2: Configurar o Repositório no GitHub
Crie um novo repositório no GitHub (ex: `data-pipeline-jenkins`).

Faça o `git init` no seu diretório local, adicione os arquivos, faça um `commit` e o `push` para o repositório no GitHub.

# Passo 3: Conectar o Jenkins ao GitHub (sem provedor de nuvem)
Se seu Jenkins está rodando localmente (sem um endereço público), use o ngrok.

- Instale o ngrok no seu servidor Ubuntu: `sudo snap install ngrok`.

- Autentique o ngrok com seu token pessoal: `ngrok config add-authtoken <SEU_TOKEN>`.

- Inicie o túnel para a porta do Jenkins: `ngrok http 8082`.

- Copie a URL `https://...ngrok.io` que o ngrok exibir.

- No GitHub, vá em Settings > Webhooks > Add webhook.

- No campo `Payload` URL, cole a URL do ngrok e adicione `/github-webhook/` no final. Exemplo: `https://abcd1234.ngrok-free.app/github-webhook/`.

- Deixe o Content type como `application/json`.

- Marque a opção Just the push event e clique em Add webhook.

# Passo 4: Criar o Job no Jenkins

- No painel do Jenkins, clique em `New Item`.

- Dê um nome ao job (ex: `pipeline-analise-dados`) e selecione `Freestyle project`.

- Em `Source Code Management`, selecione `Git` e adicione a URL do seu repositório.

- Em `Triggers`, marque `GitHub hook trigger for GITScm polling`.

- Em `Build Steps`, clique em `Add build step` e selecione `Execute shell`.

- Adicione os comandos para instalar as dependências e executar o script.

````Bash
python3 -m pip install -r requirements.txt
python3 pipeline.py
````
- Em `Post-build Actions`, clique em `Add post-build action` e selecione `Archive the artifacts`.

- No campo `Files to archive`, digite `grafico_vendas.png` para salvar a imagem gerada.

- Clique em `Save`.

# Passo 5: Executar e Verificar o Pipeline

- Faça um pequeno `commit` e `push` para o seu repositório no GitHub.

- O webhook irá acionar o Jenkins, que iniciará o build.

- Na página do job no Jenkins, você verá o log de execução. Se tudo estiver correto, o build terá o status `SUCCESS`.

- Na página do build, procure por "Artefatos da construção" para ver e baixar o `grafico_vendas.png`.
