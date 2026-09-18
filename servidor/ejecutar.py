from infraestructura.aplicacion_flask import crear_app

app = crear_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
