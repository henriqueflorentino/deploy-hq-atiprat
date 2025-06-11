from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configurações essenciais
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-segura-123'

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Retorna resultados como dicionários

mysql = MySQL(app)

from app import routes