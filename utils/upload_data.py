import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

csv_path = "project_development/dataset/created/df_view.csv"

load_dotenv()
db_url = os.getenv('DB_URL')
engine = create_engine(db_url)

# Verifica se a tabela já existe e tem dados
from sqlalchemy import inspect
inspector = inspect(engine)

if inspector.has_table("flights"):
    # Conta registros existentes
    existing_count = pd.read_sql("SELECT COUNT(*) as count FROM flights", engine).iloc[0]['count']
    print(f"⚠️  Tabela já existe com {existing_count} registros")
    
    # Pergunta se quer substituir
    resposta = input("Deseja substituir os dados existentes? (s/n): ")
    if resposta.lower() == 's':
        chunksize = 50000
        reader = pd.read_csv(csv_path, chunksize=chunksize, encoding="ascii")
        
        # Substitui a tabela inteira
        for i, chunk in enumerate(reader):
            if i == 0:
                chunk.to_sql("flights", engine, if_exists="replace", index=False)
            else:
                chunk.to_sql("flights", engine, if_exists="append", index=False)
        print("✅ Dados carregados com sucesso!")
    else:
        print("Operação cancelada.")
else:
    # Tabela não existe, carga normal
    chunksize = 50000
    reader = pd.read_csv(csv_path, chunksize=chunksize, encoding="ascii")
    
    for chunk in reader:
        chunk.to_sql("flights", engine, if_exists="append", index=False)
    print("✅ Dados carregados com sucesso!")