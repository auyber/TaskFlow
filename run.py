# run.py
from app import create_app, db
from app.models import User, Post  # Importe os modelos para garantir que o SQLAlchemy os registre

app = create_app()

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()  # Cria as tabelas no banco de dados (se ainda não existirem)

if __name__ == "__main__":
    app.run(debug=True)
