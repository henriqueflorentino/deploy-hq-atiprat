from app import app, mysql

with app.app_context():
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT
            )
        """)
        mysql.connection.commit()
        print("✅ Tabela 'item' criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")
    finally:
        cur.close()