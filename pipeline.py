import pandas as pd
import matplotlib.pyplot as plt

# 1. Extração: Ler o arquivo CSV
try:
    df = pd.read_csv('dados.csv')
    print("Dados lidos com sucesso.")
except FileNotFoundError:
    print("Erro: O arquivo 'dados.csv' não foi encontrado.")
    exit()

# 2. Transformação: Processar os dados
# Converter a coluna 'data' para o tipo datetime
df['data'] = pd.to_datetime(df['data'])
# Calcular o total de vendas
total_vendas = df['vendas'].sum()
print(f"O total de vendas é: {total_vendas}")

# 3. Geração: Criar e salvar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(df['data'], df['vendas'], marker='o', linestyle='-')
plt.title('Vendas Diárias')
plt.xlabel('Data')
plt.ylabel('Vendas')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar o gráfico como um arquivo de imagem
plt.savefig('grafico_vendas.png')
print("Gráfico 'grafico_vendas.png' gerado com sucesso!")