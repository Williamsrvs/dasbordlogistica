import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np

banco_dados = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Q1k2v1y5@',
    'database': 'teste_db'
}

df = pd.read_excel('torre_controle.xlsx')
print(f"📊 {len(df)} linhas e {len(df.columns)} colunas carregadas")

def tipo_mysql(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    else:
        return "VARCHAR(255)"

def tratar_valor(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        return float(val)
    if hasattr(val, 'isoformat'):
        return val.isoformat()
    return str(val)

try:
    conexao = mysql.connector.connect(**banco_dados)

    if conexao.is_connected():
        print('✅ Conexão bem sucedida!')
        cursor = conexao.cursor()

        # Montar SQL de criação
        colunas_sql = [
            f"`{col}` {tipo_mysql(df[col].dtype)}"
            for col in df.columns
        ]
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS torre_controle (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {', '.join(colunas_sql)}
        )
        """
        cursor.execute(create_table_sql)

        # ── Verificar se colunas batem ──────────────────────────
        cursor.execute("SHOW COLUMNS FROM torre_controle")
        colunas_banco = [row[0] for row in cursor.fetchall()]
        colunas_banco_sem_id = [c for c in colunas_banco if c != 'id']
        colunas_excel = list(df.columns)

        if colunas_banco_sem_id != colunas_excel:
            print(f"⚠️  Colunas divergem! Recriando tabela...")
            print(f"   Banco : {colunas_banco_sem_id}")
            print(f"   Excel : {colunas_excel}")
            cursor.execute("DROP TABLE torre_controle")
            cursor.execute(create_table_sql)
            print("✅ Tabela recriada!")
        else:
            print('✅ Tabela verificada!')
        # ───────────────────────────────────────────────────────

        colunas = ', '.join([f"`{col}`" for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        sql = f"INSERT INTO torre_controle ({colunas}) VALUES ({placeholders})"

        dados = [
            tuple(tratar_valor(val) for val in row)
            for row in df.itertuples(index=False, name=None)
        ]

        cursor.executemany(sql, dados)
        conexao.commit()
        print(f'✅ {cursor.rowcount} linhas inseridas com sucesso!')

except Error as e:
    print(f'❌ Erro MySQL: {e}')

finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()
        print('🔒 Conexão encerrada!')