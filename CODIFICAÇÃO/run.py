from flask import Flask
from core.views import app, db # Importando as rotas

if __name__ == '__main__':
    print("Iniciando o servidor Flask")
    
    app.run(debug=True, use_reloader=True)
