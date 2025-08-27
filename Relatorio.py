import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="K4u4n+1706", 
    database="covid19_db"
)
cursor = conn.cursor()

print("="*60)
print("RELATÓRIO COVID-19 POR CIDADE")
print("="*60)

#  Todos os casos de morte por cidade
print("\n🕱 Casos de morte por cidade:")
cursor.execute("""
    SELECT city, SUM(deaths) as total_mortes
    FROM DadosCovid
    GROUP BY city
    ORDER BY total_mortes DESC;
""")
for city, deaths in cursor.fetchall():
    print(f"- {city}: {deaths} mortes")

#  População estimada antes e depois dos casos
print("\n População estimada antes e depois dos casos:")
cursor.execute("""
    SELECT city,
           MAX(estimated_population) as populacao,
           SUM(confirmed) as total_confirmados
    FROM DadosCovid
    GROUP BY city;
""")
for city, pop, confirmed in cursor.fetchall():
    pop_depois = pop - confirmed
    print(f"- {city}: Antes = {pop}, Depois = {pop_depois}")

#  Maior cidade em quantidade de casos confirmados
cursor.execute("""
    SELECT city, SUM(confirmed) as total_confirmados
    FROM DadosCovid
    GROUP BY city
    ORDER BY total_confirmados DESC
    LIMIT 1;
""")
maior = cursor.fetchone()
print("\n Maior cidade em casos confirmados:")
print(f"- {maior[0]} com {maior[1]} casos")

# Menor cidade em quantidade de casos confirmados
cursor.execute("""
    SELECT city, SUM(confirmed) as total_confirmados
    FROM DadosCovid
    GROUP BY city
    ORDER BY total_confirmados ASC
    LIMIT 1;
""")
menor = cursor.fetchone()
print("\n Menor cidade em casos confirmados:")
print(f"- {menor[0]} com {menor[1]} casos")

print("\nRelatório gerado com sucesso!")

cursor.close()
conn.close()