import pandas as pd 
import mysql.connector

# ===== 1. Ler o CSV =====
df = pd.read_csv(r"C:\Users\kauan\OneDrive\Área de Trabalho\DadosCovid19\teste.csv")

# Padronizar nomes das cidades
df['city'] = df['city'].astype(str).str.strip().str.title()

# Manter apenas registros de cidades (eliminar place_type != city)
df = df[df['place_type'] == 'city']

# Remover registros sem informações essenciais
df = df.dropna(subset=['city', 'city_ibge_code', 
                       'estimated_population', 
                       'last_available_confirmed', 
                       'last_available_deaths'])

df_relatorio = df[['city', 'city_ibge_code', 
                   'estimated_population', 
                   'last_available_confirmed', 
                   'last_available_deaths']].copy()

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="K4u4n+1706",
    database="Covid19_db"
)

cursor = con.cursor()

for _, row in df_relatorio.iterrows():
    cursor.execute("""
        INSERT INTO DadosCovid (city, city_ibge_code, estimated_population, confirmed, deaths)
VALUES (%s, %s, %s, %s, %s)
    """, (row['city'], row['city_ibge_code'], 
          row['estimated_population'], 
          row['last_available_confirmed'], 
          row['last_available_deaths']))

con.commit()
con.close()
print(f"{len(df_relatorio)} registros inseridos no banco.")
